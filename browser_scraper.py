"""
Shared-browser scraper for Yellow Pages.

Key insight: Chromium's RAM cost is mostly the PROCESS startup (~200MB).
Browser contexts (like incognito windows) within one process are cheap (~5-10MB each).

So instead of 150 browser processes = 30GB RAM,
we use 1 browser process + 150 contexts = ~1.5GB RAM.
"""

import asyncio
import logging
import random
from typing import List, Dict, Optional, Callable
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Browser, Playwright
from proxy_manager import ProxyManager, Proxy

logger = logging.getLogger(__name__)

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
]

BROWSER_ARGS = [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--disable-background-networking',
    '--disable-default-apps',
    '--disable-sync',
    '--disable-translate',
    '--metrics-recording-only',
    '--no-first-run',
    '--disable-background-timer-throttling',
    '--disable-renderer-backgrounding',
    '--disable-backgrounding-occluded-windows',
    '--disable-component-update',
    '--disable-hang-monitor',
    '--js-flags=--max-old-space-size=256',
]

# Timeout for a single search (all pages). Prevents indefinite hangs.
SEARCH_TIMEOUT_SECONDS = 120


def build_url(search_term: str, location: str, page: int = 1) -> str:
    search_encoded = search_term.replace(' ', '+')
    location_encoded = location.replace(' ', '+').replace(',', '%2C')
    base = "https://www.yellowpages.com/search"
    url = f"{base}?search_terms={search_encoded}&geo_location_terms={location_encoded}"
    if page > 1:
        url += f"&page={page}"
    return url


def parse_listing(listing) -> Optional[Dict]:
    business = {}

    name_elem = listing.find('a', class_='business-name')
    if name_elem:
        business['name'] = name_elem.get_text(strip=True)
    else:
        return None

    phone_elem = listing.find('div', class_='phones')
    business['phone'] = phone_elem.get_text(strip=True) if phone_elem else ''

    street_elem = listing.find('div', class_='street-address')
    locality_elem = listing.find('div', class_='locality')
    business['street'] = street_elem.get_text(strip=True) if street_elem else ''
    business['city'] = ''
    business['state'] = ''
    business['zip'] = ''

    if locality_elem:
        locality_text = locality_elem.get_text(strip=True)
        parts = locality_text.split(',')
        if len(parts) >= 2:
            business['city'] = parts[0].strip()
            state_zip = parts[1].strip().split()
            if len(state_zip) >= 1:
                business['state'] = state_zip[0]
            if len(state_zip) >= 2:
                business['zip'] = state_zip[1]

    website_elem = listing.find('a', class_='track-visit-website')
    business['website'] = website_elem.get('href', '') if website_elem else ''

    categories_elem = listing.find('div', class_='categories')
    business['categories'] = categories_elem.get_text(strip=True) if categories_elem else ''

    rating_elem = listing.find('div', class_='result-rating')
    business['rating'] = rating_elem.get_text(strip=True) if rating_elem else ''

    yib_elem = listing.find('div', class_='years-in-business')
    business['years_in_business'] = yib_elem.get_text(strip=True) if yib_elem else ''

    return business


def extract_businesses(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, 'lxml')
    businesses = []
    listings = soup.find_all('div', class_='result')
    if not listings:
        listings = soup.find_all('div', class_='search-results organic')
    for listing in listings:
        try:
            biz = parse_listing(listing)
            if biz:
                businesses.append(biz)
        except Exception:
            continue
    return businesses


async def scrape_one_search(
    browser: Browser,
    search_term: str,
    location: str,
    max_pages: int = 5,
    proxy: Optional[Proxy] = None,
    delay: float = 1.5,
) -> List[Dict]:
    """
    Scrape one search using a lightweight browser context.
    Each context is like an incognito window — own cookies, ~5-10MB RAM.
    """
    businesses = []
    context = None

    ctx_options = {'user_agent': random.choice(USER_AGENTS)}
    if proxy:
        ctx_options['proxy'] = proxy.to_playwright_dict()

    try:
        context = await browser.new_context(**ctx_options)
        page = await context.new_page()

        for page_num in range(1, max_pages + 1):
            url = build_url(search_term, location, page_num)

            try:
                response = await page.goto(url, wait_until='domcontentloaded', timeout=30000)

                if response:
                    status = response.status
                    if status in (429, 403):
                        if proxy:
                            proxy.record_failure(is_block=True)
                        break
                    elif status >= 400:
                        break

                await asyncio.sleep(delay)
                html = await page.content()

                if proxy:
                    proxy.record_success()

                page_businesses = extract_businesses(html)
                if not page_businesses:
                    break

                businesses.extend(page_businesses)

            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.warning(f"Error scraping {search_term} in {location} page {page_num}: {e}")
                break

    except asyncio.CancelledError:
        raise
    except Exception as e:
        logger.warning(f"Context error for {search_term} in {location}: {e}")
    finally:
        if context:
            try:
                await context.close()
            except Exception:
                pass

    return businesses


async def scrape_batch(
    searches: List[Dict],
    max_pages: int = 5,
    proxy_manager: Optional[ProxyManager] = None,
    max_concurrent: int = 50,
    delay: float = 1.5,
    on_result: Optional[Callable] = None,
    on_error: Optional[Callable] = None,
    stop_check: Optional[Callable] = None,
) -> List[Dict]:
    """
    Scrape all searches using ONE shared browser process + many concurrent contexts.

    Memory model:
    - 1 Chromium process: ~200-250MB base
    - Each context: ~5-10MB
    - 50 concurrent contexts: ~500MB total
    - 150 concurrent contexts: ~1.75GB total
    """
    all_businesses = []
    all_lock = asyncio.Lock()
    semaphore = asyncio.Semaphore(max_concurrent)
    total = len(searches)
    completed_count = 0
    error_count = 0
    count_lock = asyncio.Lock()

    pw = None
    browser = None

    try:
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=True, args=BROWSER_ARGS)
        logger.info(f"Shared browser started. Running up to {min(max_concurrent, total)} concurrent contexts.")

        async def run_one(idx, search):
            nonlocal completed_count, error_count

            if stop_check and stop_check():
                return

            async with semaphore:
                if stop_check and stop_check():
                    return

                proxy = proxy_manager.get_next_proxy() if proxy_manager else None
                await asyncio.sleep(random.uniform(0, 0.3))

                try:
                    businesses = await asyncio.wait_for(
                        scrape_one_search(
                            browser=browser,
                            search_term=search['term'],
                            location=search['location'],
                            max_pages=max_pages,
                            proxy=proxy,
                            delay=delay,
                        ),
                        timeout=SEARCH_TIMEOUT_SECONDS,
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"Search timed out: {search['term']} in {search['location']}")
                    businesses = []
                    async with count_lock:
                        error_count += 1
                    if on_error:
                        on_error(idx + 1, total, f"Timeout: {search['term']} in {search['location']}")
                    return
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    logger.error(f"Search failed: {search['term']} in {search['location']}: {e}")
                    businesses = []
                    async with count_lock:
                        error_count += 1
                    if on_error:
                        on_error(idx + 1, total, str(e))
                    return

                for biz in businesses:
                    biz['search_category'] = search['term']
                    biz['search_location'] = search['location']

                async with all_lock:
                    all_businesses.extend(businesses)

                async with count_lock:
                    completed_count += 1
                    if not businesses:
                        error_count += 1

                if on_result:
                    on_result(completed_count, total, businesses, error_count)

        tasks = [asyncio.create_task(run_one(i, s)) for i, s in enumerate(searches)]

        # Wait for all tasks, handle cancellation gracefully
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            for t in tasks:
                t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

    except asyncio.CancelledError:
        logger.info("Scrape batch cancelled")
    except Exception as e:
        logger.error(f"Browser error: {e}")
    finally:
        if browser:
            try:
                await asyncio.wait_for(browser.close(), timeout=10)
            except Exception:
                logger.warning("Browser close timed out, forcing cleanup")
        if pw:
            try:
                await asyncio.wait_for(pw.stop(), timeout=10)
            except Exception:
                logger.warning("Playwright stop timed out")

    return all_businesses

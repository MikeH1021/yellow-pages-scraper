"""
Lightweight HTTP-based Yellow Pages scraper.
Replaces Playwright/Chromium with aiohttp for ~150x less RAM per worker.

Playwright: ~300MB per browser instance
aiohttp:    ~2MB per concurrent request

With 150 proxies and 150 concurrent workers: ~300MB total vs ~45GB with Playwright.
"""

import asyncio
import logging
import random
import time
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import aiohttp
from proxy_manager import ProxyManager, Proxy

logger = logging.getLogger(__name__)

# Rotate user agents to reduce fingerprinting
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0',
]


def _get_headers(ua: str, referer: str = None) -> dict:
    """Build browser-like headers."""
    headers = {
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin' if referer else 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    if referer:
        headers['Referer'] = referer
    return headers


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


async def _warm_session(session: aiohttp.ClientSession, ua: str, proxy_url: str = None):
    """Visit yellowpages.com homepage to get cookies before scraping."""
    try:
        headers = _get_headers(ua)
        async with session.get(
            'https://www.yellowpages.com',
            headers=headers,
            proxy=proxy_url,
            timeout=aiohttp.ClientTimeout(total=15),
            ssl=False,
            allow_redirects=True,
        ) as resp:
            await resp.read()  # consume body to complete the request
    except Exception:
        pass  # best-effort; some proxies may fail here


async def scrape_search(
    session: aiohttp.ClientSession,
    search_term: str,
    location: str,
    max_pages: int = 5,
    proxy: Optional[Proxy] = None,
    delay: float = 1.0,
    ua: str = None,
) -> List[Dict]:
    """Scrape a single search term + location combo, all pages."""
    businesses = []
    if not ua:
        ua = random.choice(USER_AGENTS)
    proxy_url = proxy.url if proxy else None

    # Warm the session to get cookies on first use
    if not session.cookie_jar:
        await _warm_session(session, ua, proxy_url)

    referer = 'https://www.yellowpages.com'

    for page_num in range(1, max_pages + 1):
        url = build_url(search_term, location, page_num)
        headers = _get_headers(ua, referer=referer)

        try:
            async with session.get(
                url,
                headers=headers,
                proxy=proxy_url,
                timeout=aiohttp.ClientTimeout(total=30),
                ssl=False,
                allow_redirects=True,
            ) as response:
                if response.status == 429:
                    logger.warning(f"Rate limited (429) on page {page_num}")
                    if proxy:
                        proxy.record_failure(is_block=True)
                    break
                elif response.status == 403:
                    logger.warning(f"Forbidden (403) on page {page_num}")
                    if proxy:
                        proxy.record_failure(is_block=True)
                    break
                elif response.status >= 400:
                    logger.warning(f"HTTP {response.status} on page {page_num}")
                    break

                html = await response.text()
                referer = str(response.url)

                if proxy:
                    proxy.record_success()

            page_businesses = extract_businesses(html)

            if not page_businesses:
                break

            businesses.extend(page_businesses)

            if page_num < max_pages:
                await asyncio.sleep(delay + random.uniform(0, 0.5))

        except asyncio.TimeoutError:
            logger.warning(f"Timeout on page {page_num}")
            break
        except Exception as e:
            logger.warning(f"Error on page {page_num}: {e}")
            break

    return businesses


async def scrape_batch(
    searches: List[Dict],
    max_pages: int = 5,
    proxy_manager: Optional[ProxyManager] = None,
    max_concurrent: int = 50,
    delay: float = 1.0,
    on_result=None,
    stop_check=None,
) -> List[Dict]:
    """
    Scrape a list of searches with high concurrency using HTTP requests.

    Each concurrent worker gets its own cookie jar (simulating separate browser sessions).
    With proxies, each worker also gets a unique IP.
    """
    all_businesses = []
    semaphore = asyncio.Semaphore(max_concurrent)
    total = len(searches)

    async def run_one(idx, search):
        if stop_check and stop_check():
            return []

        async with semaphore:
            # Assign a proxy from the pool
            proxy = None
            if proxy_manager:
                proxy = proxy_manager.get_next_proxy()

            # Small stagger to avoid burst
            await asyncio.sleep(random.uniform(0, 0.5))

            # Each search gets its own cookie jar = its own "browser session"
            jar = aiohttp.CookieJar(unsafe=True)
            connector = aiohttp.TCPConnector(
                limit=5,
                ttl_dns_cache=300,
                ssl=False,
                enable_cleanup_closed=True,
            )
            ua = random.choice(USER_AGENTS)

            async with aiohttp.ClientSession(cookie_jar=jar, connector=connector) as session:
                # Warm session: visit homepage to get cookies
                proxy_url = proxy.url if proxy else None
                await _warm_session(session, ua, proxy_url)

                businesses = await scrape_search(
                    session=session,
                    search_term=search['term'],
                    location=search['location'],
                    max_pages=max_pages,
                    proxy=proxy,
                    delay=delay,
                    ua=ua,
                )

            for biz in businesses:
                biz['search_category'] = search['term']
                biz['search_location'] = search['location']

            if on_result:
                on_result(idx + 1, total, businesses)

            return businesses

    # Launch ALL searches concurrently (semaphore limits actual concurrency)
    tasks = [run_one(i, s) for i, s in enumerate(searches)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, list):
            all_businesses.extend(result)

    return all_businesses

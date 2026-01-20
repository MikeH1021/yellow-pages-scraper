"""
Yellow Pages Scraper
Scrapes business listings from YellowPages.com for multiple categories
"""

import asyncio
import csv
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup
import pandas as pd
from proxy_manager import ProxyManager, Proxy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class YellowPagesScraper:
    """Scraper for YellowPages.com business listings"""

    # States east of Colorado
    EASTERN_STATES = [
        'AL', 'AR', 'CT', 'DE', 'FL', 'GA', 'IL', 'IN', 'IA', 'KS', 'KY',
        'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'NE', 'NH', 'NJ',
        'NY', 'NC', 'ND', 'OH', 'OK', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
        'VT', 'VA', 'WV', 'WI', 'DC'
    ]

    def __init__(self, headless: bool = True, delay: float = 2.0, proxy_manager: Optional[ProxyManager] = None):
        """
        Initialize the scraper

        Args:
            headless: Run browser in headless mode
            delay: Delay between page loads (seconds)
            proxy_manager: Optional ProxyManager for IP rotation
        """
        self.headless = headless
        self.delay = delay
        self.proxy_manager = proxy_manager
        self.browser: Optional[Browser] = None
        self.results: List[Dict] = []

    async def start_browser(self, proxy: Optional[Proxy] = None):
        """
        Start the Playwright browser

        Args:
            proxy: Optional proxy to use for this browser instance
        """
        self.playwright = await async_playwright().start()

        launch_args = {
            'headless': self.headless,
            'args': ['--disable-blink-features=AutomationControlled']
        }

        # Add proxy if provided
        if proxy:
            launch_args['proxy'] = proxy.to_playwright_dict()
            logger.info(f"🔒 Using proxy: {proxy.host}:{proxy.port}")
        elif self.proxy_manager:
            proxy = self.proxy_manager.get_next_proxy()
            if proxy:
                launch_args['proxy'] = proxy.to_playwright_dict()
                logger.info(f"🔒 Using proxy: {proxy.host}:{proxy.port}")

        self.browser = await self.playwright.chromium.launch(**launch_args)

    async def close_browser(self):
        """Close the browser and playwright"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()

    async def scrape_search(
        self,
        search_term: str,
        location: str,
        max_pages: int = 5
    ) -> List[Dict]:
        """
        Scrape Yellow Pages for a specific search term and location

        Args:
            search_term: What to search for (e.g., "building supply")
            location: Where to search (e.g., "Miami, FL")
            max_pages: Maximum number of pages to scrape

        Returns:
            List of business dictionaries
        """
        if not self.browser:
            await self.start_browser()

        context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = await context.new_page()

        businesses = []

        for page_num in range(1, max_pages + 1):
            logger.info(f"📄 Scraping page {page_num}/{max_pages} for '{search_term}' in {location}...")

            # Construct URL
            url = self._build_url(search_term, location, page_num)
            logger.debug(f"URL: {url}")

            try:
                # Navigate to the page
                logger.debug("Loading page...")
                response = await page.goto(url, wait_until='networkidle', timeout=30000)

                # Check for rate limiting
                if response:
                    status = response.status
                    if status == 429:
                        logger.error(f"🚫 RATE LIMITED (429) on page {page_num}")
                        logger.error("Too many requests. Solutions:")
                        logger.error("  1. Increase DELAY_BETWEEN_PAGES (try 5-10 seconds)")
                        logger.error("  2. Use proxies (run get_free_proxies.py)")
                        logger.error("  3. Wait 1-2 hours before retrying")
                        break
                    elif status == 403:
                        logger.error(f"🚫 ACCESS FORBIDDEN (403) on page {page_num}")
                        logger.error("Your IP is likely blocked. Solutions:")
                        logger.error("  1. Use proxies (required for large scrapes)")
                        logger.error("  2. Wait 2-4 hours before retrying")
                        logger.error("  3. Use paid residential proxies")
                        break
                    elif status >= 400:
                        logger.warning(f"⚠️  HTTP {status} on page {page_num}")

                logger.debug(f"Waiting {self.delay}s before extracting...")
                await asyncio.sleep(self.delay)

                # Extract businesses from current page
                page_businesses = await self._extract_businesses(page)

                if not page_businesses:
                    if page_num == 1:
                        logger.error(f"⚠️  No results on FIRST page - possible block or bad search")
                        logger.warning("Check:")
                        logger.warning("  1. Is this search valid? (test on yellowpages.com)")
                        logger.warning("  2. Are you being blocked? (use proxies)")
                        logger.warning("  3. Did Yellow Pages change their HTML? (check STRUCTURE_NOTES.md)")
                    else:
                        logger.warning(f"⚠️  No results found on page {page_num} - stopping")
                    break

                businesses.extend(page_businesses)
                logger.info(f"✓ Found {len(page_businesses)} businesses on page {page_num} (Total: {len(businesses)})")

            except Exception as e:
                error_msg = str(e)
                if "timeout" in error_msg.lower():
                    logger.error(f"⏱️  Timeout on page {page_num} - page took too long to load")
                    logger.warning("Possible slow proxy or rate limiting")
                elif "net::ERR" in error_msg:
                    logger.error(f"🌐 Network error on page {page_num}: {error_msg}")
                else:
                    logger.error(f"❌ Error on page {page_num}: {error_msg}")
                break

        await context.close()
        return businesses

    def _build_url(self, search_term: str, location: str, page: int = 1) -> str:
        """Build Yellow Pages search URL"""
        base_url = "https://www.yellowpages.com/search"
        search_encoded = search_term.replace(' ', '+')
        location_encoded = location.replace(' ', '+').replace(',', '%2C')

        if page == 1:
            return f"{base_url}?search_terms={search_encoded}&geo_location_terms={location_encoded}"
        else:
            return f"{base_url}?search_terms={search_encoded}&geo_location_terms={location_encoded}&page={page}"

    async def _extract_businesses(self, page: Page) -> List[Dict]:
        """Extract business information from a page"""
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        businesses = []

        # Find all business listings - Yellow Pages uses various selectors
        # Common class patterns: 'result', 'search-results organic', etc.
        listings = soup.find_all('div', class_='result')

        if not listings:
            # Try alternative selector
            listings = soup.find_all('div', class_='search-results organic')

        logger.debug(f"Found {len(listings)} potential listings on page")

        for listing in listings:
            try:
                business = self._parse_listing(listing)
                if business:
                    businesses.append(business)
                    logger.debug(f"  ✓ Parsed: {business.get('name', 'N/A')}")
            except Exception as e:
                logger.warning(f"  ⚠️  Error parsing listing: {str(e)}")
                continue

        return businesses

    def _parse_listing(self, listing) -> Optional[Dict]:
        """Parse a single business listing"""
        business = {}

        # Business name
        name_elem = listing.find('a', class_='business-name')
        if name_elem:
            business['name'] = name_elem.get_text(strip=True)
        else:
            return None

        # Phone number
        phone_elem = listing.find('div', class_='phones')
        if phone_elem:
            business['phone'] = phone_elem.get_text(strip=True)
        else:
            business['phone'] = ''

        # Address
        street_elem = listing.find('div', class_='street-address')
        locality_elem = listing.find('div', class_='locality')

        if street_elem:
            business['street'] = street_elem.get_text(strip=True)
        else:
            business['street'] = ''

        if locality_elem:
            locality_text = locality_elem.get_text(strip=True)
            business['city'] = ''
            business['state'] = ''
            business['zip'] = ''

            # Parse "City, ST ZIP"
            parts = locality_text.split(',')
            if len(parts) >= 2:
                business['city'] = parts[0].strip()
                state_zip = parts[1].strip().split()
                if len(state_zip) >= 1:
                    business['state'] = state_zip[0]
                if len(state_zip) >= 2:
                    business['zip'] = state_zip[1]
        else:
            business['city'] = ''
            business['state'] = ''
            business['zip'] = ''

        # Website
        website_elem = listing.find('a', class_='track-visit-website')
        if website_elem:
            business['website'] = website_elem.get('href', '')
        else:
            business['website'] = ''

        # Categories/Services
        categories_elem = listing.find('div', class_='categories')
        if categories_elem:
            business['categories'] = categories_elem.get_text(strip=True)
        else:
            business['categories'] = ''

        # Rating
        rating_elem = listing.find('div', class_='result-rating')
        if rating_elem:
            business['rating'] = rating_elem.get_text(strip=True)
        else:
            business['rating'] = ''

        # Years in business
        yib_elem = listing.find('div', class_='years-in-business')
        if yib_elem:
            business['years_in_business'] = yib_elem.get_text(strip=True)
        else:
            business['years_in_business'] = ''

        return business

    def filter_eastern_states(self, businesses: List[Dict]) -> List[Dict]:
        """Filter businesses to only those in states east of Colorado"""
        return [
            business for business in businesses
            if business.get('state', '').upper() in self.EASTERN_STATES
        ]

    def save_to_csv(self, businesses: List[Dict], filename: str):
        """Save businesses to CSV file"""
        if not businesses:
            logger.warning("No businesses to save")
            return

        df = pd.DataFrame(businesses)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"💾 Saved {len(businesses)} businesses to {filename}")

    def save_to_json(self, businesses: List[Dict], filename: str):
        """Save businesses to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(businesses, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved {len(businesses)} businesses to {filename}")


async def main():
    """Main execution function"""

    # Define search categories
    categories = [
        {"term": "building supply", "location": "United States"},
        {"term": "shutters", "location": "United States"},
        {"term": "millwork", "location": "United States"},
        {"term": "lumber", "location": "United States"},
        {"term": "architects", "location": "United States"},
    ]

    scraper = YellowPagesScraper(headless=False, delay=2.0)

    try:
        await scraper.start_browser()

        all_businesses = []

        for category in categories:
            print(f"\n{'='*60}")
            print(f"Scraping category: {category['term']}")
            print(f"{'='*60}\n")

            businesses = await scraper.scrape_search(
                search_term=category['term'],
                location=category['location'],
                max_pages=3  # Adjust as needed
            )

            # Tag with category
            for business in businesses:
                business['search_category'] = category['term']

            all_businesses.extend(businesses)

            # Save individual category results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            category_filename = f"{category['term'].replace(' ', '_')}_{timestamp}.csv"
            scraper.save_to_csv(businesses, category_filename)

        # Filter for eastern states
        print(f"\n{'='*60}")
        print("Filtering for states east of Colorado...")
        print(f"{'='*60}\n")

        eastern_businesses = scraper.filter_eastern_states(all_businesses)

        # Save combined results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scraper.save_to_csv(all_businesses, f"all_businesses_{timestamp}.csv")
        scraper.save_to_csv(eastern_businesses, f"eastern_businesses_{timestamp}.csv")

        print(f"\n{'='*60}")
        print(f"Scraping complete!")
        print(f"Total businesses found: {len(all_businesses)}")
        print(f"Businesses in eastern states: {len(eastern_businesses)}")
        print(f"{'='*60}\n")

    finally:
        await scraper.close_browser()


if __name__ == "__main__":
    asyncio.run(main())

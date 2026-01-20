"""
Simple example of using the Yellow Pages scraper
This script shows how to scrape a single category in a specific location
"""

import asyncio
from yellowpages_scraper import YellowPagesScraper


async def main():
    """Simple scraping example"""

    # Create scraper instance
    scraper = YellowPagesScraper(
        headless=False,  # Show browser window
        delay=2.0  # Wait 2 seconds between pages
    )

    try:
        # Start the browser
        await scraper.start_browser()

        # Scrape building supply companies in Miami, FL
        print("Scraping building supply companies in Miami, FL...")
        businesses = await scraper.scrape_search(
            search_term="building supply",
            location="Miami, FL",
            max_pages=2  # Scrape first 2 pages
        )

        print(f"\nFound {len(businesses)} businesses!")

        # Display first few results
        print("\nFirst 3 results:")
        for i, business in enumerate(businesses[:3], 1):
            print(f"\n{i}. {business.get('name', 'N/A')}")
            print(f"   Phone: {business.get('phone', 'N/A')}")
            print(f"   Address: {business.get('street', 'N/A')}, {business.get('city', 'N/A')}")

        # Save to CSV
        scraper.save_to_csv(businesses, "miami_building_supply.csv")

    finally:
        # Always close the browser
        await scraper.close_browser()


if __name__ == "__main__":
    asyncio.run(main())

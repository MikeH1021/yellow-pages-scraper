"""
Run the Yellow Pages scraper using settings from config.py
This is the main entry point for the scraper
"""

import asyncio
import os
from datetime import datetime
from yellowpages_scraper import YellowPagesScraper
from proxy_manager import ProxyManager, create_paid_proxy_pool
import config


async def main():
    """Main execution function using config settings"""

    print("=" * 60)
    print("Yellow Pages Scraper")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Headless mode: {config.HEADLESS_MODE}")
    print(f"  Delay between pages: {config.DELAY_BETWEEN_PAGES}s")
    print(f"  Max pages per search: {config.MAX_PAGES_PER_SEARCH}")
    print(f"  Categories to scrape: {len(config.SEARCH_CATEGORIES)}")

    # Setup proxy manager if enabled
    proxy_manager = None

    if config.USE_PAID_PROXY_SERVICE:
        print(f"  Proxy mode: Paid service")
        service = os.getenv('PROXY_SERVICE') or config.PROXY_SERVICE
        username = os.getenv('PROXY_USERNAME') or config.PROXY_USERNAME
        password = os.getenv('PROXY_PASSWORD') or config.PROXY_PASSWORD

        if not all([service, username, password]):
            print("\n❌ ERROR: Proxy service credentials not set!")
            print("Set environment variables:")
            print("  export PROXY_SERVICE='smartproxy'")
            print("  export PROXY_USERNAME='your-username'")
            print("  export PROXY_PASSWORD='your-password'")
            return

        proxy_manager = create_paid_proxy_pool(
            service=service,
            username=username,
            password=password,
            count=5
        )
        print(f"  Service: {service}")

    elif config.USE_PROXIES:
        print(f"  Proxy mode: File-based ({config.PROXY_FILE})")
        proxy_manager = ProxyManager.from_file(
            config.PROXY_FILE,
            validate=config.VALIDATE_PROXIES
        )

        if config.VALIDATE_PROXIES:
            print("\nValidating proxies...")
            await proxy_manager.validate_all_proxies()

            if not proxy_manager.proxies:
                print("\n❌ ERROR: No working proxies found!")
                print(f"Check your {config.PROXY_FILE} file")
                return

        print(f"  Proxies loaded: {len(proxy_manager.proxies)}")

    else:
        print(f"  Proxy mode: None (may risk IP ban)")

    print("=" * 60)

    # Create scraper instance
    scraper = YellowPagesScraper(
        headless=config.HEADLESS_MODE,
        delay=config.DELAY_BETWEEN_PAGES,
        proxy_manager=proxy_manager
    )

    try:
        await scraper.start_browser()

        all_businesses = []

        # Scrape each category
        for i, category in enumerate(config.SEARCH_CATEGORIES, 1):
            print(f"\n{'='*60}")
            print(f"[{i}/{len(config.SEARCH_CATEGORIES)}] Scraping: {category['term']}")
            print(f"Location: {category['location']}")
            print(f"{'='*60}\n")

            businesses = await scraper.scrape_search(
                search_term=category['term'],
                location=category['location'],
                max_pages=config.MAX_PAGES_PER_SEARCH
            )

            # Tag with category
            for business in businesses:
                business['search_category'] = category['term']

            all_businesses.extend(businesses)
            print(f"✓ Found {len(businesses)} businesses for '{category['term']}'")

            # Save individual category results if configured
            if config.SAVE_INDIVIDUAL_CATEGORIES:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                category_name = category['term'].replace(' ', '_')
                filename = f"{category_name}_{timestamp}.csv"

                if config.OUTPUT_DIR:
                    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
                    filename = os.path.join(config.OUTPUT_DIR, filename)

                scraper.save_to_csv(businesses, filename)

        # Save combined results if configured
        if config.SAVE_COMBINED_RESULTS and all_businesses:
            print(f"\n{'='*60}")
            print("Saving combined results...")
            print(f"{'='*60}\n")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"all_businesses_{timestamp}.csv"

            if config.OUTPUT_DIR:
                filename = os.path.join(config.OUTPUT_DIR, filename)

            scraper.save_to_csv(all_businesses, filename)

        # Filter and save eastern states if configured
        if config.SAVE_EASTERN_STATES_ONLY and all_businesses:
            print(f"\n{'='*60}")
            print("Filtering for states east of Colorado...")
            print(f"{'='*60}\n")

            eastern_businesses = scraper.filter_eastern_states(all_businesses)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"eastern_businesses_{timestamp}.csv"

            if config.OUTPUT_DIR:
                filename = os.path.join(config.OUTPUT_DIR, filename)

            scraper.save_to_csv(eastern_businesses, filename)
            print(f"✓ {len(eastern_businesses)} businesses in eastern states")

        # Final summary
        print(f"\n{'='*60}")
        print("SCRAPING COMPLETE!")
        print(f"{'='*60}")
        print(f"Total businesses found: {len(all_businesses)}")
        print(f"Categories scraped: {len(config.SEARCH_CATEGORIES)}")

        if config.SAVE_EASTERN_STATES_ONLY:
            eastern_count = len(scraper.filter_eastern_states(all_businesses))
            print(f"Businesses in eastern states: {eastern_count}")

        print(f"{'='*60}\n")

    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")

    except Exception as e:
        print(f"\n\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        await scraper.close_browser()


if __name__ == "__main__":
    asyncio.run(main())

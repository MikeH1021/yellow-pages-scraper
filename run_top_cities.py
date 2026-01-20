"""
Run scraper with TOP CITIES strategy
This is the RECOMMENDED approach for comprehensive coverage
"""

import asyncio
import os
from datetime import datetime
from yellowpages_scraper import YellowPagesScraper
from proxy_manager import ProxyManager, create_paid_proxy_pool
import config_top_cities as config


async def main():
    """Main execution using top cities strategy"""

    print("=" * 60)
    print("Yellow Pages Scraper - TOP CITIES Strategy")
    print("=" * 60)

    # Show what we're doing
    print(f"\nThis will scrape:")
    print(f"  • {len(config.CITY_LIST)} cities")
    print(f"  • {len(config.CATEGORIES)} categories")
    print(f"  • {len(config.SEARCH_CATEGORIES)} total searches")
    print(f"  • Up to {config.MAX_PAGES_PER_SEARCH} pages each")
    print(f"  • ~{len(config.SEARCH_CATEGORIES) * config.MAX_PAGES_PER_SEARCH} total pages")

    est_time_min = len(config.SEARCH_CATEGORIES) * config.MAX_PAGES_PER_SEARCH * 6 / 60
    print(f"\nEstimated time: {est_time_min:.0f} minutes ({est_time_min/60:.1f} hours)")

    if not config.USE_PROXIES:
        print("\n⚠️  WARNING: Proxies not enabled!")
        print("You will likely get blocked scraping this many pages.")
        print("Enable USE_PROXIES in config_top_cities.py")
        response = input("\nContinue anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("Exiting. Enable proxies first!")
            return

    # Setup proxy manager
    proxy_manager = None

    if config.USE_PAID_PROXY_SERVICE:
        service = os.getenv('PROXY_SERVICE') or config.PROXY_SERVICE
        username = os.getenv('PROXY_USERNAME')
        password = os.getenv('PROXY_PASSWORD')

        if not all([service, username, password]):
            print("\n❌ ERROR: Proxy credentials not set!")
            print("Set environment variables or edit config_top_cities.py")
            return

        proxy_manager = create_paid_proxy_pool(service, username, password, count=5)
        print(f"  Proxy service: {service}")

    elif config.USE_PROXIES:
        proxy_manager = ProxyManager.from_file(
            config.PROXY_FILE,
            validate=config.VALIDATE_PROXIES
        )

        if config.VALIDATE_PROXIES:
            print("\nValidating proxies...")
            await proxy_manager.validate_all_proxies()

        if not proxy_manager.proxies:
            print("\n❌ ERROR: No working proxies!")
            print("Run: python get_free_proxies.py")
            return

        print(f"  Proxies: {len(proxy_manager.proxies)} loaded")

    print("=" * 60)

    # Confirm before starting
    response = input("\nReady to start scraping? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        return

    print("\n🚀 Starting scrape...\n")

    # Create scraper
    scraper = YellowPagesScraper(
        headless=config.HEADLESS_MODE,
        delay=config.DELAY_BETWEEN_PAGES,
        proxy_manager=proxy_manager
    )

    all_businesses = []
    start_time = datetime.now()

    try:
        await scraper.start_browser()

        # Scrape each city/category combo
        for i, search in enumerate(config.SEARCH_CATEGORIES, 1):
            print(f"\n{'='*60}")
            print(f"[{i}/{len(config.SEARCH_CATEGORIES)}] {search['term']} in {search['location']}")
            print(f"{'='*60}")

            businesses = await scraper.scrape_search(
                search_term=search['term'],
                location=search['location'],
                max_pages=config.MAX_PAGES_PER_SEARCH
            )

            # Tag with search info
            for biz in businesses:
                biz['search_category'] = search['term']
                biz['search_location'] = search['location']

            all_businesses.extend(businesses)

            # Save checkpoint every 25 searches
            if i % 25 == 0:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                checkpoint_file = f"checkpoint_{i}searches_{timestamp}.csv"
                scraper.save_to_csv(all_businesses, checkpoint_file)
                print(f"\n💾 Checkpoint saved: {checkpoint_file}")

            # Progress update
            elapsed = (datetime.now() - start_time).total_seconds()
            avg_time = elapsed / i
            remaining = (len(config.SEARCH_CATEGORIES) - i) * avg_time
            print(f"\nProgress: {i}/{len(config.SEARCH_CATEGORIES)} searches")
            print(f"Total businesses: {len(all_businesses)}")
            print(f"Est. time remaining: {remaining/60:.0f} minutes")

        # Save final results
        print(f"\n{'='*60}")
        print("Saving final results...")
        print(f"{'='*60}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save all businesses
        all_file = f"top_cities_all_businesses_{timestamp}.csv"
        scraper.save_to_csv(all_businesses, all_file)

        # Save by category
        if config.SAVE_INDIVIDUAL_CATEGORIES:
            for category in config.CATEGORIES:
                cat_businesses = [b for b in all_businesses if b.get('search_category') == category]
                cat_file = f"top_cities_{category.replace(' ', '_')}_{timestamp}.csv"
                scraper.save_to_csv(cat_businesses, cat_file)

        # Final summary
        elapsed_total = (datetime.now() - start_time).total_seconds()
        print(f"\n{'='*60}")
        print("✅ SCRAPING COMPLETE!")
        print(f"{'='*60}")
        print(f"Total businesses: {len(all_businesses)}")
        print(f"Cities scraped: {len(config.CITY_LIST)}")
        print(f"Categories: {len(config.CATEGORIES)}")
        print(f"Searches completed: {len(config.SEARCH_CATEGORIES)}")
        print(f"Time elapsed: {elapsed_total/60:.1f} minutes ({elapsed_total/3600:.2f} hours)")
        print(f"Average: {len(all_businesses)/len(config.SEARCH_CATEGORIES):.1f} businesses per search")
        print(f"{'='*60}")

        # Show breakdown by category
        print("\nResults by category:")
        for category in config.CATEGORIES:
            count = len([b for b in all_businesses if b.get('search_category') == category])
            print(f"  {category}: {count} businesses")

    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        emergency_file = f"emergency_save_{timestamp}.csv"
        scraper.save_to_csv(all_businesses, emergency_file)
        print(f"Partial results saved to: {emergency_file}")

    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await scraper.close_browser()


if __name__ == "__main__":
    asyncio.run(main())

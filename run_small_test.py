"""
Run SMALL TEST SCRAPE
Target: ~500 businesses from 2 cities
Perfect for testing before full run
"""

import asyncio
import os
from datetime import datetime
from yellowpages_scraper import YellowPagesScraper
from proxy_manager import ProxyManager
import config_small_test as config


async def main():
    """Small test run"""

    print("=" * 60)
    print("Yellow Pages Scraper - SMALL TEST RUN")
    print("=" * 60)
    print(f"\nTarget: ~500 businesses")
    print(f"Cities: {', '.join(config.TEST_CITIES)}")
    print(f"Categories: {len(config.CATEGORIES)}")
    print(f"Total searches: {len(config.SEARCH_CATEGORIES)}")
    print(f"Estimated time: {len(config.SEARCH_CATEGORIES) * config.MAX_PAGES_PER_SEARCH * 6 / 60:.0f} minutes")
    print("=" * 60)

    # Load proxies
    proxy_manager = None
    if config.USE_PROXIES:
        proxy_manager = ProxyManager.from_file(
            config.PROXY_FILE,
            validate=config.VALIDATE_PROXIES
        )

        if not proxy_manager.proxies:
            print("\n❌ ERROR: No proxies found in proxies.txt")
            return

        print(f"\n✅ Loaded {len(proxy_manager.proxies)} Webshare proxies")
    else:
        print("\n⚠️  Running without proxies")

    print("\n🚀 Starting test scrape...\n")

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

        # Scrape each search
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

            print(f"\n✓ Found {len(businesses)} businesses")
            print(f"Running total: {len(all_businesses)} businesses")

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        print(f"\n{'='*60}")
        print("Saving results...")
        print(f"{'='*60}")

        # Save all
        all_file = f"test_small_all_{timestamp}.csv"
        scraper.save_to_csv(all_businesses, all_file)

        # Save by category
        for category in config.CATEGORIES:
            cat_businesses = [b for b in all_businesses if b.get('search_category') == category]
            if cat_businesses:
                cat_file = f"test_small_{category.replace(' ', '_')}_{timestamp}.csv"
                scraper.save_to_csv(cat_businesses, cat_file)

        # Final summary
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n{'='*60}")
        print("✅ TEST COMPLETE!")
        print(f"{'='*60}")
        print(f"Total businesses: {len(all_businesses)}")
        print(f"Target was: ~500")
        print(f"Cities scraped: {len(config.TEST_CITIES)}")
        print(f"Categories: {len(config.CATEGORIES)}")
        print(f"Searches: {len(config.SEARCH_CATEGORIES)}")
        print(f"Time: {elapsed/60:.1f} minutes")
        print(f"Avg per search: {len(all_businesses)/len(config.SEARCH_CATEGORIES):.1f} businesses")
        print(f"{'='*60}")

        # Show breakdown
        print("\nResults by category:")
        for category in config.CATEGORIES:
            count = len([b for b in all_businesses if b.get('search_category') == category])
            print(f"  {category}: {count} businesses")

        print("\nResults by city:")
        for city in config.TEST_CITIES:
            count = len([b for b in all_businesses if b.get('search_location') == city])
            print(f"  {city}: {count} businesses")

        print(f"\n{'='*60}")
        print("📁 Files created:")
        print(f"  - {all_file}")
        for category in config.CATEGORIES:
            print(f"  - test_small_{category.replace(' ', '_')}_{timestamp}.csv")
        print(f"{'='*60}")

        # Data quality check
        with_phone = len([b for b in all_businesses if b.get('phone')])
        with_address = len([b for b in all_businesses if b.get('street')])

        print(f"\n📊 Data Quality:")
        print(f"  Businesses with phone: {with_phone}/{len(all_businesses)} ({with_phone/len(all_businesses)*100:.1f}%)")
        print(f"  Businesses with address: {with_address}/{len(all_businesses)} ({with_address/len(all_businesses)*100:.1f}%)")

        if with_phone / len(all_businesses) > 0.6:
            print(f"\n✅ Good data quality!")
        else:
            print(f"\n⚠️  Lower data quality - some listings incomplete")

        print(f"\n{'='*60}")
        print("Next steps:")
        print("  1. Check the CSV files")
        print("  2. Verify data quality")
        print("  3. If satisfied, run full scrape:")
        print("     python run_top_cities.py")
        print(f"{'='*60}\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        emergency_file = f"test_small_interrupted_{timestamp}.csv"
        scraper.save_to_csv(all_businesses, emergency_file)
        print(f"Partial results saved to: {emergency_file}")

    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await scraper.close_browser()


if __name__ == "__main__":
    asyncio.run(main())

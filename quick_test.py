"""
Quick automated test to verify scraper works
No user interaction required
"""

import asyncio
import logging
from yellowpages_scraper import YellowPagesScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


async def main():
    """Quick test without proxies"""
    logger.info("=" * 60)
    logger.info("QUICK TEST - Scraping 1 page without proxies")
    logger.info("=" * 60)

    scraper = YellowPagesScraper(
        headless=True,  # Run in background
        delay=2.0,
        proxy_manager=None
    )

    try:
        logger.info("Starting browser...")
        await scraper.start_browser()

        logger.info("Scraping building supply in Miami, FL (1 page)...")
        businesses = await scraper.scrape_search(
            search_term="building supply",
            location="Miami, FL",
            max_pages=1
        )

        if businesses:
            logger.info(f"\n{'='*60}")
            logger.info(f"✓ SUCCESS! Found {len(businesses)} businesses")
            logger.info(f"{'='*60}")

            # Show first result
            if businesses:
                biz = businesses[0]
                logger.info(f"\nFirst result:")
                logger.info(f"  Name: {biz.get('name', 'N/A')}")
                logger.info(f"  Phone: {biz.get('phone', 'N/A')}")
                logger.info(f"  Address: {biz.get('street', 'N/A')}, {biz.get('city', 'N/A')}")

            scraper.save_to_csv(businesses, "quick_test_results.csv")
            logger.info("\n✅ Test passed! Scraper is working.")
            logger.info("You're ready to run: python test_scraper.py")
        else:
            logger.error("❌ No businesses found")
            logger.info("This could mean:")
            logger.info("  1. Yellow Pages changed their HTML structure")
            logger.info("  2. The search returned no results")
            logger.info("Check STRUCTURE_NOTES.md for debugging")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        logger.info("\nTroubleshooting:")
        logger.info("  1. Check your internet connection")
        logger.info("  2. Try again (Yellow Pages might be temporarily down)")
        logger.info("  3. Check TESTING_GUIDE.md for help")

    finally:
        logger.info("\nClosing browser...")
        await scraper.close_browser()


if __name__ == "__main__":
    asyncio.run(main())

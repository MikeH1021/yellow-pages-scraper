"""
Example of using the Yellow Pages scraper with proxy rotation
Demonstrates different ways to configure proxies
"""

import asyncio
import os
from yellowpages_scraper import YellowPagesScraper
from proxy_manager import ProxyManager, Proxy, create_paid_proxy_pool


async def example_with_proxy_list():
    """Example using proxies from a file"""
    print("=" * 60)
    print("Example 1: Using proxies from file")
    print("=" * 60)

    # Load proxies from file
    proxy_manager = ProxyManager.from_file('proxies.txt', validate=True)

    # Validate proxies before using
    await proxy_manager.validate_all_proxies()

    if not proxy_manager.proxies:
        print("No working proxies found. Exiting.")
        return

    # Create scraper with proxy rotation
    scraper = YellowPagesScraper(
        headless=True,
        delay=3.0,
        proxy_manager=proxy_manager
    )

    try:
        await scraper.start_browser()

        businesses = await scraper.scrape_search(
            search_term="building supply",
            location="Miami, FL",
            max_pages=2
        )

        print(f"\nFound {len(businesses)} businesses")
        scraper.save_to_csv(businesses, "proxied_results.csv")

    finally:
        await scraper.close_browser()


async def example_with_manual_proxies():
    """Example using manually configured proxies"""
    print("\n" + "=" * 60)
    print("Example 2: Using manually configured proxies")
    print("=" * 60)

    # Manually create proxy list
    proxies = [
        Proxy(host="proxy1.example.com", port=8080),
        Proxy(host="proxy2.example.com", port=8080, username="user", password="pass"),
        Proxy(host="proxy3.example.com", port=3128),
    ]

    proxy_manager = ProxyManager(proxies, validate=False)

    scraper = YellowPagesScraper(
        headless=True,
        delay=2.0,
        proxy_manager=proxy_manager
    )

    try:
        await scraper.start_browser()

        businesses = await scraper.scrape_search(
            search_term="shutters",
            location="New York, NY",
            max_pages=1
        )

        print(f"\nFound {len(businesses)} businesses")

    finally:
        await scraper.close_browser()


async def example_with_paid_service():
    """Example using a paid proxy service"""
    print("\n" + "=" * 60)
    print("Example 3: Using paid proxy service")
    print("=" * 60)

    # Get credentials from environment variables
    proxy_username = os.getenv('PROXY_USERNAME')
    proxy_password = os.getenv('PROXY_PASSWORD')

    if not proxy_username or not proxy_password:
        print("Set PROXY_USERNAME and PROXY_PASSWORD environment variables")
        print("Example: export PROXY_USERNAME='your-username'")
        print("         export PROXY_PASSWORD='your-password'")
        return

    # Create proxy pool from paid service
    # Options: brightdata, smartproxy, oxylabs, proxyrack
    proxy_manager = create_paid_proxy_pool(
        service='smartproxy',  # Change to your service
        username=proxy_username,
        password=proxy_password,
        count=5  # Number of proxy instances
    )

    scraper = YellowPagesScraper(
        headless=True,
        delay=2.0,
        proxy_manager=proxy_manager
    )

    try:
        await scraper.start_browser()

        businesses = await scraper.scrape_search(
            search_term="lumber",
            location="Los Angeles, CA",
            max_pages=3
        )

        print(f"\nFound {len(businesses)} businesses")
        scraper.save_to_csv(businesses, "lumber_la.csv")

    finally:
        await scraper.close_browser()


async def example_without_proxies():
    """Example without proxies (may get IP banned on large scrapes)"""
    print("\n" + "=" * 60)
    print("Example 4: Without proxies (for testing)")
    print("=" * 60)

    scraper = YellowPagesScraper(
        headless=False,
        delay=3.0,
        proxy_manager=None  # No proxies
    )

    try:
        await scraper.start_browser()

        businesses = await scraper.scrape_search(
            search_term="architects",
            location="Chicago, IL",
            max_pages=1
        )

        print(f"\nFound {len(businesses)} businesses")

    finally:
        await scraper.close_browser()


async def main():
    """Run examples"""

    print("Yellow Pages Scraper - Proxy Examples\n")

    # Choose which example to run
    print("Select an example:")
    print("1. Use proxies from file (proxies.txt)")
    print("2. Use manually configured proxies")
    print("3. Use paid proxy service")
    print("4. No proxies (testing only)")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        await example_with_proxy_list()
    elif choice == "2":
        await example_with_manual_proxies()
    elif choice == "3":
        await example_with_paid_service()
    elif choice == "4":
        await example_without_proxies()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    # For non-interactive use, uncomment one of these:
    # asyncio.run(example_with_proxy_list())
    # asyncio.run(example_with_manual_proxies())
    # asyncio.run(example_with_paid_service())
    # asyncio.run(example_without_proxies())

    # Interactive mode:
    asyncio.run(main())

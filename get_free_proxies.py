"""
Fetch free proxies from public sources and save to proxies.txt
WARNING: Free proxies are unreliable - use only for testing!
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List
from proxy_manager import Proxy, ProxyManager


async def fetch_free_proxy_list() -> List[Proxy]:
    """
    Fetch free proxies from free-proxy-list.net
    Returns list of Proxy objects
    """
    proxies = []

    try:
        async with aiohttp.ClientSession() as session:
            print("Fetching proxies from free-proxy-list.net...")

            async with session.get('https://free-proxy-list.net/', timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    # Find the proxy table
                    table = soup.find('table', class_='table')
                    if table:
                        rows = table.find('tbody').find_all('tr')

                        for row in rows[:50]:  # Get first 50 proxies
                            cols = row.find_all('td')
                            if len(cols) >= 7:
                                ip = cols[0].text.strip()
                                port = cols[1].text.strip()
                                https = cols[6].text.strip()

                                # Only get HTTPS proxies
                                if https == 'yes':
                                    protocol = 'https'
                                else:
                                    protocol = 'http'

                                proxies.append(Proxy(
                                    host=ip,
                                    port=int(port),
                                    protocol=protocol
                                ))

                        print(f"✓ Found {len(proxies)} proxies from free-proxy-list.net")

    except Exception as e:
        print(f"✗ Error fetching from free-proxy-list.net: {e}")

    return proxies


async def fetch_sslproxies() -> List[Proxy]:
    """
    Fetch free SSL proxies from sslproxies.org
    Returns list of Proxy objects
    """
    proxies = []

    try:
        async with aiohttp.ClientSession() as session:
            print("Fetching proxies from sslproxies.org...")

            async with session.get('https://www.sslproxies.org/', timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    # Find the proxy table
                    table = soup.find('table', class_='table')
                    if table:
                        rows = table.find('tbody').find_all('tr')

                        for row in rows[:30]:  # Get first 30 proxies
                            cols = row.find_all('td')
                            if len(cols) >= 2:
                                ip = cols[0].text.strip()
                                port = cols[1].text.strip()

                                proxies.append(Proxy(
                                    host=ip,
                                    port=int(port),
                                    protocol='https'
                                ))

                        print(f"✓ Found {len(proxies)} proxies from sslproxies.org")

    except Exception as e:
        print(f"✗ Error fetching from sslproxies.org: {e}")

    return proxies


async def main():
    """Fetch free proxies and save to file"""

    print("=" * 60)
    print("Free Proxy Fetcher")
    print("=" * 60)
    print("\nWARNING: Free proxies are:")
    print("  - Slow and unreliable")
    print("  - May not work (60-90% failure rate)")
    print("  - Potential security risk")
    print("  - Good for testing only!")
    print("\nFor production, use paid proxies (see PROXY_GUIDE.md)")
    print("=" * 60)

    # Fetch from multiple sources
    all_proxies = []

    tasks = [
        fetch_free_proxy_list(),
        fetch_sslproxies(),
    ]

    results = await asyncio.gather(*tasks)
    for proxy_list in results:
        all_proxies.extend(proxy_list)

    print(f"\n{'='*60}")
    print(f"Total proxies fetched: {len(all_proxies)}")
    print(f"{'='*60}")

    if not all_proxies:
        print("\n❌ No proxies found. Try again later or use paid proxies.")
        return

    # Validate proxies
    print("\nValidating proxies (this may take a few minutes)...")
    proxy_manager = ProxyManager(all_proxies, validate=True)
    await proxy_manager.validate_all_proxies()

    working_proxies = proxy_manager.working_proxies

    if not working_proxies:
        print("\n❌ No working proxies found. Free proxies are unreliable.")
        print("Consider using paid proxy services (see PROXY_GUIDE.md)")
        return

    # Save to file
    print(f"\nSaving {len(working_proxies)} working proxies to proxies.txt...")

    with open('proxies.txt', 'w') as f:
        f.write("# Free proxies fetched on " +
                __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("# WARNING: Free proxies are unreliable and may stop working\n")
        f.write("# Format: host:port\n\n")

        for proxy in working_proxies:
            f.write(f"{proxy.protocol}://{proxy.host}:{proxy.port}\n")

    print(f"\n{'='*60}")
    print("✓ SUCCESS!")
    print(f"{'='*60}")
    print(f"Saved {len(working_proxies)} working proxies to proxies.txt")
    print("\nNext steps:")
    print("  1. Edit config.py and set: USE_PROXIES = True")
    print("  2. Run: python test_scraper.py")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())

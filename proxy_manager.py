"""
Proxy Manager for rotating IPs to avoid bans
Supports both free and paid proxy services
"""

import random
import asyncio
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from datetime import datetime
import aiohttp


@dataclass
class Proxy:
    """Proxy configuration with health tracking"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"

    # Health tracking
    success_count: int = 0
    fail_count: int = 0
    block_count: int = 0
    last_used: Optional[datetime] = None
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    is_blocked: bool = False

    @property
    def url(self) -> str:
        """Get proxy URL"""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"

    def to_playwright_dict(self) -> Dict:
        """Convert to Playwright proxy format"""
        proxy_dict = {
            "server": f"{self.protocol}://{self.host}:{self.port}"
        }
        if self.username and self.password:
            proxy_dict["username"] = self.username
            proxy_dict["password"] = self.password
        return proxy_dict

    def record_success(self):
        """Record a successful request"""
        self.success_count += 1
        self.last_success = datetime.now()
        self.last_used = datetime.now()

        # Reset block status if we get successful requests
        if self.success_count > self.fail_count:
            self.is_blocked = False

    def record_failure(self, is_block: bool = False):
        """Record a failed request"""
        self.fail_count += 1
        self.last_failure = datetime.now()
        self.last_used = datetime.now()

        if is_block:
            self.block_count += 1
            # Mark as blocked if we get 3+ blocks
            if self.block_count >= 3:
                self.is_blocked = True

    def get_success_rate(self) -> float:
        """Calculate success rate"""
        total = self.success_count + self.fail_count
        if total == 0:
            return 1.0
        return self.success_count / total

    def reset_stats(self):
        """Reset health statistics"""
        self.success_count = 0
        self.fail_count = 0
        self.block_count = 0
        self.is_blocked = False


class ProxyManager:
    """Manages proxy rotation"""

    def __init__(self, proxies: List[Proxy], validate: bool = False):
        """
        Initialize proxy manager

        Args:
            proxies: List of Proxy objects
            validate: Whether to validate proxies before use
        """
        self.proxies = proxies
        self.current_index = 0
        self.validate = validate
        self.working_proxies: List[Proxy] = []

    async def validate_proxy(self, proxy: Proxy) -> bool:
        """
        Validate if a proxy is working

        Args:
            proxy: Proxy to validate

        Returns:
            True if proxy works, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                proxy_url = proxy.url
                async with session.get(
                    'http://httpbin.org/ip',
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✓ Proxy {proxy.host}:{proxy.port} works (IP: {data.get('origin', 'unknown')})")
                        return True
        except Exception as e:
            print(f"✗ Proxy {proxy.host}:{proxy.port} failed: {str(e)[:50]}")
            return False

    async def validate_all_proxies(self):
        """Validate all proxies and keep only working ones"""
        print(f"Validating {len(self.proxies)} proxies...")

        tasks = [self.validate_proxy(proxy) for proxy in self.proxies]
        results = await asyncio.gather(*tasks)

        self.working_proxies = [
            proxy for proxy, is_working in zip(self.proxies, results)
            if is_working
        ]

        print(f"\n{len(self.working_proxies)}/{len(self.proxies)} proxies are working")

        if not self.working_proxies:
            print("WARNING: No working proxies found!")
        else:
            self.proxies = self.working_proxies

    def get_next_proxy(self) -> Optional[Proxy]:
        """
        Get next proxy in rotation (skips blocked proxies)

        Returns:
            Next proxy or None if no proxies available
        """
        if not self.proxies:
            return None

        # Filter out blocked proxies
        available_proxies = [p for p in self.proxies if not p.is_blocked]

        if not available_proxies:
            # All proxies are blocked, reset block status and try again
            print("⚠️ All proxies blocked, resetting block status...")
            for proxy in self.proxies:
                proxy.is_blocked = False
            available_proxies = self.proxies

        # Get next available proxy
        attempts = 0
        max_attempts = len(self.proxies)

        while attempts < max_attempts:
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)

            if not proxy.is_blocked:
                return proxy

            attempts += 1

        # Return first proxy as fallback
        return self.proxies[0] if self.proxies else None

    def get_random_proxy(self) -> Optional[Proxy]:
        """
        Get random proxy (skips blocked proxies)

        Returns:
            Random proxy or None if no proxies available
        """
        if not self.proxies:
            return None

        # Filter out blocked proxies
        available_proxies = [p for p in self.proxies if not p.is_blocked]

        if not available_proxies:
            # All proxies are blocked, use all
            available_proxies = self.proxies

        return random.choice(available_proxies)

    def get_health_report(self) -> Dict:
        """
        Get health report for all proxies

        Returns:
            Dictionary with health statistics
        """
        total_proxies = len(self.proxies)
        blocked_proxies = sum(1 for p in self.proxies if p.is_blocked)
        total_requests = sum(p.success_count + p.fail_count for p in self.proxies)
        total_success = sum(p.success_count for p in self.proxies)

        overall_success_rate = total_success / total_requests if total_requests > 0 else 0

        return {
            "total_proxies": total_proxies,
            "blocked_proxies": blocked_proxies,
            "available_proxies": total_proxies - blocked_proxies,
            "total_requests": total_requests,
            "total_success": total_success,
            "success_rate": overall_success_rate
        }

    @classmethod
    def from_file(cls, filepath: str, validate: bool = False) -> 'ProxyManager':
        """
        Create ProxyManager from a file

        File format (one per line):
            host:port
            host:port:username:password
            protocol://host:port
            protocol://username:password@host:port

        Args:
            filepath: Path to proxy list file
            validate: Whether to validate proxies

        Returns:
            ProxyManager instance
        """
        proxies = []

        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    try:
                        proxy = cls._parse_proxy_string(line)
                        if proxy:
                            proxies.append(proxy)
                    except Exception as e:
                        print(f"Error parsing proxy '{line}': {e}")

        except FileNotFoundError:
            print(f"Proxy file not found: {filepath}")

        return cls(proxies, validate)

    @staticmethod
    def _parse_proxy_string(proxy_str: str) -> Optional[Proxy]:
        """Parse proxy string into Proxy object"""

        # Remove protocol if present
        protocol = "http"
        if "://" in proxy_str:
            protocol, proxy_str = proxy_str.split("://", 1)

        # Check for username:password
        username = None
        password = None
        if "@" in proxy_str:
            auth, proxy_str = proxy_str.split("@", 1)
            if ":" in auth:
                username, password = auth.split(":", 1)

        # Parse host:port
        parts = proxy_str.split(":")
        if len(parts) < 2:
            return None

        host = parts[0]
        port = int(parts[1])

        # If username/password in parts (alternative format)
        if len(parts) == 4:
            username = parts[2]
            password = parts[3]

        return Proxy(
            host=host,
            port=port,
            username=username,
            password=password,
            protocol=protocol
        )


# Popular free proxy services (use with caution - quality varies)
class FreeProxyProviders:
    """Helper class for free proxy services"""

    @staticmethod
    async def get_free_proxy_list() -> List[Proxy]:
        """
        Fetch free proxies from various sources
        WARNING: Free proxies are unreliable and may not work

        Returns:
            List of Proxy objects
        """
        # This is a placeholder - you would need to implement actual fetching
        # from free proxy sites like:
        # - https://www.proxy-list.download/
        # - https://free-proxy-list.net/
        # - https://www.sslproxies.org/

        print("WARNING: Free proxies are slow and unreliable")
        print("Consider using paid proxy services for production use")
        return []


# Paid proxy service configurations
PROXY_SERVICE_CONFIGS = {
    "brightdata": {
        # BrightData (formerly Luminati) - High quality residential proxies
        # Get from: https://brightdata.com/
        "host": "brd.superproxy.io",
        "port": 22225,
        # Set in environment or config: username="brd-customer-{customer_id}-zone-{zone_name}"
    },
    "smartproxy": {
        # SmartProxy - Good quality residential proxies
        # Get from: https://smartproxy.com/
        "host": "gate.smartproxy.com",
        "port": 7000,
        # Set in environment: username, password
    },
    "oxylabs": {
        # Oxylabs - Enterprise proxy service
        # Get from: https://oxylabs.io/
        "host": "pr.oxylabs.io",
        "port": 7777,
        # Set in environment: username="customer-{customer_id}", password
    },
    "proxyrack": {
        # ProxyRack - Affordable proxy service
        # Get from: https://www.proxyrack.com/
        "host": "megaproxy.rotating.proxyrack.net",
        "port": 222,
        # Set in environment: username, password
    }
}


def create_paid_proxy_pool(
    service: str,
    username: str,
    password: str,
    count: int = 10
) -> ProxyManager:
    """
    Create a proxy pool from a paid service

    Args:
        service: Service name (brightdata, smartproxy, oxylabs, proxyrack)
        username: Service username
        password: Service password
        count: Number of proxy instances to create

    Returns:
        ProxyManager with proxy pool
    """
    if service not in PROXY_SERVICE_CONFIGS:
        raise ValueError(f"Unknown service: {service}. Available: {list(PROXY_SERVICE_CONFIGS.keys())}")

    config = PROXY_SERVICE_CONFIGS[service]

    # For rotating proxies, create multiple instances
    # (most paid services handle rotation server-side)
    proxies = [
        Proxy(
            host=config["host"],
            port=config["port"],
            username=username,
            password=password,
            protocol="http"
        )
        for _ in range(count)
    ]

    return ProxyManager(proxies, validate=False)

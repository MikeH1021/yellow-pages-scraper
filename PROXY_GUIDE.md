# Proxy Setup Guide

This guide explains how to set up proxies to avoid IP bans when scraping Yellow Pages.

## Why Use Proxies?

When scraping large amounts of data, websites may:
1. **Rate limit** your requests
2. **Block your IP** temporarily or permanently
3. **Return CAPTCHA challenges**
4. **Serve different content** to suspected bots

Proxies solve this by:
- Rotating your IP address
- Distributing requests across multiple IPs
- Making it harder for sites to detect scraping

## Proxy Options

### Option 1: Free Proxies (Not Recommended for Production)

**Pros:**
- Free
- Easy to find

**Cons:**
- Very unreliable (60-90% don't work)
- Slow speeds
- Security risks (some log your traffic)
- Frequently blocked
- May inject ads or malware

**When to use:** Testing only, not for production scraping

**How to get free proxies:**
1. Visit free proxy sites (at your own risk):
   - https://free-proxy-list.net/
   - https://www.sslproxies.org/
   - https://www.proxy-list.download/

2. Copy proxy addresses to `proxies.txt`:
   ```
   123.45.67.89:8080
   98.76.54.32:3128
   ```

3. Enable validation in `config.py`:
   ```python
   VALIDATE_PROXIES = True  # Filters out non-working proxies
   ```

### Option 2: Paid Proxy Services (Recommended)

**Pros:**
- High reliability (99%+ uptime)
- Fast speeds
- Good customer support
- Rotating IPs automatically
- Residential IPs (harder to detect)

**Cons:**
- Cost money ($30-$500/month typically)

**Recommended Services:**

#### 1. SmartProxy (Best for beginners)
- **Cost:** ~$50/month for 5GB
- **Features:** Residential IPs, 40M+ IP pool, good support
- **Website:** https://smartproxy.com/
- **Setup:**
  ```bash
  export PROXY_SERVICE="smartproxy"
  export PROXY_USERNAME="your-username"
  export PROXY_PASSWORD="your-password"
  ```

#### 2. BrightData (formerly Luminati) (Best for large-scale)
- **Cost:** ~$500/month for 20GB
- **Features:** Largest IP pool (72M+), best quality, enterprise-grade
- **Website:** https://brightdata.com/
- **Setup:**
  ```bash
  export PROXY_SERVICE="brightdata"
  export PROXY_USERNAME="brd-customer-{customer_id}-zone-{zone_name}"
  export PROXY_PASSWORD="your-password"
  ```

#### 3. Oxylabs (Best for enterprise)
- **Cost:** ~$300/month for 20GB
- **Features:** High-quality residential IPs, great compliance
- **Website:** https://oxylabs.io/
- **Setup:**
  ```bash
  export PROXY_SERVICE="oxylabs"
  export PROXY_USERNAME="customer-{customer_id}"
  export PROXY_PASSWORD="your-password"
  ```

#### 4. ProxyRack (Best budget option)
- **Cost:** ~$30/month for 20GB
- **Features:** Decent quality, affordable
- **Website:** https://www.proxyrack.com/
- **Setup:**
  ```bash
  export PROXY_SERVICE="proxyrack"
  export PROXY_USERNAME="your-username"
  export PROXY_PASSWORD="your-password"
  ```

## Setup Instructions

### Method 1: Using Proxy List File

1. **Create `proxies.txt` file:**
   ```
   # Format: host:port or host:port:username:password
   proxy1.example.com:8080
   proxy2.example.com:8080:myuser:mypass
   http://username:password@proxy3.example.com:3128
   ```

2. **Edit `config.py`:**
   ```python
   USE_PROXIES = True
   PROXY_FILE = "proxies.txt"
   VALIDATE_PROXIES = True
   ```

3. **Run the scraper:**
   ```bash
   python run_scraper.py
   ```

### Method 2: Using Paid Proxy Service

1. **Sign up for a proxy service** (e.g., SmartProxy)

2. **Set environment variables:**
   ```bash
   # macOS/Linux
   export PROXY_SERVICE="smartproxy"
   export PROXY_USERNAME="your-username"
   export PROXY_PASSWORD="your-password"

   # Windows PowerShell
   $env:PROXY_SERVICE="smartproxy"
   $env:PROXY_USERNAME="your-username"
   $env:PROXY_PASSWORD="your-password"
   ```

3. **Edit `config.py`:**
   ```python
   USE_PAID_PROXY_SERVICE = True
   ```

4. **Run the scraper:**
   ```bash
   python run_scraper.py
   ```

### Method 3: Programmatic Setup

Create a custom script:

```python
import asyncio
from yellowpages_scraper import YellowPagesScraper
from proxy_manager import ProxyManager, Proxy

async def main():
    # Option A: From file
    proxy_manager = ProxyManager.from_file('proxies.txt', validate=True)
    await proxy_manager.validate_all_proxies()

    # Option B: Manual list
    proxies = [
        Proxy("proxy1.com", 8080, "user", "pass"),
        Proxy("proxy2.com", 8080),
    ]
    proxy_manager = ProxyManager(proxies)

    # Option C: Paid service
    from proxy_manager import create_paid_proxy_pool
    proxy_manager = create_paid_proxy_pool(
        service='smartproxy',
        username='your-username',
        password='your-password',
        count=5
    )

    # Use with scraper
    scraper = YellowPagesScraper(
        headless=True,
        delay=3.0,
        proxy_manager=proxy_manager
    )

    await scraper.start_browser()
    # ... your scraping code ...
    await scraper.close_browser()

asyncio.run(main())
```

## Testing Your Proxies

Run the proxy validation:

```python
python -c "
import asyncio
from proxy_manager import ProxyManager

async def test():
    pm = ProxyManager.from_file('proxies.txt', validate=True)
    await pm.validate_all_proxies()

asyncio.run(test())
"
```

Or use the example script:

```bash
python example_with_proxies.py
```

## Best Practices

### 1. Start Small
- Test with 1-2 pages first
- Verify proxies work before large scrapes
- Monitor for blocks or CAPTCHAs

### 2. Increase Delays
- Use longer delays with proxies: `DELAY_BETWEEN_PAGES = 3.0` or higher
- Mimics human behavior
- Reduces detection risk

### 3. Rotate Smartly
- Don't rotate on every request (suspicious)
- Rotate per search category or location
- Keep the same IP for a full page/search

### 4. Monitor Your Proxies
- Check success rates
- Replace non-working proxies
- Watch for speed degradation

### 5. Respect Rate Limits
- Even with proxies, don't hammer the site
- 2-5 second delays minimum
- Consider scraping during off-peak hours

### 6. Use Residential Proxies
- Harder to detect than datacenter proxies
- More expensive but worth it
- Yellow Pages likely blocks datacenter IPs

## Troubleshooting

### "No working proxies found"
- Proxies in file are incorrect or dead
- Try different proxy source
- Reduce `VALIDATE_PROXIES` timeout (edit `proxy_manager.py`)

### "403 Forbidden" with proxies
- Proxies are detected as proxies
- Try residential proxies instead
- Increase delay between requests
- Use better user agent rotation

### Slow scraping
- Free proxies are slow
- Reduce `VALIDATE_PROXIES` timeout
- Use paid proxies
- Decrease `MAX_PAGES_PER_SEARCH`

### Still getting blocked
1. Increase `DELAY_BETWEEN_PAGES` to 5-10 seconds
2. Run in non-headless mode: `HEADLESS_MODE = False`
3. Add random delays:
   ```python
   import random
   delay = random.uniform(3.0, 7.0)
   ```
4. Rotate user agents
5. Use higher-quality residential proxies

## Cost Estimates

### For scraping 1000 businesses:

**Without proxies:**
- Cost: Free
- Risk: High (likely to get blocked)
- Speed: Fast (until blocked)

**With free proxies:**
- Cost: Free
- Risk: Medium (unreliable)
- Speed: Slow (many timeouts)
- Success rate: 50-70%

**With paid proxies (SmartProxy):**
- Cost: ~$50/month
- Risk: Low
- Speed: Fast
- Success rate: 95%+

### For scraping 10,000+ businesses:

**Recommended:** Paid proxy service with residential IPs
- SmartProxy: ~$100-200/month
- BrightData: ~$500/month
- Best success rate and support

## Security Notes

1. **Never commit credentials:**
   - Add `.env` to `.gitignore`
   - Use environment variables
   - Don't hardcode in scripts

2. **Proxy security:**
   - Free proxies may log traffic
   - Use HTTPS when possible
   - Don't send sensitive data through proxies

3. **Legal considerations:**
   - Check Yellow Pages Terms of Service
   - Respect robots.txt
   - Don't resell scraped data without permission

## Support

If you have issues:

1. Check the `STRUCTURE_NOTES.md` for HTML changes
2. Review `example_with_proxies.py` for working examples
3. Enable verbose output to debug
4. Contact your proxy provider's support

---

**Last Updated:** January 2026

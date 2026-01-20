# How to Detect When Proxies Get Blocked

## Overview

Proxies can get blocked by websites using various anti-scraping measures. This guide explains how to detect blocks and what to do about them.

---

## Detection Methods

### 1. HTTP Status Codes (Most Common)

**403 Forbidden**
```
Status: 403
Message: "Access Denied" or "Forbidden"
```
- Website is explicitly blocking your IP
- Most common block indicator
- Usually means the proxy IP is flagged

**429 Too Many Requests**
```
Status: 429
Message: "Too Many Requests" or "Rate Limit Exceeded"
```
- You're making requests too fast
- Temporary rate limit (usually clears in 15-60 minutes)
- Not necessarily a permanent block

**503 Service Unavailable**
```
Status: 503
Message: "Service Temporarily Unavailable"
```
- Could be a block or actual server issue
- Check if pattern repeats across proxies
- If only one proxy gets 503s, it's likely blocked

### 2. CAPTCHA Detection

**Signs of CAPTCHA:**
```html
<!-- Page contains CAPTCHA elements -->
<div class="g-recaptcha">
<iframe src="https://www.google.com/recaptcha/">
<form action="/captcha">
```

**How to detect:**
- Check page HTML for "captcha" or "recaptcha" keywords
- Look for specific CAPTCHA service domains
- Monitor page titles (often contain "Verify" or "Security Check")

```python
if "captcha" in page_content.lower():
    # Proxy is blocked
    proxy.record_failure(is_block=True)
```

### 3. Timeout Patterns

**Connection Timeouts:**
- Proxy connects but never receives response
- Request hangs indefinitely
- Usually indicates proxy is being silently blocked

**Typical timeout thresholds:**
- Normal response: < 5 seconds
- Slow response: 5-15 seconds
- Timeout/Block: > 15 seconds

```python
try:
    response = await page.goto(url, timeout=15000)  # 15 sec timeout
except TimeoutError:
    # Likely blocked
    proxy.record_failure(is_block=True)
```

### 4. Response Content Analysis

**Empty or Minimal Content:**
```html
<!-- Blocked page often returns minimal HTML -->
<html><body>Access Denied</body></html>
```

**Detection method:**
- Expected page size: > 10KB
- Blocked page: < 1KB
- Check for expected content markers

```python
if len(page_content) < 1000:
    # Suspiciously small response
    if "access denied" in page_content.lower():
        proxy.record_failure(is_block=True)
```

### 5. JavaScript Challenge Pages

**Cloudflare, DataDome, PerimeterX:**
```html
<!-- Challenge pages contain specific markers -->
<title>Just a moment...</title>
<script src="challenge-platform.js"></script>
```

**Detection:**
- Look for challenge page keywords
- Check for JavaScript verification scripts
- Monitor redirect patterns

### 6. Success Rate Monitoring

**Track proxy performance over time:**
```python
success_rate = proxy.success_count / (proxy.success_count + proxy.fail_count)

if success_rate < 0.3:  # Less than 30% success
    proxy.is_blocked = True
```

**Thresholds:**
- Healthy proxy: > 70% success rate
- Warning: 40-70% success rate
- Blocked: < 30% success rate

---

## Implementation in Your Scraper

### Enhanced Proxy Class (Already Implemented)

```python
@dataclass
class Proxy:
    # Health tracking
    success_count: int = 0
    fail_count: int = 0
    block_count: int = 0
    is_blocked: bool = False

    def record_success(self):
        self.success_count += 1
        # Reset block status if recovering
        if self.success_count > self.fail_count:
            self.is_blocked = False

    def record_failure(self, is_block: bool = False):
        self.fail_count += 1
        if is_block:
            self.block_count += 1
            # Mark as blocked after 3+ blocks
            if self.block_count >= 3:
                self.is_blocked = True
```

### Integration with Scraper

**In yellowpages_scraper.py:**
```python
async def scrape_page(self, url):
    try:
        response = await self.page.goto(url)

        # Check for blocks
        if response.status == 403:
            logger.error("🚫 BLOCKED (403)")
            if self.proxy_manager:
                current_proxy.record_failure(is_block=True)
            return []

        elif response.status == 429:
            logger.error("🚫 RATE LIMITED (429)")
            if self.proxy_manager:
                current_proxy.record_failure(is_block=True)
            return []

        # Check for CAPTCHA
        content = await self.page.content()
        if "captcha" in content.lower():
            logger.error("🚫 CAPTCHA DETECTED")
            if self.proxy_manager:
                current_proxy.record_failure(is_block=True)
            return []

        # Success
        if self.proxy_manager:
            current_proxy.record_success()

        return self.extract_data()

    except TimeoutError:
        logger.error("🚫 TIMEOUT")
        if self.proxy_manager:
            current_proxy.record_failure(is_block=True)
        return []
```

---

## What to Do When Proxies Get Blocked

### 1. Automatic Rotation (Already Implemented)

The proxy manager automatically skips blocked proxies:
```python
def get_next_proxy(self):
    # Filter out blocked proxies
    available_proxies = [p for p in self.proxies if not p.is_blocked]

    if not available_proxies:
        # All blocked - reset and try again
        for proxy in self.proxies:
            proxy.is_blocked = False
```

### 2. Increase Delays

```python
# In config
DELAY_BETWEEN_PAGES = 5.0  # Increase from 3s to 5s
```

### 3. Reduce Max Pages

```python
# In config
MAX_PAGES_PER_SEARCH = 5  # Reduce from 10 to 5
```

### 4. Add More Proxies

- Purchase more proxies from Webshare
- Upload new proxy file through web UI
- Automatically distributes load

### 5. Reset Proxy Stats

If proxies were temporarily blocked and you want to retry:
```python
for proxy in proxy_manager.proxies:
    proxy.reset_stats()
```

### 6. Switch Proxy Provider

If Webshare proxies are getting blocked:
- Try SmartProxy
- Try BrightData (most expensive but most reliable)
- Try Oxylabs

---

## Monitoring in Web UI

The web interface shows real-time proxy health:

**Proxy Status Table:**
| Proxy | Success Rate | Status | Last Used |
|-------|--------------|--------|-----------|
| 142.111.48.253:7030 | 87% | HEALTHY | 14:32:15 |
| 23.95.150.145:6114 | 45% | WARNING | 14:32:10 |
| 198.23.239.134:6540 | 12% | BLOCKED | 14:31:55 |

**Status Indicators:**
- 🟢 **HEALTHY** - Success rate > 70%
- 🟡 **WARNING** - Success rate 40-70%
- 🔴 **BLOCKED** - Success rate < 40% or marked as blocked

---

## Best Practices

### 1. Start Conservative
```python
DELAY_BETWEEN_PAGES = 5.0  # Start slow
MAX_PAGES_PER_SEARCH = 5   # Limit pages initially
```

### 2. Monitor Closely
- Watch live logs in web UI
- Check proxy health every 30 seconds
- Stop if > 50% of proxies get blocked

### 3. Respect Rate Limits
- If you see 429 errors, increase delays
- Don't try to "work around" rate limits
- Patience = better data quality

### 4. Use Quality Proxies
**Proxy Quality Hierarchy:**
1. Residential proxies (best - what you have)
2. Mobile proxies (excellent but expensive)
3. Datacenter proxies (cheap but easily detected)

**Your Webshare proxies are residential = good choice**

### 5. Rotate Aggressively
```python
# Switch proxy after EVERY search (not every page)
for search in searches:
    proxy = proxy_manager.get_next_proxy()
    await scraper.switch_proxy(proxy)
    await scraper.scrape_search(...)
```

---

## Common Block Patterns

### Pattern 1: Immediate 403
```
Request 1: 403 Forbidden
Request 2: 403 Forbidden
Request 3: 403 Forbidden
```
**Diagnosis:** Proxy IP is already blacklisted
**Solution:** Skip this proxy, mark as blocked

### Pattern 2: Gradual Degradation
```
Requests 1-10: 200 OK
Requests 11-15: Some 200, some 429
Requests 16+: All 403
```
**Diagnosis:** Rate limit exceeded, then banned
**Solution:** Slower delays, rotate more frequently

### Pattern 3: CAPTCHA After N Requests
```
Requests 1-20: 200 OK
Request 21: CAPTCHA page
```
**Diagnosis:** Behavior-based detection
**Solution:** More realistic delays, vary request timing

### Pattern 4: Random Blocks
```
Request 5: 403
Request 6: 200 OK
Request 12: 403
Request 13: 200 OK
```
**Diagnosis:** Probabilistic blocking or shared IP
**Solution:** Keep using, mark failures but don't block proxy

---

## Web UI Real-Time Detection

The web interface automatically detects blocks:

**Live Logs Show:**
```
14:32:10 🚫 BLOCKED (403) - Proxy 142.111.48.253
14:32:15 ⚠️ Switching to next proxy
14:32:16 ✅ Using proxy 23.95.150.145
14:32:20 ✓ Found 34 businesses
```

**Proxy Health Updates Every 5 Seconds:**
- Success rate recalculated
- Block status updated
- Color-coded health indicators

**Auto-Actions:**
- Blocked proxies automatically skipped
- Scraper switches to next available proxy
- Warning if all proxies blocked

---

## Emergency Procedures

### If All Proxies Get Blocked

**Option 1: Wait it out (24-48 hours)**
```python
# Blocks often expire after 24-48 hours
# Come back tomorrow and reset stats
```

**Option 2: Buy new proxies**
```
1. Purchase new batch from Webshare
2. Upload through web UI
3. Resume scraping
```

**Option 3: Switch to paid rotating service**
```python
# Use SmartProxy or BrightData
# They handle IP rotation automatically
# More expensive but more reliable
```

### If Website Updates Anti-Scraping

**Indicators:**
- Sudden 100% block rate
- New CAPTCHA type
- Different page structure

**Actions:**
1. Check if Yellow Pages updated their site
2. Update scraper HTML selectors
3. Increase delays significantly
4. Consider using more premium proxies

---

## Summary

### How to Know Proxy is Blocked

✅ **Definite Block:**
- HTTP 403 Forbidden
- CAPTCHA page appears
- 3+ consecutive failures
- Success rate < 30%

⚠️ **Possible Block:**
- HTTP 429 Rate Limit
- Timeouts > 15 seconds
- Suspiciously small responses
- HTTP 503 errors

### What Scraper Does Automatically

1. Detects 403/429/503 status codes
2. Records failures on proxy object
3. Marks proxy as blocked after 3 failures
4. Automatically skips blocked proxies
5. Rotates to next available proxy
6. Resets block status if proxy recovers

### What You Should Monitor

1. Live logs for 🚫 block indicators
2. Proxy health table (success rates)
3. Overall scraping progress
4. Number of available vs. blocked proxies

### When to Take Action

- **> 50% proxies blocked:** Increase delays or stop
- **All proxies blocked:** Buy more or wait 24-48 hours
- **Consistent 429s:** Increase `DELAY_BETWEEN_PAGES`
- **No blocks:** You're good, keep going!

---

**The web UI handles most of this automatically. Just watch the logs and proxy health table!**

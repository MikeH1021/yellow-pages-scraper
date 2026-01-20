# Proxy Buying Guide - What Should You Buy?

Complete guide to choosing the right proxies for Yellow Pages scraping.

## 🎯 Quick Answer

**For Yellow Pages scraping, buy RESIDENTIAL PROXIES**

Best choice: **SmartProxy or Bright Data** ($50-100/month)

---

## 📊 Types of Proxies

### 1. Datacenter Proxies ❌ (NOT Recommended)

**What they are:**
- Come from data centers (AWS, Digital Ocean, etc.)
- Easy to detect
- Cheap but obvious

**Pros:**
- ✅ Very cheap ($5-20/month)
- ✅ Very fast
- ✅ Unlimited bandwidth

**Cons:**
- ❌ Yellow Pages WILL block them
- ❌ Easy to detect as proxies
- ❌ Not suitable for scraping

**Verdict:** Don't buy these for Yellow Pages

---

### 2. Residential Proxies ✅ (RECOMMENDED)

**What they are:**
- Real IP addresses from real homes/devices
- Look like regular users
- Hard to detect and block

**Pros:**
- ✅ Yellow Pages can't tell it's a proxy
- ✅ Very high success rate (95%+)
- ✅ Won't get blocked
- ✅ Rotate automatically

**Cons:**
- ❌ More expensive ($50-500/month)
- ❌ Slower than datacenter
- ❌ Bandwidth limited

**Verdict:** This is what you need ⭐

---

### 3. Mobile Proxies (Overkill)

**What they are:**
- IP addresses from mobile carriers (4G/5G)
- Most expensive
- Hardest to detect

**Verdict:** Too expensive for this project ($100-300/month)

---

## 💰 Recommended Services

### 🥇 #1 SmartProxy (BEST FOR BEGINNERS)

**Why I recommend it:**
- ✅ Easiest to set up
- ✅ Great documentation
- ✅ Good support
- ✅ Affordable pricing
- ✅ 40M+ residential IPs

**Pricing:**
- **5GB:** $50/month ($10/GB)
- **10GB:** $90/month ($9/GB)
- **25GB:** $200/month ($8/GB)

**How much do you need?**
- Top 100 cities = ~500 searches
- ~50MB per search = 25GB total
- **Recommendation:** 25GB plan ($200) for full scrape
- **Or:** 10GB plan ($90) + careful monitoring

**Setup:**
```python
PROXY_SERVICE = "smartproxy"
PROXY_USERNAME = "your_username"
PROXY_PASSWORD = "your_password"
```

**Signup:** https://smartproxy.com/

---

### 🥈 #2 Bright Data (BEST QUALITY)

**Formerly Luminati - the gold standard**

**Why it's great:**
- ✅ Best quality (72M+ IPs)
- ✅ Most reliable
- ✅ Enterprise-grade
- ✅ Excellent compliance tools

**Pricing:**
- **20GB:** $500/month ($25/GB)
- **100GB:** $2,000/month ($20/GB)

**Verdict:** Best but expensive. Worth it if:
- You're scraping regularly
- You need guaranteed success
- Budget isn't a concern

**Setup:**
```python
PROXY_SERVICE = "brightdata"
PROXY_USERNAME = "brd-customer-{id}-zone-{zone}"
PROXY_PASSWORD = "your_password"
```

**Signup:** https://brightdata.com/

---

### 🥉 #3 Oxylabs (ENTERPRISE)

**Professional scraping service**

**Pricing:**
- **20GB:** $300/month ($15/GB)
- **100GB:** $1,200/month ($12/GB)

**Verdict:** Good middle ground, professional features

**Signup:** https://oxylabs.io/

---

### Budget Option: ProxyRack

**Cheapest residential proxies**

**Pricing:**
- **20GB:** $65/month ($3.25/GB)
- **100GB:** $250/month ($2.50/GB)

**Pros:**
- ✅ Very affordable
- ✅ Works for Yellow Pages

**Cons:**
- ❌ Lower quality than others
- ❌ Smaller IP pool
- ❌ Less reliable support

**Verdict:** Good if budget is tight

**Signup:** https://www.proxyrack.com/

---

## 🎯 My Specific Recommendation

### For Your Project (Top 100 Cities):

**Best Choice: SmartProxy 25GB Plan - $200**

**Why?**
- ✓ Enough bandwidth for full scrape
- ✓ High quality residential IPs
- ✓ Easy setup
- ✓ Good support
- ✓ One payment covers everything

**Alternative: SmartProxy 10GB Plan - $90**
- Run Top 50 cities first (uses ~12GB)
- See if you need more
- Upgrade if needed

---

## 📐 How Much Bandwidth Do You Need?

### Calculation:

**Per page:**
- HTML + images: ~100KB
- Average: 100KB per page

**Per search:**
- 10 pages × 100KB = 1MB
- With overhead: ~5MB

**Top 100 cities:**
- 100 cities × 5 categories = 500 searches
- 500 × 5MB = 2.5GB minimum
- **Safe estimate:** 5-10GB

**Actually, data shows:**
- Yellow Pages pages are ~500KB-1MB each
- With all assets: ~50MB per search
- **Realistic need:** 25GB for Top 100

**Recommendations by scope:**
- Top 25 cities: 5-10GB
- Top 50 cities: 10-15GB
- Top 100 cities: 20-30GB
- Top 200 cities: 40-60GB
- All 455 cities: 100GB+

---

## 💳 Cost-Benefit Analysis

### SmartProxy Example (Top 100 Cities):

**Investment:**
- SmartProxy 25GB: $200

**Return:**
- ~20,000 businesses
- Cost per business: $0.01

**Alternative (buy less):**
- SmartProxy 10GB: $90
- Scrape Top 50 cities
- Get ~10,000 businesses
- Cost per business: $0.009

---

## 🚀 What I'd Do

**If I were you:**

### Option 1: Conservative Approach

**Day 1:**
- Buy SmartProxy 10GB ($90)
- Scrape Top 50 cities
- Get 10,000 businesses
- See if that's enough

**Day 2 (if needed):**
- Buy another 10GB or upgrade
- Scrape cities 51-100
- Get another 10,000

**Total cost:** $90-180
**Total businesses:** 10,000-20,000

### Option 2: Go Big

**Day 1:**
- Buy SmartProxy 25GB ($200)
- Scrape all Top 100 cities
- Get 20,000 businesses
- Done!

**Total cost:** $200
**Total businesses:** ~20,000

**My pick:** Option 1 (start with 10GB)

---

## 🔧 Setup Instructions

### SmartProxy Setup (Recommended):

**1. Sign up:**
- Go to https://smartproxy.com/
- Create account
- Choose "Residential Proxies"
- Select plan (10GB or 25GB)

**2. Get credentials:**
- Dashboard → Residential Proxies
- Copy username (looks like: `user-USERNAME-country-us`)
- Copy password

**3. Configure scraper:**
```bash
# Set environment variables
export PROXY_SERVICE="smartproxy"
export PROXY_USERNAME="user-USERNAME-country-us"
export PROXY_PASSWORD="your_password"

# Or edit config_top_cities.py:
USE_PAID_PROXY_SERVICE = True
# Uncomment and set:
# PROXY_SERVICE = "smartproxy"
```

**4. Run:**
```bash
python run_top_cities.py
```

---

## ⚠️ Important Notes

### Free Trials:
- SmartProxy: No free trial, but 3-day money back
- Bright Data: $1 trial available
- Oxylabs: Contact for trial

### Bandwidth Monitoring:
- SmartProxy shows usage in dashboard
- You'll get email alerts at 80%, 90%
- Can upgrade mid-scrape if needed

### Session Management:
- Most services rotate IPs automatically
- SmartProxy rotates every request
- You don't need to manage this

### Country Targeting:
- Use US IPs only (country-us)
- Cheaper than worldwide
- Makes sense for US-based Yellow Pages

---

## 🎓 Pro Tips

### 1. Start Small
Don't buy 100GB right away. Start with 10GB, see how it goes.

### 2. Monitor Usage
Check dashboard after first 50 searches to estimate total need.

### 3. Sticky Sessions
Not needed for Yellow Pages - use rotating IPs.

### 4. IP Quality
Yellow Pages doesn't check IP reputation heavily. Mid-tier residential works fine.

### 5. Whitelist IPs
Not needed - use username/password auth.

---

## ❓ FAQ

**Q: Can I use free proxies?**
A: For testing only. Won't work for 500 searches.

**Q: Do I need mobile proxies?**
A: No, residential is enough.

**Q: What about datacenter proxies?**
A: They'll get blocked immediately by Yellow Pages.

**Q: How long does bandwidth last?**
A: Depends on usage. 10GB typically = 200-300 searches for us.

**Q: Can I pause and resume?**
A: Yes! The scraper saves checkpoints every 25 searches.

**Q: What if I run out mid-scrape?**
A: Buy more bandwidth, update credentials, resume scraping.

**Q: Refund policy?**
A: SmartProxy: 3 days, Bright Data: 7 days (check terms)

---

## 🎯 Final Recommendation

**For Top 100 Cities Yellow Pages Scraping:**

### Best Value: SmartProxy

**Plan:** Start with 10GB ($90)
- Scrape Top 50 cities
- See if you need more
- Upgrade if necessary

**Why?**
- ✓ Affordable test
- ✓ Easy to upgrade
- ✓ Low risk
- ✓ Good quality

**Upgrade to 25GB ($200) if:**
- Top 50 isn't enough coverage
- You want all 100 cities in one go
- You plan to scrape regularly

---

## 📞 Ready to Buy?

### Step-by-Step:

**1. Go to SmartProxy:**
https://smartproxy.com/proxies/residential-proxies

**2. Click "Get Started"**

**3. Choose plan:**
- 5GB ($50) - Too small
- **10GB ($90) - Good start** ⭐
- 25GB ($200) - Full coverage

**4. Complete payment**

**5. Get credentials from dashboard**

**6. Run:**
```bash
export PROXY_SERVICE="smartproxy"
export PROXY_USERNAME="your-username"
export PROXY_PASSWORD="your-password"

python run_top_cities.py
```

**Done!** 🚀

---

**Bottom line:** Buy SmartProxy 10GB for $90. Start scraping Top 50 cities. Upgrade if you need more. Simple!

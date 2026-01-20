# Strategy Comparison Guide

Quick comparison of different scraping approaches.

## 📊 Quick Comparison Table

| Strategy | Searches | Est. Time | Proxies? | Coverage | Best For |
|----------|----------|-----------|----------|----------|----------|
| **Nationwide** | 5 | 5 min | Optional | ~1,000 | Quick test |
| **Top 10 Cities** | 50 | 1 hour | Recommended | ~3,000 | Pilot run |
| **Top 25 Cities** | 125 | 2.5 hours | Required | ~7,500 | Good coverage |
| **Top 50 Cities** | 250 | 5 hours | Required | ~15,000 | Best coverage |
| **All States** | 190 | 8 hours | Required | ~20,000 | Maximum data |

*Assumes 5 categories, 10 pages per search, 6 seconds per page*

## 🎯 Recommended: Top 25 Cities

**Best balance of coverage vs. effort**

### Configuration
```python
# Use this file
python run_top_cities.py
```

### What You Get
- 25 major cities × 5 categories = 125 searches
- ~7,500-10,000 businesses
- 2.5 hours total time
- Good geographic coverage

### Cost
- Free proxies: $0 (may get blocked)
- Paid proxies: $50-100/month

## 📋 Strategy Breakdown

### 1. Nationwide Search

**Command:**
```bash
python run_scraper.py  # With default config.py
```

**Config:**
```python
SEARCH_CATEGORIES = [
    {"term": "building supply", "location": "United States"},
    {"term": "shutters", "location": "United States"},
    # ... 3 more
]
```

**Pros:**
- ✅ Fastest (5 minutes)
- ✅ Simple setup
- ✅ No proxies needed
- ✅ Good for testing

**Cons:**
- ❌ Limited results (~200 per category)
- ❌ Yellow Pages caps nationwide searches
- ❌ May miss smaller businesses
- ❌ Can't target specific regions

**Results:**
- Expected: 1,000-1,500 businesses total
- Quality: Major/well-known businesses only

**When to use:** Quick test, proof of concept

---

### 2. Top 10 Cities

**Command:**
```bash
# Edit config_top_cities.py
CITY_LIST = TOP_10_CITIES

python run_top_cities.py
```

**Cities:**
New York, Chicago, Houston, Philadelphia, San Antonio, Dallas, Austin, Jacksonville, Fort Worth, Columbus

**Pros:**
- ✅ Fast (1 hour)
- ✅ Targets major metros
- ✅ More complete than nationwide
- ✅ Good for pilot testing

**Cons:**
- ❌ Misses medium/small cities
- ❌ Still limited coverage

**Results:**
- Expected: 2,500-4,000 businesses
- Coverage: ~40% of total market

**When to use:** Pilot run to test workflow

---

### 3. Top 25 Cities ⭐ RECOMMENDED

**Command:**
```bash
# Default in config_top_cities.py
python run_top_cities.py
```

**Cities:**
All top 10 + Tampa, Miami, Atlanta, Orlando, Nashville, Charlotte, Boston, and more

**Pros:**
- ✅ Excellent coverage (~70% of market)
- ✅ Reasonable time (2.5 hours)
- ✅ Targets high-business areas
- ✅ Manageable with free proxies

**Cons:**
- ❌ Requires proxies
- ❌ Misses rural areas
- ❌ Takes a few hours

**Results:**
- Expected: 7,500-12,000 businesses
- Coverage: ~70% of total market

**When to use:** Production scraping, best ROI

---

### 4. Top 50 Cities

**Command:**
```bash
# Edit config_top_cities.py
CITY_LIST = TOP_CITIES_EASTERN

python run_top_cities.py
```

**Pros:**
- ✅ Very comprehensive (~85% coverage)
- ✅ Includes medium-sized cities
- ✅ Still faster than state-by-state

**Cons:**
- ❌ Takes 5 hours
- ❌ Requires good proxies
- ❌ More prone to blocks

**Results:**
- Expected: 15,000-20,000 businesses
- Coverage: ~85% of total market

**When to use:** Maximum coverage needed

---

### 5. State-by-State

**Command:**
```bash
# Edit config.py
SEARCH_CATEGORIES = [
    {"term": "building supply", "location": state}
    for state in EASTERN_STATES
]
```

**Pros:**
- ✅ Most complete (95%+ coverage)
- ✅ Includes rural businesses
- ✅ Easy to track progress

**Cons:**
- ❌ Takes 8+ hours
- ❌ Requires paid proxies
- ❌ Many duplicates
- ❌ More requests = more blocks

**Results:**
- Expected: 20,000-30,000 businesses
- Coverage: ~95% of total market

**When to use:** Need absolutely every business

---

## 💰 Cost Comparison

### Free Proxies
- **Cost:** $0
- **Reliability:** 40-60%
- **Speed:** Slow
- **Best for:** Top 10-25 cities, testing
- **Risk:** May get blocked mid-scrape

### Paid Proxies
- **Cost:** $50-100/month
- **Reliability:** 95%+
- **Speed:** Fast
- **Best for:** Top 25+ cities, production
- **Risk:** Very low

### Cost-Benefit Analysis

**Top 10 Cities:**
- Free proxies: OK
- Worth: $0

**Top 25 Cities:**
- Free proxies: Risky
- Paid proxies: Recommended ($50)
- Worth: ~10,000 businesses for $50 = $0.005/business

**Top 50 Cities:**
- Paid proxies: Required ($100)
- Worth: ~18,000 businesses for $100 = $0.0055/business

**State-by-State:**
- Paid proxies: Required ($100+)
- Worth: ~25,000 businesses for $100 = $0.004/business

## ⏱️ Time Estimates

### Per Page: 6 seconds
- 3s delay
- 2-3s load time

### Top 10 Cities:
- 10 cities × 5 categories × 10 pages × 6s = 50 minutes
- Plus startup/shutdown: **1 hour total**

### Top 25 Cities:
- 25 cities × 5 categories × 10 pages × 6s = 125 minutes
- Plus overhead: **2.5 hours total**

### Top 50 Cities:
- 50 cities × 5 categories × 10 pages × 6s = 250 minutes
- Plus overhead: **5 hours total**

### All States:
- 38 states × 5 categories × 10 pages × 6s = 380 minutes
- Plus overhead: **8 hours total**

## 🎯 Decision Matrix

### Choose Nationwide if:
- ✅ Just testing the scraper
- ✅ Need quick results now
- ✅ Only want major businesses
- ✅ Don't have proxies set up

### Choose Top 10 Cities if:
- ✅ Running a pilot
- ✅ Have 1 hour to spare
- ✅ Want to test with proxies
- ✅ Only need major metros

### Choose Top 25 Cities if: ⭐
- ✅ Need good coverage
- ✅ Have 2-3 hours
- ✅ Want best ROI
- ✅ Have proxies (free or paid)

### Choose Top 50 Cities if:
- ✅ Need comprehensive data
- ✅ Have 5 hours
- ✅ Have paid proxies
- ✅ Want 85%+ coverage

### Choose State-by-State if:
- ✅ Need absolutely everything
- ✅ Have 8+ hours
- ✅ Have good paid proxies
- ✅ Want rural businesses too

## 📈 Expected Results

### By Category (Top 25 Cities)

**Building Supply:**
- Expected: 2,000-3,000 businesses
- Avg per city: 80-120

**Shutters:**
- Expected: 1,000-1,500 businesses
- Avg per city: 40-60

**Millwork:**
- Expected: 800-1,200 businesses
- Avg per city: 32-48

**Lumber:**
- Expected: 1,500-2,000 businesses
- Avg per city: 60-80

**Architects:**
- Expected: 2,000-3,000 businesses
- Avg per city: 80-120

**Total:** 7,300-10,700 businesses

## 🚀 Recommended Workflow

### Week 1: Test & Pilot

**Day 1: Test**
```bash
python quick_test.py  # Verify it works
```

**Day 2: Get Proxies**
```bash
python get_free_proxies.py  # Or setup paid
```

**Day 3: Pilot (Top 10)**
```bash
# Edit config_top_cities.py: CITY_LIST = TOP_10_CITIES
python run_top_cities.py
```

**Analyze:**
- How many businesses?
- Any rate limits?
- Data quality good?

### Week 2: Production

**Day 1-2: Top 25 Cities**
```bash
# config_top_cities.py: CITY_LIST = TOP_25_CITIES
python run_top_cities.py > logs/top25_scrape.log 2>&1
```

**Day 3: Cleanup**
- Remove duplicates
- Validate data
- Enrich with manual checks

**Day 4-5: Gap Fill (Optional)**
If you need more:
```bash
# Run specific missing cities
```

## 📝 Summary

**For your use case (building supply, shutters, millwork, lumber, architects):**

**BEST STRATEGY: Top 25 Cities**

```bash
# 1. Get proxies
python get_free_proxies.py

# 2. Run scraper
python run_top_cities.py

# 3. Wait 2.5 hours

# 4. Get ~10,000 businesses
```

**Backup: Top 10 for speed, Top 50 for completeness**

**Avoid: Nationwide (too limited), State-by-state (overkill)**

---

See `SCRAPING_STRATEGY.md` for detailed strategies
See `config_top_cities.py` for configuration
See `run_top_cities.py` to execute

# Yellow Pages Scraping Strategy Guide

Complete guide to scraping efficiently without getting blocked.

## 🚨 Rate Limits & Blocks

### How to Know if You're Being Rate Limited

Yellow Pages will show these signs:

#### 1. **HTTP 429 (Too Many Requests)**
```
❌ Error on page 2: 429 Too Many Requests
```
**What it means:** You're scraping too fast
**Solution:** Increase delay, use proxies

#### 2. **HTTP 403 (Forbidden)**
```
❌ Error on page 1: 403 Forbidden
```
**What it means:** IP blocked
**Solution:** Switch proxy, wait 1-2 hours

#### 3. **CAPTCHA Page**
```
⚠️  No results found on page 1
```
**What it means:** CAPTCHA challenge appeared
**Solution:** Use residential proxies, increase delays

#### 4. **Empty Results**
```
⚠️  No results found on page 1 - stopping
✓ Found 0 businesses
```
**What it means:** Either no results OR being blocked
**Solution:** Check manually, use proxies

#### 5. **Slowdowns**
Normal: 5-7 seconds per page
Throttled: 20-30+ seconds per page
**Solution:** Use different proxy

### Rate Limit Thresholds (Estimated)

Based on typical Yellow Pages behavior:

**Without Proxies:**
- **Safe:** 10-20 pages per hour (~2-3 searches)
- **Risky:** 50+ pages per hour
- **Block likely:** 100+ pages per hour

**With Proxies:**
- **Safe:** 100-200 pages per hour
- **Risky:** 500+ pages per hour per proxy
- **Block likely:** 1000+ pages per hour per proxy

**Recommendation:** Start conservative, monitor results

### Best Practices to Avoid Rate Limits

1. **Use Delays**
   - Minimum: 2 seconds between pages
   - Recommended: 3-5 seconds
   - With proxies: 2-3 seconds
   - Without proxies: 5-10 seconds

2. **Use Proxies**
   - Essential for >50 pages
   - Rotate every 10-20 pages
   - Use residential IPs (datacenter IPs get blocked faster)

3. **Scrape During Off-Peak Hours**
   - Best: 2am - 6am EST (Yellow Pages servers less loaded)
   - Avoid: 9am - 5pm EST weekdays (peak traffic)

4. **Randomize Delays**
   - Don't use exact same delay
   - Vary between 2-5 seconds randomly
   - More human-like behavior

5. **Monitor for Blocks**
   - Watch for empty results
   - Check HTTP status codes
   - Validate data quality

## 🎯 Geographic Targeting Strategy

### Option 1: Nationwide Search (Easiest)

```python
SEARCH_CATEGORIES = [
    {"term": "building supply", "location": "United States"},
]
```

**Pros:**
- ✅ Simple - one search per category
- ✅ Gets all businesses
- ✅ Fewer requests

**Cons:**
- ❌ Results may be incomplete (Yellow Pages limits nationwide results)
- ❌ Can't control geographic priority
- ❌ May miss smaller businesses (shows "top" results)

**Best for:** Quick overview, testing

### Option 2: State-by-State (Balanced)

```python
EASTERN_STATES = ['FL', 'NY', 'CA', 'TX', ...]

SEARCH_CATEGORIES = [
    {"term": "building supply", "location": state}
    for state in EASTERN_STATES
]
```

**Pros:**
- ✅ More complete results
- ✅ Can filter by state
- ✅ Manageable number of requests (~38 states)

**Cons:**
- ❌ 38x more requests than nationwide
- ❌ May still miss small cities
- ❌ Takes longer

**Best for:** Comprehensive state coverage

### Option 3: Top Cities (Recommended)

Target major metropolitan areas where most businesses are:

```python
TOP_CITIES = [
    # Florida
    "Miami, FL", "Tampa, FL", "Orlando, FL", "Jacksonville, FL",
    # New York
    "New York, NY", "Buffalo, NY", "Rochester, NY",
    # Texas
    "Houston, TX", "Dallas, TX", "Austin, TX", "San Antonio, TX",
    # California
    "Los Angeles, CA", "San Francisco, CA", "San Diego, CA",
    # More...
]
```

**Pros:**
- ✅ Targets where 80% of businesses are
- ✅ More complete results than nationwide
- ✅ Manageable request volume
- ✅ Can prioritize by city size

**Cons:**
- ❌ Misses rural/small town businesses
- ❌ More setup required

**Best for:** Most business coverage with reasonable effort

### Option 4: Hybrid Approach (Most Complete)

1. Start with top 100 cities
2. Then do state-level for remaining
3. Filter duplicates

**Best for:** Maximum coverage

## 📊 Recommended Scraping Strategy

### Phase 1: Test & Validate (Day 1)

**Goal:** Make sure everything works

```bash
# 1. Test without proxies (1 city, 1 page)
python quick_test.py

# 2. Get proxies
python get_free_proxies.py

# 3. Test with proxies (1 city, 3 pages)
python test_scraper.py  # Choose option 2

# 4. Validate data quality
head -20 test_results.csv
```

**Success criteria:**
- ✅ Getting business names
- ✅ Getting addresses
- ✅ No blocks/errors
- ✅ Proxies working

### Phase 2: Pilot Scrape (Day 1-2)

**Goal:** Scrape top 10 cities to estimate full effort

```python
# config.py
SEARCH_CATEGORIES = [
    # Top 10 cities only
    {"term": "building supply", "location": "Miami, FL"},
    {"term": "building supply", "location": "New York, NY"},
    {"term": "building supply", "location": "Los Angeles, CA"},
    # ... 7 more
]
MAX_PAGES_PER_SEARCH = 5
DELAY_BETWEEN_PAGES = 3.0
USE_PROXIES = True
```

**Run:**
```bash
./run_with_logs.sh
```

**Analyze:**
- How many businesses per city?
- How many pages needed?
- Any rate limits hit?
- Proxy success rate?
- Time per city?

**Extrapolate:**
- 10 cities × 5 pages × 6s per page = 5 minutes
- 100 cities = 50 minutes
- 5 categories = 4 hours total

### Phase 3: Full Scrape (Day 2-7)

**Goal:** Get all businesses from top cities

**Strategy A - Conservative (Recommended):**
```python
# Scrape 20 cities per day over 5 days
# Lower risk of blocks
MAX_PAGES_PER_SEARCH = 10
DELAY_BETWEEN_PAGES = 4.0
USE_PROXIES = True
```

Run daily:
```bash
./run_with_logs.sh > logs/day1.log 2>&1
```

**Strategy B - Aggressive (Risky):**
```python
# Scrape all cities in 1 day
# Higher risk but faster
MAX_PAGES_PER_SEARCH = 10
DELAY_BETWEEN_PAGES = 2.0
USE_PROXIES = True  # MUST use good proxies
```

**Strategy C - Parallel (Fastest):**
Run multiple instances with different proxies:
```bash
# Terminal 1 - Cities 1-50
python run_scraper.py > logs/batch1.log 2>&1 &

# Terminal 2 - Cities 51-100
python run_scraper.py > logs/batch2.log 2>&1 &
```

Requires different proxy pools for each.

## 🏙️ Top Cities List (Eastern States)

### By Population (Top 50)

Use this for maximum business coverage:

```python
TOP_50_EASTERN_CITIES = [
    # Mega Cities (1M+)
    "New York, NY",
    "Chicago, IL",
    "Houston, TX",
    "Philadelphia, PA",
    "San Antonio, TX",
    "Dallas, TX",
    "Austin, TX",

    # Major Cities (500K-1M)
    "Jacksonville, FL",
    "Fort Worth, TX",
    "Columbus, OH",
    "Charlotte, NC",
    "Detroit, MI",
    "El Paso, TX",
    "Memphis, TN",
    "Baltimore, MD",
    "Boston, MA",
    "Nashville, TN",
    "Oklahoma City, OK",
    "Louisville, KY",
    "Milwaukee, WI",

    # Large Cities (250K-500K)
    "Albuquerque, NM",
    "Tucson, AZ",
    "Atlanta, GA",
    "Miami, FL",
    "Minneapolis, MN",
    "Tulsa, OK",
    "Cleveland, OH",
    "Wichita, KS",
    "New Orleans, LA",
    "Tampa, FL",
    "Honolulu, HI",
    "Raleigh, NC",
    "Omaha, NE",
    "Miami, FL",
    "Virginia Beach, VA",
    "Arlington, TX",
    "Pittsburgh, PA",
    "Cincinnati, OH",
    "Lexington, KY",
    "St. Louis, MO",
    "Orlando, FL",
    "Durham, NC",
    "Jersey City, NJ",
    "Buffalo, NY",
    "Richmond, VA",
    "Madison, WI",
    "Des Moines, IA",
]
```

### By Industry Concentration

For building supplies specifically:

```python
# Cities with most construction activity
CONSTRUCTION_HEAVY_CITIES = [
    # Rapid growth = more construction
    "Austin, TX",
    "Miami, FL",
    "Tampa, FL",
    "Charlotte, NC",
    "Nashville, TN",
    "Orlando, FL",
    "Phoenix, AZ",
    "Atlanta, GA",
    "Dallas, TX",
    "Houston, TX",

    # Major metros = more businesses
    "New York, NY",
    "Chicago, IL",
    "Los Angeles, CA",
    "Philadelphia, PA",
    "Boston, MA",
]
```

## 📈 Estimating Coverage

### Nationwide vs City-Targeted

**Example: Building Supply Companies**

**Nationwide search:**
- Yellow Pages shows ~100-200 results
- May cap at 10-20 pages
- **Estimated coverage:** 200-400 businesses

**Top 50 cities:**
- Each city: 10-50 businesses
- 50 cities × 30 avg = 1,500 businesses
- **Estimated coverage:** 1,500-2,500 businesses

**State-by-state (38 states):**
- Each state: 50-200 businesses
- 38 states × 100 avg = 3,800 businesses
- **Estimated coverage:** 3,800-7,600 businesses

**Verdict:** City-targeted gives best balance of coverage vs. effort

## ⚡ Performance Optimization

### Time Estimates

**Per page:** 5-7 seconds (3s delay + 2-4s load)

**Per city:**
- 5 pages: 35 seconds
- 10 pages: 70 seconds

**Per category:**
- 50 cities × 10 pages × 6s = 50 minutes
- 100 cities × 10 pages × 6s = 100 minutes

**All 5 categories:**
- 50 cities: 4 hours
- 100 cities: 8 hours

### Parallelization

Run multiple scrapers simultaneously:

**Requirements:**
- Different proxy pools per instance
- Different output files per instance
- Different cities per instance

**Example:**
```bash
# Instance 1 - Building Supply
python run_scraper.py --category "building supply" --cities cities_1_50.txt

# Instance 2 - Lumber
python run_scraper.py --category "lumber" --cities cities_1_50.txt
```

Can reduce 8 hours to 1.5 hours with 5 parallel instances.

## 🎯 Recommended Strategy for Your Use Case

Based on your needs (building supply, shutters, millwork, lumber, architects):

### Strategy: Top Cities + State Fallback

**Week 1: Top 50 Cities**
- Scrape top 50 eastern cities
- All 5 categories
- 10 pages per city
- **Expected:** 7,500-12,500 businesses
- **Time:** 5-8 hours total
- **Cost:** Free proxies or $50 paid

**Week 2: State-Level Gaps**
- Scrape state-level for smaller states
- Fill in rural areas
- **Expected:** +2,000-3,000 businesses
- **Time:** 2-3 hours

**Week 3: Cleanup**
- Deduplicate results
- Validate data quality
- Enrich with additional info

### Configuration

I'll create this for you:

```python
# Focus on top 50 cities
TOP_50_CITIES = [...]  # Full list

# Create searches
SEARCH_CATEGORIES = []
for city in TOP_50_CITIES:
    for category in ["building supply", "shutters", "millwork", "lumber", "architects"]:
        SEARCH_CATEGORIES.append({
            "term": category,
            "location": city
        })

# Result: 50 cities × 5 categories = 250 searches
# At 10 pages each = 2,500 pages
# At 6s per page = 4 hours total
```

## 🚦 Monitoring for Rate Limits

### What to Watch

**In logs:**
```bash
# Good - consistent results
✓ Found 34 businesses (page 1)
✓ Found 30 businesses (page 2)
✓ Found 28 businesses (page 3)

# Bad - dropping off
✓ Found 34 businesses (page 1)
✓ Found 30 businesses (page 2)
⚠️  Found 0 businesses (page 3)  ← Rate limited!
```

**In real-time:**
```bash
# Watch for zeros
grep "Found 0" scraper.log

# Count errors
grep -c "❌" scraper.log

# Check success rate
grep "✓ Found" scraper.log | wc -l
```

### Response to Rate Limits

**If you see blocks:**

1. **Stop immediately**
   ```bash
   # Press Ctrl+C to stop
   ```

2. **Wait 1-2 hours**
   ```bash
   # Let IP cooldown
   ```

3. **Resume with:**
   - Higher delays (5-10s)
   - Different proxies
   - Fewer pages per search

4. **Or switch to paid proxies**

## 📊 Data Quality Monitoring

Track data completeness:

```bash
# Count complete records (with phone)
grep -c ",(" all_businesses.csv

# Count records missing phone
grep -c ",," all_businesses.csv

# Sample 10 random records
sort -R all_businesses.csv | head -10
```

**Healthy scrape:**
- 60-80% have phone numbers
- 80-90% have addresses
- 95%+ have names

**Degraded (possible blocks):**
- <40% have phone numbers
- Many duplicates
- Names only, no details

## 🎯 Summary Recommendations

### For Your Use Case

**Best approach:**
1. **Start:** Top 25 cities, 1 category, 5 pages
2. **Validate:** Check data quality
3. **Scale:** Add more cities gradually
4. **Monitor:** Watch for rate limits
5. **Optimize:** Adjust delays/proxies as needed

**Timeline:**
- Day 1: Test & validate
- Day 2-3: Top 25 cities
- Day 4-5: Cities 26-50
- Day 6-7: State-level gaps
- **Total:** ~10,000-15,000 businesses in 1 week

**Costs:**
- Free proxies: $0 (slow, risky)
- Paid proxies: $50-100/month (fast, reliable)

**Time investment:**
- Setup: 1 hour
- Monitoring: 30 min/day
- Cleanup: 2-3 hours
- **Total:** 5-6 hours of your time

Would you like me to create the top cities configuration now?

# Which Strategy Should You Use?

Quick decision guide to choose the best approach.

## 🎯 Quick Decision

Answer these questions:

### 1. How much time do you have?

- **1 hour** → Top 50 cities
- **3-5 hours** → Top 100 cities
- **8-12 hours** → Top 200 cities
- **24+ hours** → All 455 cities

### 2. How many businesses do you need?

- **5,000-10,000** → Top 50 cities
- **10,000-20,000** → Top 100 cities
- **20,000-40,000** → Top 200 cities
- **40,000-60,000+** → All 455 cities

### 3. Do you have proxies set up?

- **No proxies** → Max 50 cities (high risk)
- **Free proxies** → 50-100 cities (medium risk)
- **Paid proxies** → 100-455 cities (low risk)

### 4. What's your budget?

- **$0** → Top 50 with free proxies (risky)
- **$50-100** → Top 100-200 with paid proxies
- **$100-200** → All 455 cities with paid proxies

## 📊 Strategy Comparison (with 5 categories)

| Cities | Searches | Time | Proxies | Businesses | Cost | Best For |
|--------|----------|------|---------|------------|------|----------|
| **50** | 250 | 2.5h | Recommended | 7,500-12,500 | $0-50 | **BEST ROI** |
| **100** | 500 | 5h | Required | 15,000-25,000 | $50-100 | Balanced |
| **200** | 1,000 | 10h | Required | 30,000-50,000 | $100 | Comprehensive |
| **455** | 2,275 | 22h | Required | 68,000-114,000 | $150-200 | Exhaustive |

## 🏆 My Recommendation

**Start with TOP 50 or TOP 100**

### Why?

1. **80/20 Rule**: Top 100 cities have ~80% of all businesses
2. **Manageable**: Can complete in one work day
3. **Testable**: See results quickly, adjust if needed
4. **Cost-effective**: $50-100 for 15K-25K businesses
5. **Lower risk**: Less chance of getting blocked

### Don't Go All 455 Unless:

- ✅ You need rural/small town businesses
- ✅ You have 24+ hours to spare
- ✅ You have excellent paid proxies
- ✅ You need absolutely every business

**Reality**: Top 100 cities will give you 80% of what you need in 20% of the time.

## 🎯 Recommended Workflow

### Phase 1: Pilot (Top 50)

**Day 1:**
```bash
# Setup
python get_free_proxies.py

# Edit config_top_cities.py
CITY_LIST = TOP_50_CITIES  # Already default

# Run
python run_top_cities.py
```

**Expected:**
- Time: 2.5 hours
- Businesses: 7,500-12,500
- Cost: $0-50

**Analyze:**
- Is data quality good?
- Is coverage sufficient?
- Any rate limit issues?

### Phase 2: Scale (if needed)

**Option A: Expand to 100**
```bash
# Use pre-generated list
# Edit config_top_cities.py:
with open('cities_top_100.txt') as f:
    CITY_LIST = [line.strip() for line in f if not line.startswith('#')]

python run_top_cities.py
```

**Option B: Expand to 200**
```bash
# Edit config_top_cities.py:
with open('cities_top_200.txt') as f:
    CITY_LIST = [line.strip() for line in f if not line.startswith('#')]

python run_top_cities.py
```

**Option C: Go all in (455)**
```bash
# Edit config_top_cities.py:
with open('cities_all.txt') as f:
    CITY_LIST = [line.strip() for line in f if not line.startswith('#')]

python run_top_cities.py
```

## 💰 Cost-Benefit Analysis

### Top 50 Cities
- **Businesses:** ~10,000
- **Cost:** $0-50 (free or paid proxies)
- **Per business:** $0.005
- **Coverage:** ~60% of market
- **Verdict:** ⭐⭐⭐⭐⭐ **Best value**

### Top 100 Cities
- **Businesses:** ~20,000
- **Cost:** $50-100
- **Per business:** $0.005
- **Coverage:** ~80% of market
- **Verdict:** ⭐⭐⭐⭐⭐ **Best balance**

### Top 200 Cities
- **Businesses:** ~40,000
- **Cost:** $100
- **Per business:** $0.0025
- **Coverage:** ~90% of market
- **Verdict:** ⭐⭐⭐⭐ Good if you need more

### All 455 Cities
- **Businesses:** ~90,000
- **Cost:** $150-200
- **Per business:** $0.002
- **Coverage:** ~98% of market
- **Verdict:** ⭐⭐⭐ Overkill for most uses

## ⚡ Speed Comparison

**Per search:** ~60 seconds (10 pages × 6s)

### Top 50 Cities:
- 50 cities × 5 categories = 250 searches
- 250 × 60s = 15,000s = **2.5 hours**

### Top 100 Cities:
- 100 cities × 5 categories = 500 searches
- 500 × 60s = 30,000s = **5 hours**

### Top 200 Cities:
- 200 cities × 5 categories = 1,000 searches
- 1,000 × 60s = 60,000s = **10 hours**

### All 455 Cities:
- 455 cities × 5 categories = 2,275 searches
- 2,275 × 60s = 136,500s = **22 hours**

## 🚦 Risk Assessment

### Top 50 - Low Risk ✅
- Can use free proxies
- Unlikely to get blocked
- Easy to complete in one session

### Top 100 - Medium Risk ⚠️
- Should use paid proxies
- Possible blocks with free proxies
- Can split into 2 sessions

### Top 200 - Higher Risk 🟡
- Need paid proxies
- May hit rate limits
- Should split into 2-3 sessions

### All 455 - High Risk 🔴
- Must use paid residential proxies
- Will likely hit rate limits
- Split into 3-5 sessions over multiple days

## 📈 Expected Data Coverage

### Building Supply Example:

**Top 50 cities:**
- ~50 businesses per city avg
- 50 × 50 = 2,500 building supply companies
- **Coverage:** Major markets only

**Top 100 cities:**
- ~40 businesses per city avg
- 100 × 40 = 4,000 building supply companies
- **Coverage:** Major + medium markets

**Top 200 cities:**
- ~30 businesses per city avg
- 200 × 30 = 6,000 building supply companies
- **Coverage:** Major + medium + small markets

**All 455 cities:**
- ~20 businesses per city avg
- 455 × 20 = 9,100 building supply companies
- **Coverage:** Everything including rural

## 🎯 My Strong Recommendation

**TOP 100 CITIES = Sweet Spot**

Why?
1. 80% of businesses in 20% of the time
2. Affordable ($50-100)
3. Completeable in one work day
4. Lower risk than 200+
5. Better coverage than 50

**Perfect for:** Most business use cases

**Skip if:**
- You ONLY need major metros (use Top 50)
- You need absolutely everything (use 200+)

## 🚀 Get Started Now

### Recommended: Top 100 Strategy

```bash
# 1. Get proxies (if not done)
python get_free_proxies.py
# OR setup paid proxies

# 2. Edit config_top_cities.py
# Add this at the top:
with open('cities_top_100.txt') as f:
    CITY_LIST = [line.strip() for line in f if not line.startswith('#') and line.strip()]

# 3. Run
python run_top_cities.py

# 4. Wait 5 hours, get ~20,000 businesses
```

## ❓ Still Unsure?

### Start small, scale up:

**Week 1:** Top 50 (2.5 hours)
**Week 2:** Add cities 51-100 if needed (2.5 hours)
**Week 3:** Add cities 101-200 if still need more (5 hours)

This lets you:
- ✅ Validate data quality first
- ✅ See if Top 50 is enough
- ✅ Scale only if necessary
- ✅ Spread cost over time

---

**Bottom line:** Top 100 cities, 5 hours, $50-100 = 20,000 businesses.

That's the sweet spot. 🎯

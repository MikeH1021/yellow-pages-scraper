# Nationwide Business Scraping Estimates

## Current Coverage: Eastern US

**Configured:** 455 cities across 38 states east of Colorado
**Estimated leads:** 100,000-150,000 unique businesses

---

## Nationwide Expansion Potential

### Western States Not Yet Covered (12 states)

**Major Western States:**
- California (CA) - MASSIVE population
- Washington (WA)
- Oregon (OR)
- Colorado (CO)
- Arizona (AZ)
- Nevada (NV)
- New Mexico (NM)
- Utah (UT)
- Idaho (ID)
- Montana (MT)
- Wyoming (WY)
- Alaska (AK)
- Hawaii (HI)

### Major Western Cities to Add (~120-150 cities)

**California alone (30-40 cities):**
- Los Angeles, San Diego, San Jose, San Francisco, Fresno, Sacramento, Long Beach, Oakland, Bakersfield, Anaheim, Santa Ana, Riverside, Stockton, Irvine, Chula Vista, Fremont, San Bernardino, Modesto, Fontana, Oxnard, Moreno Valley, Huntington Beach, Glendale, Santa Clarita, Garden Grove, Oceanside, Rancho Cucamonga, Santa Rosa, Ontario, Elk Grove, Corona, Lancaster, Palmdale, Salinas, Pomona, Hayward, Sunnyvale, Pasadena, Torrance, Escondido...

**Other Major Western Cities:**
- Seattle, WA
- Portland, OR
- Denver, CO
- Colorado Springs, CO
- Phoenix, AZ
- Tucson, AZ
- Las Vegas, NV
- Reno, NV
- Albuquerque, NM
- Salt Lake City, UT
- Boise, ID
- Spokane, WA
- Tacoma, WA
- And 50-80 more...

---

## Nationwide Totals

### Conservative Estimate

| Region | Cities | Est. Unique Businesses |
|--------|--------|----------------------|
| **Eastern US** (current) | 455 | 100,000-150,000 |
| **Western US** (expansion) | 120-150 | 40,000-70,000 |
| **TOTAL NATIONWIDE** | **575-605** | **150,000-220,000** |

### Optimistic Estimate

| Region | Cities | Est. Unique Businesses |
|--------|--------|----------------------|
| **Eastern US** (current) | 455 | 150,000-200,000 |
| **Western US** (expansion) | 150-180 | 60,000-100,000 |
| **TOTAL NATIONWIDE** | **605-635** | **220,000-300,000** |

---

## Why These Numbers?

### Raw Results vs. Unique Businesses

**Raw scraping results:**
- 600 cities × 5 categories = 3,000 searches
- 3,000 searches × 300-500 businesses per search = **900,000-1,500,000 raw results**

**After deduplication:**
- Same business appears in multiple categories (e.g., a lumber yard shows up in "building supply" AND "lumber")
- Typical deduplication rate: 60-75% overlap
- **Final unique businesses: 150,000-300,000**

### Category Overlap Examples

A typical building supply company might appear in:
- "building supply" ✓
- "lumber" ✓
- "millwork" ✓
- Total: 3 times (2 duplicates)

A shutter installer might appear in:
- "shutters" ✓
- "building supply" (maybe)
- Total: 1-2 times

An architect typically only appears in:
- "architects" ✓
- Total: 1 time (no duplicates)

**Average duplication factor:** Each business appears 2-3 times across categories

---

## Realistic Nationwide Target

### Best Estimate: **200,000-250,000 unique businesses**

**Breakdown:**
- Building supply companies: 60,000-80,000
- Lumber yards: 30,000-40,000
- Millwork companies: 20,000-30,000
- Shutter dealers/installers: 10,000-15,000
- Architects: 80,000-100,000

**Note:** Architects are the largest category (less overlap with others)

---

## Runtime & Cost for Nationwide

### Full Nationwide Scrape

**Configuration:**
- 600 cities (all 50 states)
- 5 categories
- 3,000 total searches
- 10 pages per search

**Runtime:**
- 3,000 searches × 6 minutes per search = 18,000 minutes
- **30 hours of continuous scraping**

**Bandwidth/Cost:**
- ~15GB of proxy bandwidth
- Cost: ~$13.50 with current Webshare pricing
- **Cost per lead: $0.000054-$0.000068** (for 200K-250K unique businesses)

---

## Phased Rollout Strategy

### Phase 1: Eastern US (CURRENT) ✓
- 455 cities, 38 states
- 100,000-150,000 businesses
- 23 hours runtime
- **Status: READY TO RUN**

### Phase 2: Add California
- Add 40 CA cities
- +30,000-50,000 businesses
- +4 hours runtime
- New total: 130,000-200,000 businesses

### Phase 3: Add Western States
- Add remaining 100 western cities
- +20,000-40,000 businesses
- +10 hours runtime
- New total: 150,000-240,000 businesses

### Phase 4: Deep Dive Secondary Markets
- Add smaller cities (population 50K-100K)
- +20,000-50,000 businesses
- +7 hours runtime
- **Final total: 200,000-300,000 businesses**

---

## Geographic Coverage Analysis

### Top 100 Cities Nationwide

**East vs. West Split:**
- Top 100 Eastern cities: ~70 cities (covered ✓)
- Top 100 Western cities: ~30 cities (not covered yet)

**Adding Top 30 Western Cities Would Give:**
- Total coverage: 485 cities
- Estimated businesses: 130,000-180,000 (huge boost from adding CA/TX cities)
- Additional runtime: +3 hours

---

## Industry Density by Region

### Where the Businesses Are

**Highest Density Regions:**
1. **California** - Most construction/building activity
2. **Texas** - Covered in eastern config (Dallas, Houston, Austin, San Antonio)
3. **Florida** - Covered (Miami, Tampa, Jacksonville, Orlando)
4. **New York** - Covered (NYC, Buffalo, Rochester)
5. **Illinois** - Covered (Chicago)

**What We're Missing:**
- Los Angeles metro: 10,000-15,000 potential businesses
- San Francisco Bay Area: 5,000-8,000 potential businesses
- San Diego: 3,000-5,000 potential businesses
- Seattle metro: 3,000-5,000 potential businesses
- Phoenix metro: 3,000-4,000 potential businesses
- Denver metro: 2,000-3,000 potential businesses

**Total missing from western markets: 30,000-50,000 businesses**

---

## Comparison to Cobblestone's "25,000 Dealers"

**Cobblestone mentioned:**
> "We have 25,000 potential dealers nationwide"

**What this system can deliver:**
- Eastern US only: 100,000-150,000 businesses (4-6x more)
- Nationwide: 200,000-250,000 businesses (8-10x more)

**Why the difference?**
- Cobblestone's 25K might be:
  - Only direct dealers (we're catching wholesalers, installers, etc.)
  - Only building supply (we have 5 categories)
  - Pre-filtered/qualified list (we get raw universe)
  - Purchased list with limited coverage

**Our advantage:**
- Comprehensive universe of ALL businesses in these categories
- Includes direct dealers, wholesalers, installers, architects
- Fresh data from Yellow Pages (not stale lists)
- Filterable/segmentable by category, location, rating, years in business

---

## Bottom Line

### Nationwide Scraping Potential

**Conservative:** 150,000-200,000 unique businesses
**Realistic:** 200,000-250,000 unique businesses
**Optimistic:** 250,000-300,000 unique businesses

### Recommended Approach

**Start with Eastern US (current config):**
- 100,000-150,000 businesses
- 23 hours runtime
- $9 cost
- Validate data quality and response rates

**Then expand to California:**
- +30,000-50,000 businesses
- +4 hours
- +$2.50

**Then complete nationwide:**
- +20,000-50,000 businesses
- +7 hours
- +$3

**Total Nationwide:**
- **200,000-250,000+ unique businesses**
- **34 hours total runtime** (can split across multiple days)
- **~$15 total cost**
- **Repeatable monthly/quarterly**

---

## For Your Client Pitch

**Current scope (Eastern US):**
"We can deliver 100,000-150,000 qualified leads in your target categories"

**Nationwide potential:**
"Expandable to 200,000-250,000 leads covering all 50 states"

**The real value:**
"This isn't a one-time list. We can refresh this monthly to maintain a consistent pipeline of hundreds of thousands of fresh leads."

**Cost comparison:**
- Buying 200K leads at $0.10/lead = $20,000
- Our system: $15 per run, unlimited runs = **1,300x cheaper**

---

## Easy Nationwide Expansion

### To Enable Nationwide Scraping

**Add this file: `cities_nationwide.txt`**
```
# Top 600 US cities including western states
New York, NY
Los Angeles, CA
Chicago, IL
Houston, TX
Phoenix, AZ
Philadelphia, PA
San Antonio, TX
San Diego, CA
Dallas, TX
San Jose, CA
...
```

**Modify `config_top_cities.py`:**
```python
# Change from:
with open('cities_top_100.txt') as f:

# To:
with open('cities_nationwide.txt') as f:
```

**Run:**
```bash
python run_top_cities.py
```

**That's it.** Same scraper, bigger list = nationwide coverage.

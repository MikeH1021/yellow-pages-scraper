# 🚀 START HERE

Quick guide to get scraping in under 5 minutes!

## What You're Building

A scraper that extracts business data from Yellow Pages for:
- ✅ Building Supply Companies
- ✅ Shutters
- ✅ Millwork
- ✅ Lumber
- ✅ Architects

Filtered for states **east of Colorado** (38 states).

## 📋 Step-by-Step Guide

### Step 1: Install Dependencies (If Not Done)

```bash
./setup.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Quick Test (No Proxies)

Test that everything works:

```bash
python test_scraper.py
```

Choose option **1** (test without proxies).

**What you'll see:**
- Browser window opens
- Navigates to Yellow Pages
- Scrapes 1 page
- Shows progress logs
- Creates `test_results.csv`

**Expected output:**
```
21:45:23 - INFO - Starting browser...
21:45:25 - INFO - 📄 Scraping page 1/1 for 'building supply'...
21:45:28 - INFO - ✓ Found 15 businesses on page 1 (Total: 15)
21:45:28 - INFO - 💾 Saved 15 businesses to test_results.csv
21:45:28 - INFO - SUCCESS!
```

### Step 3: Get Free Proxies (Recommended)

To avoid IP bans:

```bash
python get_free_proxies.py
```

This will:
1. Fetch free proxies from public sources
2. Test each one (takes 2-5 minutes)
3. Save working ones to `proxies.txt`

**You should get 3-10 working proxies.**

### Step 4: Test With Proxies

```bash
python test_scraper.py
```

Choose option **2** (test with proxies).

If this works, you're ready for production!

### Step 5: Configure Your Scrape

Edit `config.py`:

```python
# Enable proxies
USE_PROXIES = True

# How many pages per category? (start small)
MAX_PAGES_PER_SEARCH = 3

# Delay between pages (seconds)
DELAY_BETWEEN_PAGES = 3.0

# Categories to scrape
SEARCH_CATEGORIES = [
    {"term": "building supply", "location": "United States"},
    {"term": "shutters", "location": "United States"},
    {"term": "millwork", "location": "United States"},
    {"term": "lumber", "location": "United States"},
    {"term": "architects", "location": "United States"},
]
```

### Step 6: Run Full Scrape

```bash
python run_scraper.py
```

**Watch the logs:**
```
📄 Scraping page 1/3 for 'building supply'...
🔒 Using proxy: 123.45.67.89:8080
✓ Found 15 businesses on page 1 (Total: 15)
📄 Scraping page 2/3 for 'building supply'...
✓ Found 15 businesses on page 2 (Total: 30)
💾 Saved 45 businesses to building_supply_20260119_214523.csv
```

### Step 7: Check Results

Your CSV files are ready:

```bash
ls -lh *.csv
```

Files created:
- `building_supply_TIMESTAMP.csv` - Each category
- `all_businesses_TIMESTAMP.csv` - All combined
- `eastern_businesses_TIMESTAMP.csv` - Filtered for eastern states

Open in Excel, Google Sheets, or any spreadsheet app!

## 📊 Tracking Progress

### See Logs in Real-Time

The scraper automatically shows:
- ✅ Which page it's scraping
- 🔒 Which proxy it's using
- ✓ How many businesses found
- 💾 Files being saved
- ❌ Any errors

Example:
```
21:45:23 - INFO - [1/5] Scraping: building supply
21:45:24 - INFO - 🔒 Using proxy: 123.45.67.89:8080
21:45:25 - INFO - 📄 Scraping page 1/3...
21:45:28 - INFO - ✓ Found 15 businesses (Total: 15)
21:45:31 - INFO - 📄 Scraping page 2/3...
21:45:34 - INFO - ✓ Found 15 businesses (Total: 30)
21:45:37 - INFO - 📄 Scraping page 3/3...
21:45:40 - INFO - ✓ Found 12 businesses (Total: 42)
21:45:41 - INFO - 💾 Saved 42 businesses to building_supply_20260119.csv
```

### Save Logs to File

```bash
python run_scraper.py | tee scraper.log
```

Then in another terminal:
```bash
tail -f scraper.log
```

## 🔧 Common Issues

### "No proxies found"
Run: `python get_free_proxies.py`

### "No businesses found"
- Yellow Pages might have changed their HTML
- Check STRUCTURE_NOTES.md
- Try a different search term manually on yellowpages.com

### "403 Forbidden" or "Blocked"
- Need proxies or better proxies
- Increase delay: `DELAY_BETWEEN_PAGES = 5.0`
- Use paid proxies (see PROXY_GUIDE.md)

### "Proxy failed"
Free proxies die frequently:
- Re-run: `python get_free_proxies.py`
- Or use paid proxies (PROXY_GUIDE.md)

## 📚 Documentation

- **QUICK_START.md** - Fast setup guide
- **TESTING_GUIDE.md** - Testing & logging details
- **PROXY_GUIDE.md** - Proxy setup (free & paid)
- **STRUCTURE_NOTES.md** - HTML structure & debugging
- **README.md** - Complete documentation

## 💡 Tips

### Start Small
- Test with 1-2 pages first
- Verify data quality
- Then scale up

### Free vs Paid Proxies

**Free proxies:**
- ✅ Free!
- ❌ 60-90% don't work
- ❌ Slow
- ❌ May stop working mid-scrape
- **Use for:** Testing only

**Paid proxies ($50-500/month):**
- ✅ 99% reliable
- ✅ Fast
- ✅ Rotating IPs
- ✅ Support
- **Use for:** Production scraping

See PROXY_GUIDE.md for paid options.

### Avoid IP Bans

1. **Use proxies** - Essential for large scrapes
2. **Increase delays** - 3-5 seconds between pages
3. **Scrape off-peak** - Late night/early morning
4. **Start small** - Test before big scrapes
5. **Monitor logs** - Watch for 403 errors

### Data Quality

Always check your first results:
```bash
head -20 test_results.csv
```

Verify:
- ✓ Business names look correct
- ✓ Addresses are complete
- ✓ Phone numbers present
- ✓ No duplicate entries

## 🎯 Production Workflow

```bash
# 1. Setup (one time)
./setup.sh
python get_free_proxies.py  # Or setup paid proxies

# 2. Test
python test_scraper.py

# 3. Configure
nano config.py  # Set USE_PROXIES = True

# 4. Run with logging
python run_scraper.py | tee scrape_$(date +%Y%m%d_%H%M%S).log

# 5. Check results
ls -lh *.csv
wc -l all_businesses_*.csv
```

## 🚨 Important Notes

- **Terms of Service:** Check Yellow Pages TOS before scraping
- **Rate Limits:** Don't hammer their servers
- **Data Usage:** Respect business privacy
- **Commercial Use:** May require permission

## ✅ Quick Checklist

Before your first scrape:

- [ ] Dependencies installed
- [ ] Test without proxies passed
- [ ] Free proxies fetched (or paid proxies configured)
- [ ] Test with proxies passed
- [ ] config.py configured
- [ ] Understand the logs

You're ready to scrape! 🎉

## Need Help?

1. Check **TESTING_GUIDE.md** for log interpretation
2. Check **PROXY_GUIDE.md** for proxy issues
3. Check **STRUCTURE_NOTES.md** if no data found
4. Enable DEBUG logging for details

---

**Quick Commands:**
```bash
# Test scraper
python test_scraper.py

# Get free proxies
python get_free_proxies.py

# Run full scrape
python run_scraper.py

# Run with logs saved
python run_scraper.py | tee scraper.log
```

Happy scraping! 🚀

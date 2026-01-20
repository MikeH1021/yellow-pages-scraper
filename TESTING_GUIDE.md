# Testing & Logging Guide

Complete guide for testing the scraper and tracking progress with logs.

## Quick Test (No Proxies)

Test the scraper without proxies first:

```bash
python test_scraper.py
# Choose option 1
```

This will:
- ✓ Scrape 1 page of results
- ✓ Show browser window (you can watch it work)
- ✓ Display progress with detailed logs
- ✓ Save results to `test_results.csv`

**Expected output:**
```
21:45:23 - INFO - ==================================================
21:45:23 - INFO - TEST 1: Scraping WITHOUT proxies
21:45:23 - INFO - ==================================================
21:45:24 - INFO - Starting browser...
21:45:25 - INFO - Scraping building supply in Miami, FL (1 page only)...
21:45:25 - INFO - 📄 Scraping page 1/1 for 'building supply' in Miami, FL...
21:45:28 - INFO - ✓ Found 15 businesses on page 1 (Total: 15)
21:45:28 - INFO - ==================================================
21:45:28 - INFO - SUCCESS! Found 15 businesses
21:45:28 - INFO - ==================================================
21:45:28 - INFO - 💾 Saved 15 businesses to test_results.csv
```

## Test With Free Proxies

### Step 1: Get Free Proxies

```bash
python get_free_proxies.py
```

This will:
1. Fetch proxies from free proxy sites
2. Test each proxy (may take 2-5 minutes)
3. Save working proxies to `proxies.txt`

**Expected output:**
```
Fetching proxies from free-proxy-list.net...
✓ Found 30 proxies from free-proxy-list.net
Fetching proxies from sslproxies.org...
✓ Found 20 proxies from sslproxies.org

Validating proxies (this may take a few minutes)...
✓ Proxy 123.45.67.89:8080 works (IP: 123.45.67.89)
✗ Proxy 98.76.54.32:3128 failed: timeout
...

5/50 proxies are working

Saved 5 working proxies to proxies.txt
```

### Step 2: Test With Proxies

```bash
python test_scraper.py
# Choose option 2
```

## Viewing Logs

### Log Levels

The scraper uses different log levels:

**INFO** (default) - Main progress updates:
```
21:45:23 - INFO - 📄 Scraping page 1/3...
21:45:25 - INFO - ✓ Found 15 businesses
21:45:26 - INFO - 💾 Saved to file.csv
```

**DEBUG** - Detailed information:
```
21:45:23 - DEBUG - URL: https://yellowpages.com/...
21:45:24 - DEBUG - Waiting 3.0s before extracting...
21:45:25 - DEBUG - Found 20 potential listings on page
21:45:25 - DEBUG -   ✓ Parsed: ABC Company
```

**WARNING** - Issues (non-fatal):
```
21:45:25 - WARNING - ⚠️  No results found on page 3
21:45:26 - WARNING - ⚠️  Error parsing listing: missing name
```

**ERROR** - Serious problems:
```
21:45:30 - ERROR - ❌ Error on page 2: timeout
```

### Enable Debug Logging

For maximum detail, edit any script to add:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or set environment variable:
```bash
export LOG_LEVEL=DEBUG
python run_scraper.py
```

### Save Logs to File

Redirect output to a file:

```bash
# Save all output
python run_scraper.py > scraper.log 2>&1

# Save only to file (no console output)
python run_scraper.py > scraper.log 2>&1 &

# Watch logs in real-time
tail -f scraper.log
```

Or modify the script to write to file:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()  # Also print to console
    ]
)
```

## Understanding Log Messages

### Successful Scrape Flow

```
📄 Scraping page 1/3...          # Starting page
🔒 Using proxy: 1.2.3.4:8080     # Using proxy (if enabled)
✓ Found 15 businesses            # Successfully extracted
💾 Saved to file.csv             # Saved results
```

### Common Issues

#### No Results Found
```
⚠️  No results found on page 1 - stopping
```

**Possible causes:**
- Yellow Pages changed their HTML
- Search returned no matches
- Being blocked (need proxies)

**Solutions:**
1. Check if search term works on yellowpages.com manually
2. Try different search term/location
3. Enable proxies
4. Check STRUCTURE_NOTES.md for HTML changes

#### Proxy Errors
```
❌ Error on page 1: timeout
```

**Possible causes:**
- Proxy is dead/slow
- Proxy is blocked by Yellow Pages
- Network issue

**Solutions:**
1. Re-fetch proxies: `python get_free_proxies.py`
2. Enable proxy validation in config.py
3. Use paid proxies (more reliable)

#### Rate Limited / Blocked
```
❌ Error on page 2: 403 Forbidden
```

**Solutions:**
1. Enable proxies
2. Increase delay: `DELAY_BETWEEN_PAGES = 5.0`
3. Use paid residential proxies
4. Wait before trying again

## Progress Tracking

### Track Progress in Real-Time

Open two terminals:

**Terminal 1 - Run scraper:**
```bash
python run_scraper.py | tee scraper.log
```

**Terminal 2 - Watch progress:**
```bash
watch -n 1 'tail -20 scraper.log'
```

### Track Files Created

```bash
watch -n 2 'ls -lht *.csv | head -10'
```

Shows newest CSV files as they're created.

### Count Results

```bash
# Count total results in CSV
wc -l *.csv

# Count by category
grep -c "building supply" all_businesses_*.csv
```

## Testing Checklist

Before running a large scrape:

- [ ] Run `python test_scraper.py` successfully
- [ ] Verify results in `test_results.csv`
- [ ] If using proxies:
  - [ ] Run `python get_free_proxies.py`
  - [ ] At least 3-5 working proxies
  - [ ] Test with `python test_scraper.py` option 2
- [ ] Configure `config.py`:
  - [ ] Set reasonable `MAX_PAGES_PER_SEARCH` (start with 3)
  - [ ] Set `DELAY_BETWEEN_PAGES` (3.0+ with proxies)
  - [ ] Enable `USE_PROXIES` if needed
- [ ] Verify categories in `SEARCH_CATEGORIES`

## Monitoring Long Scrapes

For scrapes that take hours:

### 1. Run in Background
```bash
nohup python run_scraper.py > scraper.log 2>&1 &
echo $! > scraper.pid  # Save process ID
```

### 2. Check Progress
```bash
tail -f scraper.log
```

### 3. Check Status
```bash
ps -p $(cat scraper.pid)
```

### 4. Stop if Needed
```bash
kill $(cat scraper.pid)
```

## Performance Metrics

The scraper logs include timing information:

```
21:45:23 - INFO - 📄 Scraping page 1/3...
21:45:28 - INFO - ✓ Found 15 businesses (Total: 15)
```

**Time per page:** ~5 seconds (in this example)

**Estimated time calculations:**
- 1 page = ~5 seconds
- 10 pages = ~50 seconds
- 100 pages = ~8 minutes
- 1000 pages = ~1.5 hours

Add `DELAY_BETWEEN_PAGES` to these estimates.

## Log Analysis

### Count successes/errors:
```bash
grep "✓ Found" scraper.log | wc -l  # Successful pages
grep "❌ Error" scraper.log | wc -l   # Failed pages
grep "⚠️" scraper.log               # Warnings
```

### Extract business counts:
```bash
grep "✓ Found" scraper.log | awk '{print $6}' | paste -sd+ | bc
```

### See proxy usage:
```bash
grep "🔒 Using proxy" scraper.log | sort | uniq -c
```

## Debugging Tips

### 1. Enable Maximum Logging

```python
# At top of any script
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 2. Save HTML for Inspection

Add to scraper:
```python
# In _extract_businesses method
with open(f'debug_page_{page_num}.html', 'w') as f:
    f.write(content)
```

### 3. Print Raw Data

```python
# In _parse_listing method
print("RAW HTML:", listing.prettify()[:500])
```

### 4. Slow Down

```python
# Give yourself time to watch
delay=10.0
headless=False
```

## Getting Help

If tests fail:

1. **Check logs** for specific error messages
2. **Read STRUCTURE_NOTES.md** - Yellow Pages may have changed
3. **Try different search** - Some categories may not exist
4. **Enable DEBUG logging** - Get more details
5. **Test manually** - Visit yellowpages.com and try the search

## Example Test Session

```bash
# Full testing workflow
cd /Users/jonathangarces/Desktop/yellow\ page\ scraper

# 1. Quick test without proxies
python test_scraper.py  # Choose 1
# Check test_results.csv

# 2. Get free proxies
python get_free_proxies.py
# Wait for validation...

# 3. Test with proxies
python test_scraper.py  # Choose 2
# Check test_results_with_proxy.csv

# 4. Configure for real scrape
nano config.py
# Set USE_PROXIES = True
# Set MAX_PAGES_PER_SEARCH = 3

# 5. Run real scrape with logging
python run_scraper.py | tee full_scrape.log

# 6. Check results
ls -lh *.csv
head -20 all_businesses_*.csv
```

Happy testing! 🧪

# Web UI Guide - Yellow Pages Scraper

## Quick Start

### 1. Install Dependencies

```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"
source venv/bin/activate
pip install flask flask-cors
```

### 2. Start the Web Server

```bash
python web_app.py
```

You should see:
```
====================================================================
Yellow Pages Scraper Web UI
====================================================================

Starting server at: http://localhost:5000

Open your browser and navigate to http://localhost:5000
====================================================================
```

### 3. Open Your Browser

Navigate to: **http://localhost:5000**

---

## Using the Web Interface

### Configuration Panel

**1. Enter Keywords (comma-separated)**
```
building supply, shutters, millwork, lumber, architects
```

**2. Enter Locations (comma-separated)**
```
Miami FL, Chicago IL, New York NY
```

**3. Set Max Pages per Search**
- Default: 10 pages (≈ 300 businesses per search)
- Each page = ≈30 businesses
- Lower for faster testing

**4. Enable/Disable Proxies**
- ✅ Use Proxies (recommended)
- ⬜ Use Proxies (direct connection, may get blocked)

**5. Click "🚀 Start Scraping"**

---

## Proxy Management Panel

### Upload Proxies

**Method 1: Click Upload Button**
1. Click "📁 Click to upload proxies.txt"
2. Select your proxy file
3. See confirmation: "✅ Loaded 10 proxies"

**Method 2: Manual File**
```bash
# Your proxies are already at:
/Users/jonathangarces/Desktop/yellow page scraper/proxies.txt

# Just click refresh or reload page to see them
```

### Proxy Health Status

**Real-time table shows:**
| Column | Description |
|--------|-------------|
| **Proxy** | IP:Port of the proxy |
| **Success Rate** | % of successful requests |
| **Status** | HEALTHY / WARNING / BLOCKED |
| **Last Used** | Last request timestamp |

**Status Colors:**
- 🟢 **HEALTHY** - Success rate > 70% (green)
- 🟡 **WARNING** - Success rate 40-70% (yellow)
- 🔴 **BLOCKED** - Success rate < 40% (red)

**Auto-refresh:** Updates every 5 seconds

---

## Live Logs Panel

### Real-Time Log Streaming

**See live updates:**
```
14:32:10 🚀 Starting scraper...
14:32:11 ✅ Loaded 10 proxies
14:32:12 ✅ Browser started
14:32:15 [1/10] building supply in Miami FL
14:32:20 ✓ Found 34 businesses (Total: 34)
14:32:25 [2/10] shutters in Miami FL
14:32:30 ✓ Found 28 businesses (Total: 62)
```

**Log Types:**
- 🟦 **Info** (blue) - General progress updates
- 🟩 **Success** (green) - Successful operations
- 🟥 **Error** (red) - Errors and blocks

**Auto-scroll:** Logs automatically scroll to bottom

---

## Progress Panel

### Live Progress Tracking

**Appears when scraping starts:**

**Progress Bar:**
- Visual progress indicator
- Updates in real-time
- Shows % completion

**Statistics:**
- **SEARCHES COMPLETED** - How many searches done
- **TOTAL SEARCHES** - Total searches to complete
- **BUSINESSES FOUND** - Total businesses scraped

---

## Features

### 1. Real-Time Monitoring

**Live Updates:**
- ✅ Log streaming (via Server-Sent Events)
- ✅ Progress updates (every 1 second)
- ✅ Proxy health (every 5 seconds)

**No Page Refresh Needed!**

### 2. Proxy Block Detection

**Automatic Detection:**
- HTTP 403 Forbidden → Marked as blocked
- HTTP 429 Rate Limit → Marked as blocked
- 3+ failures → Auto-blocked
- Success rate < 30% → Blocked status

**Auto-Rotation:**
- Blocked proxies automatically skipped
- Switches to next healthy proxy
- Resets blocks if proxy recovers

### 3. Easy Configuration

**Flexible Input:**
- Comma-separated keywords and locations
- Mix and match any categories and cities
- Change on the fly for each run

**Example Configurations:**

**Small Test:**
```
Keywords: building supply
Locations: Miami FL, Chicago IL
Max Pages: 5
Result: 2 searches, ~300 businesses, ~5 minutes
```

**Medium Run:**
```
Keywords: building supply, shutters, millwork
Locations: New York NY, Los Angeles CA, Chicago IL
Max Pages: 10
Result: 9 searches, ~2,700 businesses, ~45 minutes
```

**Large Run:**
```
Keywords: building supply, shutters, millwork, lumber, architects
Locations: Miami FL, Chicago IL, New York NY, Houston TX, Phoenix AZ
Max Pages: 10
Result: 25 searches, ~7,500 businesses, ~2.5 hours
```

### 4. Automatic CSV Export

**Results saved automatically:**
```
scrape_results_20260120_143215.csv
```

**File location:** Same directory as web_app.py

**CSV includes:**
- Business name
- Phone number
- Address (street, city, state, zip)
- Website
- Categories
- Rating
- Years in business
- Search category (which keyword matched)
- Search location (which city searched)

---

## Tips & Best Practices

### Starting Out

**1. Test with 1-2 cities first**
```
Locations: Miami FL, Chicago IL
Max Pages: 5
```

**2. Check proxy health before large runs**
- Upload proxies
- Check status table
- Ensure most are HEALTHY

**3. Monitor logs closely**
- Watch for 🚫 block indicators
- If > 50% proxies blocked, stop and increase delays

### During Scraping

**1. Don't close browser tab**
- Logs stream in real-time
- Progress updates live
- Closing tab doesn't stop scraper (it's running on server)

**2. Watch proxy health**
- Green = good
- Yellow = okay but watch it
- Red = blocked (auto-skipped)

**3. Monitor success rate**
- If dropping below 60%, consider:
  - Increasing delays (restart with slower config)
  - Reducing max pages
  - Taking a break to let IPs cool down

### After Scraping

**1. Check CSV output**
```bash
ls -lh scrape_results_*.csv
head -20 scrape_results_*.csv
```

**2. Review data quality**
- How many have phone numbers?
- How many have addresses?
- Any duplicates?

**3. Import to CRM**
- Ready for Instantly.ai, Salesforce, etc.
- Deduplicate against existing contacts

---

## Troubleshooting

### Web UI Won't Start

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
source venv/bin/activate
pip install flask flask-cors
python web_app.py
```

### Proxies Not Loading

**Problem:** "No proxies loaded" in UI

**Solution:**
```bash
# Check proxies.txt exists and has content
cat proxies.txt

# Should see 10 lines like:
# 142.111.48.253:7030:iyggsdpl:i7mocimb1hxn

# Re-upload through UI or restart server
```

### All Proxies Blocked

**Problem:** All proxies show RED status

**Solution:**
1. Stop scraping (click ⏹ Stop button)
2. Wait 30 minutes
3. Restart with slower delays:
   - Max Pages: 5 (instead of 10)
   - Or add more proxies from Webshare

### Scraper Running But No Logs

**Problem:** Started scraping but logs not updating

**Solution:**
1. Check browser console (F12) for errors
2. Refresh page
3. Logs reconnect automatically
4. Server is still running in background

### Can't Stop Scraper

**Problem:** Clicked ⏹ Stop but still running

**Solution:**
1. Click Stop again
2. Wait 10-15 seconds for current search to finish
3. Or close terminal (kills web_app.py)

---

## Advanced Usage

### Running in Background

**Start server in background:**
```bash
nohup python web_app.py > web_ui.log 2>&1 &
```

**Access from another device on same network:**
```python
# In web_app.py, change last line to:
app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
```

Then access from: `http://YOUR_IP:5000`

### Custom Configuration

**Edit web_app.py to change defaults:**
```python
# Line 208: Change default delays
DELAY_BETWEEN_PAGES = 5.0  # Slower/faster

# Line 209: Change default max pages
MAX_PAGES_PER_SEARCH = 5  # Fewer/more pages
```

### API Endpoints

**Programmatic access:**
```bash
# Start scraping via API
curl -X POST http://localhost:5000/api/start-scrape \
  -H "Content-Type: application/json" \
  -d '{"keywords":"building supply","locations":"Miami FL","max_pages":10,"use_proxies":true}'

# Get progress
curl http://localhost:5000/api/progress

# Get proxy status
curl http://localhost:5000/api/proxy-status

# Stop scraping
curl -X POST http://localhost:5000/api/stop-scrape
```

---

## Keyboard Shortcuts

**While on the page:**
- **Ctrl+C** (in terminal) - Stop server
- **F5** - Refresh page (logs reconnect automatically)
- **Ctrl+Shift+I** - Open browser dev tools (see detailed logs)

---

## File Locations

```
/Users/jonathangarces/Desktop/yellow page scraper/
├── web_app.py                     ← Flask server (run this)
├── templates/
│   └── scraper.html              ← Web interface
├── proxies.txt                   ← Your proxies (10 lines)
├── scrape_results_*.csv          ← Output files
├── yellowpages_scraper.py        ← Scraper engine
└── proxy_manager.py              ← Proxy rotation
```

---

## Example Workflow

### Complete Scraping Session

**1. Prepare**
```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"
source venv/bin/activate
```

**2. Start Server**
```bash
python web_app.py
```

**3. Open Browser**
- Navigate to http://localhost:5000
- Upload proxies.txt (if not already loaded)
- Check proxy health table

**4. Configure Scrape**
```
Keywords: building supply, shutters, millwork
Locations: Miami FL, Chicago IL, Houston TX
Max Pages: 10
✅ Use Proxies
```

**5. Start & Monitor**
- Click "🚀 Start Scraping"
- Watch logs for progress
- Monitor proxy health (should stay mostly green)
- Check progress bar

**6. Complete**
- Wait for "✅ COMPLETE!" message
- Check CSV file created
- Review data quality in logs

**7. Import Data**
```bash
# Open CSV
open scrape_results_20260120_143215.csv

# Or import to tool
# Upload to Instantly.ai, Salesforce, etc.
```

**8. Cleanup**
- Click ⏹ Stop (if still running)
- Ctrl+C in terminal to stop server
- `deactivate` to exit venv

---

## Summary

### What You Get

✅ **Easy-to-use web interface**
- No command line needed (except starting server)
- Point-and-click configuration
- Real-time visual feedback

✅ **Live monitoring**
- See logs as they happen
- Track progress in real-time
- Monitor proxy health visually

✅ **Automatic proxy management**
- Upload proxies with one click
- Auto-detect and skip blocked proxies
- Health tracking and rotation

✅ **Professional results**
- Clean CSV export
- Organized by search category and location
- Ready for CRM import

### Perfect For

- **Testing different configurations** - Quick iterations
- **Monitoring long scrapes** - Real-time visibility
- **Managing proxies** - Easy upload and health tracking
- **Non-technical users** - Simple interface, no coding needed

---

**Ready to scrape! Open http://localhost:5000 and start generating leads.** 🚀

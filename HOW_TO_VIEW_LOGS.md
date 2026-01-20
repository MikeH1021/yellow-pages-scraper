# How to View Logs

Complete guide to viewing and managing scraper logs.

## Quick Answer

**Logs show automatically when you run the scraper!**

Just run any script and watch your terminal:
```bash
python test_scraper.py
python run_scraper.py
python quick_test.py
```

## 📺 Live Logs (See Progress in Real-Time)

### Method 1: Just Run the Script

```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"
source venv/bin/activate
python run_scraper.py
```

You'll see live updates:
```
21:57:01 - INFO - [1/5] Scraping: building supply
21:57:02 - INFO - 🔒 Using proxy: 123.45.67.89:8080
21:57:02 - INFO - 📄 Scraping page 1/3 for 'building supply'...
21:57:09 - INFO - ✓ Found 34 businesses on page 1 (Total: 34)
21:57:10 - INFO - 📄 Scraping page 2/3...
21:57:17 - INFO - ✓ Found 30 businesses on page 2 (Total: 64)
21:57:18 - INFO - 💾 Saved 64 businesses to building_supply_20260119.csv
```

### Method 2: Run with Logs Saved to File

**Use the helper script:**
```bash
./run_with_logs.sh
```

This will:
- ✅ Show logs in terminal (live)
- ✅ Save logs to file (e.g., `scraper_20260119_215701.log`)
- ✅ Keep running history

**Or manually:**
```bash
python run_scraper.py | tee scraper.log
```

## 💾 Saving Logs to File

### Save AND Display
```bash
# Shows in terminal AND saves to file
python run_scraper.py 2>&1 | tee scraper.log
```

### Save Only (Background)
```bash
# Saves to file, no terminal output
python run_scraper.py > scraper.log 2>&1
```

### Timestamped Logs
```bash
# Creates unique log file with timestamp
python run_scraper.py > "scraper_$(date +%Y%m%d_%H%M%S).log" 2>&1
```

## 👀 Watching Logs in Real-Time

If scraper is running in background or another terminal:

### Option 1: tail -f (Follow logs)
```bash
tail -f scraper.log
```
Press `Ctrl+C` to stop watching (scraper keeps running).

### Option 2: Watch last 20 lines
```bash
# Updates every 2 seconds
watch -n 2 'tail -20 scraper.log'
```

### Option 3: Two terminals

**Terminal 1:**
```bash
python run_scraper.py > scraper.log 2>&1
```

**Terminal 2:**
```bash
tail -f scraper.log
```

## 📖 Reading Saved Logs

### View entire log
```bash
cat scraper.log
```

### View last 50 lines
```bash
tail -50 scraper.log
```

### View first 50 lines
```bash
head -50 scraper.log
```

### Search logs
```bash
# Find all errors
grep "ERROR" scraper.log

# Find all successes
grep "✓ Found" scraper.log

# Find proxy usage
grep "🔒 Using proxy" scraper.log

# Count businesses found
grep "✓ Found" scraper.log | awk '{sum+=$6} END {print sum}'
```

### View with pagination
```bash
less scraper.log
# Use arrow keys to scroll
# Press 'q' to quit
```

## 🎨 Understanding Log Messages

### Log Format
```
TIME - LEVEL - MESSAGE
21:57:02 - INFO - 📄 Scraping page 1/3...
```

### Log Levels

**INFO** - Normal progress:
```
21:57:02 - INFO - 📄 Scraping page 1/3...
21:57:09 - INFO - ✓ Found 34 businesses
21:57:10 - INFO - 💾 Saved to file.csv
```

**WARNING** - Minor issues (non-fatal):
```
21:57:15 - WARNING - ⚠️  No results found on page 3
21:57:16 - WARNING - ⚠️  Error parsing listing: missing name
```

**ERROR** - Serious problems:
```
21:57:20 - ERROR - ❌ Error on page 2: timeout
21:57:21 - ERROR - ❌ Failed to save file: permission denied
```

**DEBUG** - Detailed info (optional):
```
21:57:02 - DEBUG - URL: https://yellowpages.com/...
21:57:03 - DEBUG - Waiting 3.0s before extracting...
21:57:04 - DEBUG - Found 20 potential listings
21:57:04 - DEBUG -   ✓ Parsed: ABC Company
```

### Log Icons

- 📄 = Scraping page
- 🔒 = Using proxy
- ✓ = Success
- 💾 = Saved file
- ⚠️ = Warning
- ❌ = Error
- [1/5] = Progress (category 1 of 5)

## 🔧 Adjusting Log Detail

### More Detail (DEBUG mode)

Edit any script and change the logging level:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
```

Or set environment variable:
```bash
export LOG_LEVEL=DEBUG
python run_scraper.py
```

### Less Detail (WARNING only)

```python
logging.basicConfig(level=logging.WARNING)
```

## 📊 Log Analysis Commands

### Count successful pages
```bash
grep -c "✓ Found" scraper.log
```

### Count errors
```bash
grep -c "❌" scraper.log
```

### Total businesses scraped
```bash
grep "✓ Found" scraper.log | awk '{sum+=$6} END {print "Total businesses:", sum}'
```

### Average businesses per page
```bash
grep "✓ Found" scraper.log | awk '{sum+=$6; count++} END {print "Average:", sum/count}'
```

### Which proxies were used
```bash
grep "🔒 Using proxy" scraper.log | sort | uniq -c
```

### Time taken
```bash
head -1 scraper.log  # Start time
tail -1 scraper.log  # End time
```

## 🚀 Quick Examples

### Example 1: Run and Watch
```bash
# Terminal 1
python run_scraper.py > scraper.log 2>&1

# Terminal 2
tail -f scraper.log
```

### Example 2: Run in Background, Check Later
```bash
# Start in background
nohup python run_scraper.py > scraper.log 2>&1 &

# Check progress anytime
tail -20 scraper.log

# Watch live
tail -f scraper.log

# Check if still running
ps aux | grep run_scraper.py
```

### Example 3: Save All Runs
```bash
# Each run gets its own log file
python run_scraper.py > "logs/scraper_$(date +%Y%m%d_%H%M%S).log" 2>&1
```

## 📁 Organizing Logs

### Create logs directory
```bash
mkdir logs
```

### Save all logs there
```bash
python run_scraper.py > logs/scraper_$(date +%Y%m%d_%H%M%S).log 2>&1
```

### View all logs
```bash
ls -lh logs/
```

### Clean old logs
```bash
# Delete logs older than 7 days
find logs/ -name "*.log" -mtime +7 -delete
```

## 🎯 Common Log Tasks

### "Did my scrape succeed?"
```bash
grep "SUCCESS" scraper.log
grep "COMPLETE" scraper.log
tail -10 scraper.log
```

### "How many businesses did I get?"
```bash
grep "Total businesses found:" scraper.log
```

Or count CSV rows:
```bash
wc -l all_businesses_*.csv
```

### "Were there any errors?"
```bash
grep "ERROR\|❌" scraper.log
```

### "Which proxies worked?"
```bash
grep "🔒 Using proxy" scraper.log | cut -d: -f4 | sort | uniq -c
```

### "How fast is it scraping?"
```bash
# Show timestamps for each page
grep "📄 Scraping page" scraper.log
```

## 💡 Pro Tips

1. **Always use `tee` for important runs**
   ```bash
   python run_scraper.py | tee scraper.log
   ```
   Shows output AND saves it.

2. **Use timestamps in log filenames**
   ```bash
   python run_scraper.py > scraper_$(date +%Y%m%d_%H%M%S).log 2>&1
   ```

3. **Compress old logs**
   ```bash
   gzip old_scraper.log
   ```

4. **Combine multiple log files**
   ```bash
   cat scraper_*.log > all_scrapes.log
   ```

5. **Monitor in real-time with colors**
   ```bash
   tail -f scraper.log | grep --color=auto -E "ERROR|WARNING|SUCCESS|$"
   ```

## 🔍 Troubleshooting Logs

### "I don't see any logs"
Make sure you're running the script:
```bash
python run_scraper.py
```

Logs appear automatically in your terminal.

### "Logs are too verbose"
Change log level:
```python
logging.basicConfig(level=logging.WARNING)
```

### "I lost my logs"
If you ran without saving:
```bash
# Check terminal history
history | grep python
```

Next time use:
```bash
./run_with_logs.sh
```

### "How do I stop watching logs?"
Press `Ctrl+C` (this only stops watching, not the scraper).

## 📚 Summary

**Quick Reference:**

```bash
# See logs live
python run_scraper.py

# Save logs to file
python run_scraper.py | tee scraper.log

# Watch logs in real-time
tail -f scraper.log

# Search logs
grep "ERROR" scraper.log

# Use helper script
./run_with_logs.sh
```

**Key Log Messages to Watch:**

- `📄 Scraping page X/Y` - Progress indicator
- `✓ Found X businesses` - Success!
- `💾 Saved to file.csv` - Data saved
- `❌ Error` - Problem occurred
- `⚠️ Warning` - Minor issue

---

For more info, see `TESTING_GUIDE.md`

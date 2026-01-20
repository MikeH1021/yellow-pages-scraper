# SmartProxy Setup Guide

Step-by-step guide to configure SmartProxy with the scraper.

## Step 1: Complete Purchase

✅ You're doing this now!

Purchase 10GB from SmartProxy

## Step 2: Get Your Credentials

After purchase:

1. **Go to SmartProxy Dashboard:**
   - Login at https://dashboard.smartproxy.com/
   - Click on "Residential Proxies" or "Proxy Setup"

2. **Find Your Credentials:**
   You'll see something like:
   ```
   Username: sp12345678-country-us-session-xyz123
   Password: abc123def456
   Host: gate.smartproxy.com
   Port: 7000 (or 10000, 10001)
   ```

3. **Copy these values** - you'll need them next

## Step 3: Configure the Scraper

### Method 1: Environment Variables (Recommended)

Open terminal and run:

```bash
cd "/Users/jonathangarces/Desktop/yellow page scraper"
source venv/bin/activate

# Set your credentials (replace with your actual values)
export PROXY_SERVICE="smartproxy"
export PROXY_USERNAME="sp12345678-country-us-session-xyz123"
export PROXY_PASSWORD="your_actual_password"
```

**Note:** Replace the username and password with YOUR actual credentials from the dashboard!

### Method 2: Edit Config File

Alternatively, edit `config_top_cities.py`:

```python
# Find these lines and uncomment/edit:
USE_PAID_PROXY_SERVICE = True

# Add these if not using environment variables:
PROXY_SERVICE = "smartproxy"
# Set credentials from environment or uncomment below:
# import os
# PROXY_USERNAME = os.getenv('PROXY_USERNAME', 'your-username')
# PROXY_PASSWORD = os.getenv('PROXY_PASSWORD', 'your-password')
```

## Step 4: Test the Connection

Run a quick test:

```bash
python quick_test.py
```

You should see:
```
🔒 Using proxy: gate.smartproxy.com:7000
📄 Scraping page 1/1...
✓ Found 34 businesses
```

If you see the proxy message, it's working! ✅

## Step 5: Run the Full Scrape

Now you're ready:

```bash
python run_top_cities.py | tee smartproxy_scrape.log
```

This will:
- Use your SmartProxy residential IPs
- Scrape 100 cities × 5 categories = 500 searches
- Take ~5 hours
- Get ~20,000 businesses
- Save logs to `smartproxy_scrape.log`

## Monitoring Usage

1. **Check Dashboard:**
   - Go to https://dashboard.smartproxy.com/
   - View "Usage" or "Statistics"
   - Monitor your bandwidth consumption

2. **During Scraping:**
   - Watch logs for successful page loads
   - Check for any proxy errors
   - Should see consistent "✓ Found X businesses" messages

## Troubleshooting

### Error: "Authentication failed"
- Check username/password are correct
- Username format: `sp12345678-country-us-...` (must include country-us)
- Password: Copy exactly from dashboard (no spaces)

### Error: "Connection refused"
- Check internet connection
- Verify SmartProxy service is active
- Try different port (7000, 10000, 10001)

### Error: "Bandwidth exceeded"
- You've used all 10GB
- Upgrade plan or buy more bandwidth
- Dashboard will show exact usage

### Slow Performance
- Normal - residential proxies are slower than direct
- Each page may take 5-10 seconds
- This is expected behavior

## Expected Performance

**With SmartProxy 10GB:**
- Speed: 5-7 seconds per page
- Success rate: 95%+
- Bandwidth: ~20MB per search
- Coverage: ~500 searches = 10GB
- Result: Top 50-60 cities fully scraped

**Estimated results:**
- Searches: 250-300 (50-60 cities)
- Businesses: 10,000-15,000
- Time: 2.5-3.5 hours
- Bandwidth used: ~10GB

## SmartProxy Specific Settings

SmartProxy auto-rotates IPs, so you don't need to:
- Set rotation
- Manage sessions
- Handle IP switching

Just use the credentials and it works!

## Tips

1. **Monitor first 50 searches:**
   - Watch bandwidth usage in dashboard
   - Estimate total usage
   - Adjust plan if needed

2. **Save logs:**
   - Always use `| tee logfile.log`
   - Helps debug if issues occur

3. **Checkpoint saves:**
   - Scraper auto-saves every 25 searches
   - Safe to stop/resume if needed

4. **Bandwidth alerts:**
   - SmartProxy emails at 80%, 90% usage
   - Plan accordingly

## What's Next?

After running the scrape:

1. **Check results:**
   ```bash
   ls -lh *.csv
   wc -l top_cities_all_businesses_*.csv
   ```

2. **Review data quality:**
   ```bash
   head -20 top_cities_all_businesses_*.csv
   ```

3. **If you need more:**
   - Upgrade to 25GB in dashboard
   - Run cities 51-100
   - Get another 10,000 businesses

## Quick Command Reference

```bash
# Setup (do once)
cd "/Users/jonathangarces/Desktop/yellow page scraper"
source venv/bin/activate
export PROXY_SERVICE="smartproxy"
export PROXY_USERNAME="your-username"
export PROXY_PASSWORD="your-password"

# Test
python quick_test.py

# Run full scrape
python run_top_cities.py | tee smartproxy_scrape.log

# Monitor progress (separate terminal)
tail -f smartproxy_scrape.log

# Check results
ls -lh *.csv
```

Good luck! 🚀

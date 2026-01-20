# Quick Start Guide

Get started scraping Yellow Pages in 5 minutes!

## Step 1: Install Dependencies

Run the setup script:

```bash
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

## Step 2: Configure Your Search

Edit `config.py` to customize what you want to scrape:

```python
# What to scrape
SEARCH_CATEGORIES = [
    {"term": "building supply", "location": "United States"},
    {"term": "shutters", "location": "United States"},
    # Add more categories...
]

# How many pages per search
MAX_PAGES_PER_SEARCH = 3  # Start small for testing

# Use proxies? (recommended to avoid IP bans)
USE_PROXIES = False  # Set to True after adding proxies
```

## Step 3: Run the Scraper

### Without proxies (testing only):

```bash
python run_scraper.py
```

**Warning:** You may get IP banned if scraping too much!

### With proxies (recommended):

1. Add proxies to `proxies.txt`:
   ```
   proxy1.example.com:8080
   proxy2.example.com:3128:username:password
   ```

2. Enable in `config.py`:
   ```python
   USE_PROXIES = True
   ```

3. Run:
   ```bash
   python run_scraper.py
   ```

See [PROXY_GUIDE.md](PROXY_GUIDE.md) for where to get proxies.

## Step 4: Check Your Results

The scraper creates CSV files:

- `building_supply_20260119_123456.csv` - Individual categories
- `all_businesses_20260119_123456.csv` - All results combined
- `eastern_businesses_20260119_123456.csv` - Filtered for eastern states

Open in Excel, Google Sheets, or any CSV viewer!

## Common Commands

```bash
# Run simple test (1 category, 2 pages)
python example_simple.py

# Run with proxies
python example_with_proxies.py

# Run full configured scrape
python run_scraper.py
```

## Need Help?

1. **Getting blocked?** → Add proxies (see PROXY_GUIDE.md)
2. **No results?** → Check STRUCTURE_NOTES.md (Yellow Pages may have changed)
3. **Proxies not working?** → Enable validation in config.py
4. **Want different data?** → Edit yellowpages_scraper.py to extract more fields

## Example Output

```csv
name,phone,street,city,state,zip,website,categories,rating,search_category
ABC Building Supply,(305) 555-0100,123 Main St,Miami,FL,33101,https://abc.com,Building Materials,4.5/5,building supply
XYZ Lumber Co,(305) 555-0200,456 Oak Ave,Miami,FL,33102,,Lumber Yard,4.0/5,lumber
```

## What's Next?

- Customize search categories in `config.py`
- Add proxies to avoid IP bans
- Increase `MAX_PAGES_PER_SEARCH` for more results
- Export to database instead of CSV (modify scraper)
- Schedule regular scrapes with cron/Task Scheduler

Happy scraping! 🚀

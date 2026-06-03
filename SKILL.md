# Skill: Yellow Pages Scraper CLI (yp-cli.py)

## What It Does
`yp-cli.py` is a command-line interface for the Yellow Pages Scraper API. It handles authentication, job submission, progress monitoring, result downloading, and AI-powered keyword suggestions. Located at `/home/mike/yellow-pages-scraper/yp-cli.py`.

## Prerequisites
- Python 3 with `requests` installed (`pip install requests`)
- A running Yellow Pages Scraper API instance (default: http://localhost:5001)

## Authentication
Always login first. The session is saved to `~/.yp-scraper/session` and reused automatically.

```bash
python3 /home/mike/yellow-pages-scraper/yp-cli.py login --user mike --password changeme123
# With a custom URL (also saved for future commands):
python3 /home/mike/yellow-pages-scraper/yp-cli.py login --url https://scraper.example.com --user mike --password changeme123
```

## Running a Scrape

### Fire-and-forget (returns job_id immediately):
```bash
python3 /home/mike/yellow-pages-scraper/yp-cli.py scrape --keywords "plumbers,electricians" --locations "Miami FL,Houston TX" --pages 2 --concurrent 100
```

### Wait for completion and auto-download:
```bash
python3 /home/mike/yellow-pages-scraper/yp-cli.py scrape --keywords "plumbers" --locations "Miami FL" --pages 5 --concurrent 50 --proxies --wait --output results.csv
```

### Key flags:
- `--keywords` (required): Comma-separated business categories
- `--locations` (required): Comma-separated "City ST" locations
- `--pages`: Max result pages per search (default: 10)
- `--concurrent`: Parallel browser instances (default: 1, max: 500)
- `--proxies`: Enable proxy rotation
- `--wait`: Block until job completes, show progress, auto-download
- `--output/-o`: Output file path (with --wait)

## Checking Status
```bash
python3 /home/mike/yellow-pages-scraper/yp-cli.py status
python3 /home/mike/yellow-pages-scraper/yp-cli.py status --job-id abc123
```

## Listing Results
```bash
python3 /home/mike/yellow-pages-scraper/yp-cli.py results
```

## Downloading Results
```bash
# Download latest result:
python3 /home/mike/yellow-pages-scraper/yp-cli.py download
# Download specific job's result:
python3 /home/mike/yellow-pages-scraper/yp-cli.py download --job-id abc123 --output ./my_leads.csv
# Download specific file:
python3 /home/mike/yellow-pages-scraper/yp-cli.py download --file scrape_results_20260603_120000.csv
```

## AI Suggestions
```bash
python3 /home/mike/yellow-pages-scraper/yp-cli.py suggest --icp "roofing companies in the southeast US"
```
Returns suggested keywords and locations. Requires a configured Grok/xAI API key on the server.

## JSON Output
Add `--json` to any command for machine-parseable output:
```bash
python3 /home/mike/yellow-pages-scraper/yp-cli.py --json status
python3 /home/mike/yellow-pages-scraper/yp-cli.py --json results
python3 /home/mike/yellow-pages-scraper/yp-cli.py --json scrape --keywords "plumbers" --locations "Miami FL" --wait
```

## Common Patterns for AI Agents

### Full scrape workflow:
```bash
python3 /home/mike/yellow-pages-scraper/yp-cli.py login --user mike --password changeme123
python3 /home/mike/yellow-pages-scraper/yp-cli.py --json scrape --keywords "plumbers" --locations "Miami FL" --pages 3 --concurrent 50 --proxies --wait --output /tmp/leads.csv
```

### Check if a job is still running:
```bash
python3 /home/mike/yellow-pages-scraper/yp-cli.py --json status
# Look for "running": true/false in output
```

### Get suggestions then scrape:
```bash
SUGGESTIONS=$(python3 /home/mike/yellow-pages-scraper/yp-cli.py --json suggest --icp "HVAC contractors in Texas")
# Parse keywords and locations from JSON, then pass to scrape command
```

## Error Handling
- Exit code 0 = success
- Exit code 1 = error (message printed to stderr with "ERROR:" prefix)
- "Not logged in" errors: re-run the login command
- Connection errors: verify the API URL and that the server is running

## Configuration Files
- `~/.yp-scraper/session` - saved auth cookies (auto-created by login)
- `~/.yp-scraper/config` - saved base URL and preferences

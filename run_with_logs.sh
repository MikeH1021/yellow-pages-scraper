#!/bin/bash
# Run scraper with logs saved to file

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOGFILE="scraper_${TIMESTAMP}.log"

echo "Starting scraper..."
echo "Logs will be saved to: $LOGFILE"
echo "Press Ctrl+C to stop"
echo ""

# Run and save logs to file AND show in terminal
python run_scraper.py 2>&1 | tee "$LOGFILE"

echo ""
echo "Scraping complete!"
echo "Logs saved to: $LOGFILE"

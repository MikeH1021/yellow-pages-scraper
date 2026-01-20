#!/bin/bash

# Start Yellow Pages Scraper Web UI
# Quick launcher script

cd "/Users/jonathangarces/Desktop/yellow page scraper"

echo "════════════════════════════════════════════════════════════════"
echo "  Yellow Pages Scraper - Web UI Launcher"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start web server
echo "Starting web server..."
echo ""
echo "🌐 Open your browser to: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

python web_app.py

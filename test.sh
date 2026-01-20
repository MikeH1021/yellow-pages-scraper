#!/bin/bash
# Helper script - automatically activates venv and runs tests

cd "$(dirname "$0")"
source venv/bin/activate
python test_scraper.py

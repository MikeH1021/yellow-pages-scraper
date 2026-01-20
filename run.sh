#!/bin/bash
# Helper script - automatically activates venv and runs the scraper

cd "$(dirname "$0")"
source venv/bin/activate
python run_scraper.py

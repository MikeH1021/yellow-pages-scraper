#!/bin/bash

echo "=================================="
echo "Yellow Pages Scraper Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

echo ""
echo "=================================="
echo "Setup complete!"
echo "=================================="
echo ""
echo "To start using the scraper:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Edit config.py to customize your searches"
echo "  3. Run the scraper: python run_scraper.py"
echo ""
echo "For a simple example: python example_simple.py"
echo ""

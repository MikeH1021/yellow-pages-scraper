"""
Configuration file for Yellow Pages Scraper
Modify these settings to customize scraper behavior
"""

# Browser settings
HEADLESS_MODE = False  # Set to True to run browser in background
DELAY_BETWEEN_PAGES = 2.0  # Seconds to wait between page loads (increase if getting blocked)

# Scraping settings
MAX_PAGES_PER_SEARCH = 3  # Maximum pages to scrape per category
TIMEOUT_MS = 30000  # Page load timeout in milliseconds

# Search categories and locations
# Format: {"term": "search term", "location": "City, State" or "United States"}
SEARCH_CATEGORIES = [
    {"term": "building supply", "location": "United States"},
    {"term": "shutters", "location": "United States"},
    {"term": "millwork", "location": "United States"},
    {"term": "lumber", "location": "United States"},
    {"term": "architects", "location": "United States"},
]

# You can also search specific locations:
# SEARCH_CATEGORIES = [
#     {"term": "building supply", "location": "Miami, FL"},
#     {"term": "shutters", "location": "New York, NY"},
#     {"term": "lumber", "location": "Los Angeles, CA"},
# ]

# Output settings
SAVE_INDIVIDUAL_CATEGORIES = True  # Save separate CSV for each category
SAVE_COMBINED_RESULTS = True  # Save one CSV with all results
SAVE_EASTERN_STATES_ONLY = True  # Save filtered results for eastern states

# Output directory (leave empty for current directory)
OUTPUT_DIR = ""

# States east of Colorado (for filtering)
EASTERN_STATES = [
    'AL', 'AR', 'CT', 'DE', 'FL', 'GA', 'IL', 'IN', 'IA', 'KS', 'KY',
    'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'NE', 'NH', 'NJ',
    'NY', 'NC', 'ND', 'OH', 'OK', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
    'VT', 'VA', 'WV', 'WI', 'DC'
]

# Proxy settings (to avoid IP bans)
USE_PROXIES = False  # Set to True to enable proxy rotation
PROXY_FILE = "proxies.txt"  # Path to proxy list file
VALIDATE_PROXIES = True  # Validate proxies before use (slower startup)

# Paid proxy service settings (alternative to proxy file)
# Set these in environment variables for security:
# export PROXY_SERVICE="smartproxy"  # Options: brightdata, smartproxy, oxylabs, proxyrack
# export PROXY_USERNAME="your-username"
# export PROXY_PASSWORD="your-password"
USE_PAID_PROXY_SERVICE = False
PROXY_SERVICE = None  # Will be read from environment if USE_PAID_PROXY_SERVICE is True
PROXY_USERNAME = None  # Will be read from environment
PROXY_PASSWORD = None  # Will be read from environment

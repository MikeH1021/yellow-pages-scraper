"""
Configuration for scraping TOP CITIES (Recommended Strategy)
This targets major metropolitan areas for maximum business coverage
"""

# Browser settings
HEADLESS_MODE = True
DELAY_BETWEEN_PAGES = 3.0  # 3 seconds - safe with proxies
MAX_PAGES_PER_SEARCH = 10  # 10 pages per city

# Top 50 Eastern Cities by Population & Business Activity
# These cities account for ~70-80% of all businesses
TOP_CITIES_EASTERN = [
    # Tier 1: Mega Cities (1M+ population)
    "New York, NY",
    "Chicago, IL",
    "Houston, TX",
    "Philadelphia, PA",
    "San Antonio, TX",
    "Dallas, TX",
    "Austin, TX",

    # Tier 2: Major Cities (500K-1M)
    "Jacksonville, FL",
    "Fort Worth, TX",
    "Columbus, OH",
    "Charlotte, NC",
    "Detroit, MI",
    "Memphis, TN",
    "Baltimore, MD",
    "Boston, MA",
    "Nashville, TN",
    "Oklahoma City, OK",
    "Louisville, KY",
    "Milwaukee, WI",

    # Tier 3: Large Cities (250K-500K)
    "Atlanta, GA",
    "Miami, FL",
    "Minneapolis, MN",
    "Tulsa, OK",
    "Cleveland, OH",
    "Wichita, KS",
    "New Orleans, LA",
    "Tampa, FL",
    "Raleigh, NC",
    "Omaha, NE",
    "Virginia Beach, VA",
    "Arlington, TX",
    "Pittsburgh, PA",
    "Cincinnati, OH",
    "Lexington, KY",
    "St. Louis, MO",
    "Orlando, FL",
    "Durham, NC",
    "Jersey City, NJ",
    "Buffalo, NY",
    "Richmond, VA",
    "Madison, WI",
    "Des Moines, IA",
    "Birmingham, AL",
    "Baton Rouge, LA",
    "Little Rock, AR",
    "Hartford, CT",
    "Manchester, NH",
    "Providence, RI",
]

# Alternative: Top 25 cities for faster testing
TOP_25_CITIES = TOP_CITIES_EASTERN[:25]

# Alternative: Top 10 for quick pilot
TOP_10_CITIES = TOP_CITIES_EASTERN[:10]

# Business categories to scrape
CATEGORIES = [
    "building supply",
    "shutters",
    "millwork",
    "lumber",
    "architects"
]

# Build search list: City × Category
# For top 50 cities: 50 × 5 = 250 searches
# For top 25 cities: 25 × 5 = 125 searches
# For top 10 cities: 10 × 5 = 50 searches

# Choose your scope:
# Load Top 100 cities from file
with open('cities_top_100.txt') as f:
    CITY_LIST = [line.strip() for line in f
                 if not line.startswith('#') and line.strip()]

# Alternative: Use built-in lists
# CITY_LIST = TOP_25_CITIES  # 25 cities
# CITY_LIST = TOP_CITIES_EASTERN  # 50 cities

SEARCH_CATEGORIES = []
for city in CITY_LIST:
    for category in CATEGORIES:
        SEARCH_CATEGORIES.append({
            "term": category,
            "location": city
        })

# Output settings
SAVE_INDIVIDUAL_CATEGORIES = True
SAVE_COMBINED_RESULTS = True
SAVE_EASTERN_STATES_ONLY = False  # Already filtered by eastern cities
OUTPUT_DIR = ""

# Proxy settings (CRITICAL for this many searches)
USE_PROXIES = True  # Using Webshare proxies
PROXY_FILE = "proxies.txt"
VALIDATE_PROXIES = False  # Skip validation, Webshare proxies are pre-verified

# Paid proxy service (not needed - using file-based proxies)
USE_PAID_PROXY_SERVICE = False
PROXY_SERVICE = None
PROXY_USERNAME = None
PROXY_PASSWORD = None

# Progress tracking
print(f"""
╔════════════════════════════════════════════════════════════════╗
║              TOP CITIES SCRAPING CONFIGURATION                 ║
╠════════════════════════════════════════════════════════════════╣
║  Cities to scrape: {len(CITY_LIST):<40}  ║
║  Categories: {len(CATEGORIES):<48}  ║
║  Total searches: {len(SEARCH_CATEGORIES):<44}  ║
║  Pages per search: {MAX_PAGES_PER_SEARCH:<42}  ║
║  Total pages: ~{len(SEARCH_CATEGORIES) * MAX_PAGES_PER_SEARCH:<45}  ║
║                                                                ║
║  Estimated time: {len(SEARCH_CATEGORIES) * MAX_PAGES_PER_SEARCH * 6 / 60:.0f} minutes ({len(SEARCH_CATEGORIES) * MAX_PAGES_PER_SEARCH * 6 / 3600:.1f} hours)                   ║
║  Using proxies: {str(USE_PROXIES):<46}  ║
╚════════════════════════════════════════════════════════════════╝
""")

# States east of Colorado (for reference, though not used with city targeting)
EASTERN_STATES = [
    'AL', 'AR', 'CT', 'DE', 'FL', 'GA', 'IL', 'IN', 'IA', 'KS', 'KY',
    'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'NE', 'NH', 'NJ',
    'NY', 'NC', 'ND', 'OH', 'OK', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
    'VT', 'VA', 'WV', 'WI', 'DC'
]

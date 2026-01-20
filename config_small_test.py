"""
Configuration for SMALL TEST RUN
Target: ~500 businesses (2-3 cities, all categories)
Time: ~10-15 minutes
"""

# Browser settings
HEADLESS_MODE = True
DELAY_BETWEEN_PAGES = 3.0
MAX_PAGES_PER_SEARCH = 10

# Just 2 cities for quick test
TEST_CITIES = [
    "Miami, FL",      # Large city with lots of businesses
    "Chicago, IL",    # Another major city
]

# All 5 categories
CATEGORIES = [
    "building supply",
    "shutters",
    "millwork",
    "lumber",
    "architects"
]

# Build search list
SEARCH_CATEGORIES = []
for city in TEST_CITIES:
    for category in CATEGORIES:
        SEARCH_CATEGORIES.append({
            "term": category,
            "location": city
        })

# Output settings
SAVE_INDIVIDUAL_CATEGORIES = True
SAVE_COMBINED_RESULTS = True
SAVE_EASTERN_STATES_ONLY = False
OUTPUT_DIR = ""

# Proxy settings - Using Webshare proxies
USE_PROXIES = True
PROXY_FILE = "proxies.txt"
VALIDATE_PROXIES = False  # Skip validation

# Not using paid proxy service
USE_PAID_PROXY_SERVICE = False
PROXY_SERVICE = None
PROXY_USERNAME = None
PROXY_PASSWORD = None

# Progress tracking
print(f"""
╔════════════════════════════════════════════════════════════════╗
║              SMALL TEST RUN CONFIGURATION                      ║
╠════════════════════════════════════════════════════════════════╣
║  Cities to scrape: {len(TEST_CITIES):<44}║
║  Categories: {len(CATEGORIES):<48}║
║  Total searches: {len(SEARCH_CATEGORIES):<44}║
║  Pages per search: {MAX_PAGES_PER_SEARCH:<42}║
║  Total pages: ~{len(SEARCH_CATEGORIES) * MAX_PAGES_PER_SEARCH:<45}║
║                                                                ║
║  Expected businesses: ~500                                     ║
║  Estimated time: {len(SEARCH_CATEGORIES) * MAX_PAGES_PER_SEARCH * 6 / 60:.0f} minutes                                    ║
║  Using proxies: {str(USE_PROXIES):<46}║
╚════════════════════════════════════════════════════════════════╝
""")

# States east of Colorado (for reference)
EASTERN_STATES = [
    'AL', 'AR', 'CT', 'DE', 'FL', 'GA', 'IL', 'IN', 'IA', 'KS', 'KY',
    'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'NE', 'NH', 'NJ',
    'NY', 'NC', 'ND', 'OH', 'OK', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
    'VT', 'VA', 'WV', 'WI', 'DC'
]

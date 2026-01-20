# Yellow Pages HTML Structure Notes

This document explains the HTML structure of Yellow Pages and how to update the scraper if the website changes.

## Current Page Structure Analysis

### URL Pattern

```
https://www.yellowpages.com/search?search_terms={term}&geo_location_terms={location}&page={num}
```

Example:
```
https://www.yellowpages.com/search?search_terms=building+supply&geo_location_terms=Miami%2C+FL
```

### Business Listings Container

Business listings are typically found in:
- `<div class="result">` - Individual business result
- `<div class="search-results organic">` - Container for organic results

### Data Fields and Their Selectors

#### 1. Business Name
```html
<a class="business-name" ...>Company Name</a>
```
**Scraper location:** `yellowpages_scraper.py:126`
```python
name_elem = listing.find('a', class_='business-name')
```

#### 2. Phone Number
```html
<div class="phones phone primary">
    (123) 456-7890
</div>
```
**Scraper location:** `yellowpages_scraper.py:132`
```python
phone_elem = listing.find('div', class_='phones')
```

#### 3. Street Address
```html
<div class="street-address">123 Main Street</div>
```
**Scraper location:** `yellowpages_scraper.py:138`
```python
street_elem = listing.find('div', class_='street-address')
```

#### 4. City, State, ZIP
```html
<div class="locality">Miami, FL 33101</div>
```
**Scraper location:** `yellowpages_scraper.py:143`
```python
locality_elem = listing.find('div', class_='locality')
```

#### 5. Website Link
```html
<a class="track-visit-website" href="...">Website</a>
```
**Scraper location:** `yellowpages_scraper.py:163`
```python
website_elem = listing.find('a', class_='track-visit-website')
```

#### 6. Categories
```html
<div class="categories">
    <a>Building Materials</a>
    <a>Hardware Stores</a>
</div>
```
**Scraper location:** `yellowpages_scraper.py:169`
```python
categories_elem = listing.find('div', class_='categories')
```

#### 7. Rating
```html
<div class="result-rating">
    <div class="stars">★★★★☆</div>
    <div class="count">(25)</div>
</div>
```
**Scraper location:** `yellowpages_scraper.py:175`
```python
rating_elem = listing.find('div', class_='result-rating')
```

#### 8. Years in Business
```html
<div class="years-in-business">
    <span>15</span> Years in Business
</div>
```
**Scraper location:** `yellowpages_scraper.py:181`
```python
yib_elem = listing.find('div', class_='years-in-business')
```

## Common Structure Variations

Yellow Pages may use different class names or structures depending on:
1. Whether you're logged in
2. Your geographic location
3. A/B testing
4. Mobile vs desktop view

### Alternative Selectors to Try

If the current selectors don't work, try these alternatives:

```python
# Business listings
listings = soup.find_all('div', class_='info')
listings = soup.find_all('div', {'data-advertising': 'false'})
listings = soup.find_all('article')

# Business name
name_elem = listing.find('h2', class_='n')
name_elem = listing.find('a', class_='n')

# Phone
phone_elem = listing.find('p', class_='phone')
phone_elem = listing.find('div', class_='phone')

# Address
street_elem = listing.find('p', class_='adr')
street_elem = listing.find('span', itemprop='streetAddress')
```

## How to Update Selectors

If Yellow Pages changes their HTML structure:

### Step 1: Inspect the Page

1. Visit Yellow Pages in a browser
2. Search for a test term (e.g., "building supply Miami FL")
3. Right-click on a business listing → "Inspect Element"
4. Note the HTML structure

### Step 2: Update the Scraper

Edit `yellowpages_scraper.py` and update the methods:

**For listing containers** (line ~103):
```python
async def _extract_businesses(self, page: Page) -> List[Dict]:
    # Update these selectors
    listings = soup.find_all('div', class_='NEW_CLASS_NAME')
```

**For individual fields** (line ~119):
```python
def _parse_listing(self, listing) -> Optional[Dict]:
    # Update each field's selector
    name_elem = listing.find('a', class_='NEW_CLASS_NAME')
```

### Step 3: Test

Run the simple example to test:
```bash
python example_simple.py
```

## Debugging Tips

### Enable verbose output
Add print statements to see what's being extracted:

```python
def _parse_listing(self, listing) -> Optional[Dict]:
    print("Raw HTML:", listing.prettify()[:500])  # First 500 chars
    # ... rest of code
```

### Save HTML for inspection
Add to `_extract_businesses()`:

```python
with open('debug_page.html', 'w') as f:
    f.write(content)
```

### Check what's being found
```python
print(f"Found {len(listings)} listings")
for i, listing in enumerate(listings[:3]):
    print(f"Listing {i}: {listing.get_text()[:100]}")
```

## Anti-Scraping Measures

Yellow Pages may block scraping attempts. Signs include:

1. **403 Forbidden errors** - IP blocked
2. **CAPTCHA pages** - Bot detection triggered
3. **Empty results** - Content not loading
4. **Different HTML** - Serving alternate version

### Solutions

1. **Increase delay**: Change `delay=2.0` to `delay=5.0` or higher
2. **Use proxies**: Rotate IP addresses (requires additional setup)
3. **Randomize user agents**: Add to browser context
4. **Scrape during off-hours**: Less likely to trigger rate limits
5. **Respect robots.txt**: Check `https://www.yellowpages.com/robots.txt`

### Adding Proxy Support

To add proxy support, modify the browser launch:

```python
self.browser = await self.playwright.chromium.launch(
    headless=self.headless,
    proxy={
        "server": "http://proxy-server:port",
        "username": "user",
        "password": "pass"
    }
)
```

## Legal and Ethical Considerations

1. **Terms of Service**: Review Yellow Pages TOS before scraping
2. **Rate Limiting**: Don't overwhelm their servers
3. **Data Usage**: Respect privacy and business information
4. **Attribution**: Give credit if publishing scraped data
5. **Commercial Use**: May require permission

## Contact

If you need to update this scraper significantly, the key files are:
- `yellowpages_scraper.py` - Main scraper class
- `config.py` - Configuration settings
- This file - Documentation

Good luck!

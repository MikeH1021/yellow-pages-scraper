"""
Generate comprehensive city lists for all eastern states
Creates exhaustive lists by population tier
"""

# Eastern states (states east of Colorado)
EASTERN_STATES = {
    'AL': 'Alabama', 'AR': 'Arkansas', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'IL': 'Illinois', 'IN': 'Indiana',
    'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
    'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'NE': 'Nebraska',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'VT': 'Vermont',
    'VA': 'Virginia', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'DC': 'District of Columbia'
}

# Comprehensive city list by state (Top 5+ cities per state)
# Population data from 2020-2024 estimates
ALL_EASTERN_CITIES = {
    'FL': [
        'Jacksonville', 'Miami', 'Tampa', 'Orlando', 'St. Petersburg',
        'Hialeah', 'Port St. Lucie', 'Cape Coral', 'Tallahassee', 'Fort Lauderdale',
        'Pembroke Pines', 'Hollywood', 'Miramar', 'Coral Springs', 'Clearwater',
        'Palm Bay', 'Lakeland', 'Pompano Beach', 'West Palm Beach', 'Davie'
    ],
    'NY': [
        'New York', 'Buffalo', 'Rochester', 'Yonkers', 'Syracuse',
        'Albany', 'New Rochelle', 'Mount Vernon', 'Schenectady', 'Utica',
        'White Plains', 'Hempstead', 'Troy', 'Niagara Falls', 'Binghamton'
    ],
    'TX': [
        'Houston', 'San Antonio', 'Dallas', 'Austin', 'Fort Worth',
        'El Paso', 'Arlington', 'Corpus Christi', 'Plano', 'Laredo',
        'Lubbock', 'Garland', 'Irving', 'Amarillo', 'Grand Prairie',
        'McKinney', 'Frisco', 'Pasadena', 'Killeen', 'McAllen'
    ],
    'PA': [
        'Philadelphia', 'Pittsburgh', 'Allentown', 'Erie', 'Reading',
        'Scranton', 'Bethlehem', 'Lancaster', 'Harrisburg', 'Altoona',
        'York', 'State College', 'Wilkes-Barre'
    ],
    'IL': [
        'Chicago', 'Aurora', 'Naperville', 'Joliet', 'Rockford',
        'Springfield', 'Elgin', 'Peoria', 'Champaign', 'Waukegan',
        'Cicero', 'Bloomington', 'Decatur', 'Evanston'
    ],
    'OH': [
        'Columbus', 'Cleveland', 'Cincinnati', 'Toledo', 'Akron',
        'Dayton', 'Parma', 'Canton', 'Youngstown', 'Lorain',
        'Hamilton', 'Springfield', 'Kettering', 'Elyria'
    ],
    'GA': [
        'Atlanta', 'Augusta', 'Columbus', 'Macon', 'Savannah',
        'Athens', 'Sandy Springs', 'Roswell', 'Johns Creek', 'Albany',
        'Warner Robins', 'Alpharetta', 'Marietta', 'Valdosta'
    ],
    'NC': [
        'Charlotte', 'Raleigh', 'Greensboro', 'Durham', 'Winston-Salem',
        'Fayetteville', 'Cary', 'Wilmington', 'High Point', 'Concord',
        'Greenville', 'Asheville', 'Gastonia', 'Jacksonville'
    ],
    'MI': [
        'Detroit', 'Grand Rapids', 'Warren', 'Sterling Heights', 'Ann Arbor',
        'Lansing', 'Flint', 'Dearborn', 'Livonia', 'Troy',
        'Westland', 'Farmington Hills', 'Kalamazoo', 'Wyoming'
    ],
    'VA': [
        'Virginia Beach', 'Norfolk', 'Chesapeake', 'Richmond', 'Newport News',
        'Alexandria', 'Hampton', 'Roanoke', 'Portsmouth', 'Suffolk',
        'Lynchburg', 'Harrisonburg', 'Charlottesville', 'Danville'
    ],
    'TN': [
        'Nashville', 'Memphis', 'Knoxville', 'Chattanooga', 'Clarksville',
        'Murfreesboro', 'Jackson', 'Johnson City', 'Franklin', 'Bartlett',
        'Hendersonville', 'Kingsport', 'Collierville'
    ],
    'MA': [
        'Boston', 'Worcester', 'Springfield', 'Cambridge', 'Lowell',
        'Brockton', 'Quincy', 'Lynn', 'New Bedford', 'Fall River',
        'Newton', 'Somerville', 'Lawrence', 'Framingham'
    ],
    'IN': [
        'Indianapolis', 'Fort Wayne', 'Evansville', 'South Bend', 'Carmel',
        'Bloomington', 'Fishers', 'Hammond', 'Gary', 'Muncie',
        'Lafayette', 'Terre Haute', 'Kokomo', 'Anderson'
    ],
    'MO': [
        'Kansas City', 'St. Louis', 'Springfield', 'Columbia', 'Independence',
        'Lee\'s Summit', 'O\'Fallon', 'St. Joseph', 'St. Charles', 'Blue Springs',
        'Joplin', 'Jefferson City'
    ],
    'WI': [
        'Milwaukee', 'Madison', 'Green Bay', 'Kenosha', 'Racine',
        'Appleton', 'Waukesha', 'Eau Claire', 'Oshkosh', 'Janesville',
        'West Allis', 'La Crosse'
    ],
    'MD': [
        'Baltimore', 'Columbia', 'Germantown', 'Silver Spring', 'Waldorf',
        'Glen Burnie', 'Ellicott City', 'Frederick', 'Rockville', 'Gaithersburg',
        'Bowie', 'Annapolis'
    ],
    'MN': [
        'Minneapolis', 'St. Paul', 'Rochester', 'Duluth', 'Bloomington',
        'Brooklyn Park', 'Plymouth', 'St. Cloud', 'Eagan', 'Woodbury',
        'Maple Grove', 'Eden Prairie'
    ],
    'SC': [
        'Charleston', 'Columbia', 'North Charleston', 'Mount Pleasant', 'Rock Hill',
        'Greenville', 'Summerville', 'Sumter', 'Goose Creek', 'Hilton Head Island',
        'Florence', 'Spartanburg'
    ],
    'AL': [
        'Birmingham', 'Montgomery', 'Mobile', 'Huntsville', 'Tuscaloosa',
        'Hoover', 'Dothan', 'Auburn', 'Decatur', 'Madison',
        'Florence', 'Gadsden'
    ],
    'LA': [
        'New Orleans', 'Baton Rouge', 'Shreveport', 'Lafayette', 'Lake Charles',
        'Kenner', 'Bossier City', 'Monroe', 'Alexandria', 'Houma',
        'Metairie', 'Slidell'
    ],
    'KY': [
        'Louisville', 'Lexington', 'Bowling Green', 'Owensboro', 'Covington',
        'Richmond', 'Georgetown', 'Florence', 'Hopkinsville', 'Nicholasville',
        'Elizabethtown', 'Frankfort'
    ],
    'OK': [
        'Oklahoma City', 'Tulsa', 'Norman', 'Broken Arrow', 'Edmond',
        'Lawton', 'Moore', 'Midwest City', 'Enid', 'Stillwater',
        'Muskogee', 'Bartlesville'
    ],
    'CT': [
        'Bridgeport', 'New Haven', 'Stamford', 'Hartford', 'Waterbury',
        'Norwalk', 'Danbury', 'New Britain', 'West Hartford', 'Greenwich',
        'Hamden', 'Meriden'
    ],
    'IA': [
        'Des Moines', 'Cedar Rapids', 'Davenport', 'Sioux City', 'Iowa City',
        'Waterloo', 'Council Bluffs', 'Ames', 'West Des Moines', 'Dubuque',
        'Ankeny', 'Cedar Falls'
    ],
    'MS': [
        'Jackson', 'Gulfport', 'Southaven', 'Hattiesburg', 'Biloxi',
        'Meridian', 'Tupelo', 'Greenville', 'Olive Branch', 'Horn Lake',
        'Clinton', 'Pearl'
    ],
    'AR': [
        'Little Rock', 'Fort Smith', 'Fayetteville', 'Springdale', 'Jonesboro',
        'North Little Rock', 'Conway', 'Rogers', 'Pine Bluff', 'Bentonville',
        'Hot Springs', 'Benton'
    ],
    'KS': [
        'Wichita', 'Overland Park', 'Kansas City', 'Olathe', 'Topeka',
        'Lawrence', 'Shawnee', 'Manhattan', 'Lenexa', 'Salina',
        'Hutchinson', 'Leavenworth'
    ],
    'NE': [
        'Omaha', 'Lincoln', 'Bellevue', 'Grand Island', 'Kearney',
        'Fremont', 'Hastings', 'Norfolk', 'Columbus', 'Papillion',
        'North Platte', 'La Vista'
    ],
    'NJ': [
        'Newark', 'Jersey City', 'Paterson', 'Elizabeth', 'Trenton',
        'Clifton', 'Camden', 'Passaic', 'Union City', 'Bayonne',
        'East Orange', 'Vineland', 'New Brunswick', 'Hoboken'
    ],
    'RI': ['Providence', 'Warwick', 'Cranston', 'Pawtucket', 'East Providence',
           'Woonsocket', 'Coventry', 'Cumberland'],
    'NH': ['Manchester', 'Nashua', 'Concord', 'Derry', 'Rochester',
           'Salem', 'Dover', 'Merrimack', 'Londonderry'],
    'ME': ['Portland', 'Lewiston', 'Bangor', 'South Portland', 'Auburn',
           'Biddeford', 'Sanford', 'Augusta', 'Saco'],
    'VT': ['Burlington', 'South Burlington', 'Rutland', 'Barre', 'Montpelier',
           'Winooski', 'St. Albans', 'Newport'],
    'DE': ['Wilmington', 'Dover', 'Newark', 'Middletown', 'Smyrna',
           'Milford', 'Seaford', 'Georgetown'],
    'WV': ['Charleston', 'Huntington', 'Morgantown', 'Parkersburg', 'Wheeling',
           'Weirton', 'Fairmont', 'Martinsburg', 'Beckley'],
    'ND': ['Fargo', 'Bismarck', 'Grand Forks', 'Minot', 'West Fargo',
           'Williston', 'Dickinson', 'Mandan'],
    'SD': ['Sioux Falls', 'Rapid City', 'Aberdeen', 'Brookings', 'Watertown',
           'Mitchell', 'Yankton', 'Pierre'],
    'DC': ['Washington']
}


def generate_city_list(tier='all'):
    """
    Generate formatted city list for Yellow Pages scraping

    Args:
        tier: 'top50', 'top100', 'top200', 'all'

    Returns:
        List of "City, ST" formatted strings
    """
    cities = []

    for state_code, state_cities in ALL_EASTERN_CITIES.items():
        for city in state_cities:
            cities.append(f"{city}, {state_code}")

    # Total available
    print(f"Total cities available: {len(cities)}")

    if tier == 'top50':
        return cities[:50]
    elif tier == 'top100':
        return cities[:100]
    elif tier == 'top200':
        return cities[:200]
    else:
        return cities


def show_breakdown():
    """Show breakdown by state"""
    print("\n" + "="*60)
    print("CITY BREAKDOWN BY STATE")
    print("="*60)

    total = 0
    for state_code, cities in sorted(ALL_EASTERN_CITIES.items()):
        state_name = EASTERN_STATES[state_code]
        print(f"{state_code} ({state_name:20s}): {len(cities):3d} cities")
        total += len(cities)

    print("="*60)
    print(f"TOTAL: {total} cities across {len(ALL_EASTERN_CITIES)} states")
    print("="*60)


def save_to_file(filename, tier='all'):
    """Save city list to file"""
    cities = generate_city_list(tier)

    with open(filename, 'w') as f:
        f.write("# City list for Yellow Pages scraping\n")
        f.write(f"# Tier: {tier}\n")
        f.write(f"# Total cities: {len(cities)}\n")
        f.write("# Format: City, ST\n\n")

        for city in cities:
            f.write(f"{city}\n")

    print(f"\n✓ Saved {len(cities)} cities to {filename}")


if __name__ == "__main__":
    print("=" * 60)
    print("EASTERN STATES CITY LIST GENERATOR")
    print("=" * 60)

    show_breakdown()

    print("\nGenerating city lists...")

    # Save different tiers
    save_to_file('cities_top_50.txt', 'top50')
    save_to_file('cities_top_100.txt', 'top100')
    save_to_file('cities_top_200.txt', 'top200')
    save_to_file('cities_all.txt', 'all')

    print("\n" + "=" * 60)
    print("FILES CREATED:")
    print("=" * 60)
    print("  cities_top_50.txt   - Top 50 cities (fastest)")
    print("  cities_top_100.txt  - Top 100 cities (balanced)")
    print("  cities_top_200.txt  - Top 200 cities (comprehensive)")
    print("  cities_all.txt      - All cities (exhaustive)")
    print("=" * 60)

    print("\nUSAGE:")
    print("  Edit config_top_cities.py and load from file:")
    print("  with open('cities_top_100.txt') as f:")
    print("      CITY_LIST = [line.strip() for line in f if not line.startswith('#')]")
    print("="* 60)

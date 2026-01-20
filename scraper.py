import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from database import insert_daily_rice, get_db

STATS_URL = 'https://engine.freerice.com/stats/rice/daily.html'

def fetch_daily_stats():
    """Fetch the daily rice stats HTML table"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(STATS_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return None

def parse_stats_table(html):
    """Parse the HTML table and return list of {date, grains}"""
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    if not table:
        print("No table found in HTML")
        return []

    data = []
    rows = table.find_all('tr')[1:]  # Skip header row

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            date_str = cols[0].text.strip()
            grains_str = cols[1].text.strip()

            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                grains = int(grains_str)
                data.append({'date': date, 'grains': grains})
            except ValueError as e:
                print(f"Error parsing row: {date_str}, {grains_str} - {e}")

    return data

def fetch_and_import_yesterday():
    """Fetch yesterday's data and import if not already exists"""
    html = fetch_daily_stats()
    if not html:
        print("Failed to fetch stats")
        return False

    data = parse_stats_table(html)
    if not data:
        print("No data parsed from stats")
        return False

    # Get yesterday's date
    yesterday = (datetime.now() - timedelta(days=1)).date()

    # Find yesterday's data
    yesterday_data = None
    for entry in data:
        if entry['date'] == yesterday:
            yesterday_data = entry
            break

    if not yesterday_data:
        print(f"No data found for {yesterday}")
        return False

    # Check if already exists
    with get_db() as conn:
        existing = conn.execute(
            'SELECT date FROM daily_rice_consumption WHERE date = ?',
            (str(yesterday),)
        ).fetchone()

        if existing:
            print(f"Data for {yesterday} already exists")
            return False

    # Insert the data
    insert_daily_rice(str(yesterday), yesterday_data['grains'], source='auto')
    print(f"Imported {yesterday}: {yesterday_data['grains']:,} grains")
    return True

def fetch_and_import_missing():
    """Fetch all missing data from most recent DB entry to yesterday"""
    # Get the most recent date in the database
    with get_db() as conn:
        result = conn.execute(
            'SELECT MAX(date) as max_date FROM daily_rice_consumption'
        ).fetchone()

        if result and result['max_date']:
            last_date = datetime.strptime(result['max_date'], '%Y-%m-%d').date()
        else:
            # No data in DB, start from a default date
            last_date = datetime(2024, 1, 1).date()

    # Calculate yesterday
    yesterday = (datetime.now() - timedelta(days=1)).date()

    # If we're already up to date
    if last_date >= yesterday:
        print(f"Already up to date! Last entry: {last_date}")
        return 0

    # Fetch all data from website
    html = fetch_daily_stats()
    if not html:
        print("Failed to fetch stats")
        return 0

    data = parse_stats_table(html)
    if not data:
        print("No data parsed from stats")
        return 0

    # Create a dict for quick lookup
    data_by_date = {entry['date']: entry['grains'] for entry in data}

    # Import all missing days
    imported = 0
    current_date = last_date + timedelta(days=1)

    while current_date <= yesterday:
        if current_date in data_by_date:
            # Check if already exists (shouldn't, but be safe)
            with get_db() as conn:
                existing = conn.execute(
                    'SELECT date FROM daily_rice_consumption WHERE date = ?',
                    (str(current_date),)
                ).fetchone()

                if not existing:
                    insert_daily_rice(str(current_date), data_by_date[current_date], source='auto')
                    print(f"Imported {current_date}: {data_by_date[current_date]:,} grains")
                    imported += 1
        else:
            print(f"Warning: No data found for {current_date}")

        current_date += timedelta(days=1)

    print(f"Imported {imported} missing days")
    return imported

def import_historical_data(start_date, end_date=None):
    """Import all historical data between dates"""
    html = fetch_daily_stats()
    if not html:
        print("Failed to fetch stats")
        return 0

    data = parse_stats_table(html)
    if not data:
        print("No data parsed from stats")
        return 0

    # Convert string dates to date objects if needed
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date and isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    imported = 0
    for entry in data:
        if entry['date'] >= start_date:
            if end_date and entry['date'] > end_date:
                continue

            # Check if already exists
            with get_db() as conn:
                existing = conn.execute(
                    'SELECT date FROM daily_rice_consumption WHERE date = ?',
                    (str(entry['date']),)
                ).fetchone()

                if not existing:
                    insert_daily_rice(str(entry['date']), entry['grains'], source='import')
                    imported += 1

    print(f"Imported {imported} days of historical data")
    return imported

if __name__ == '__main__':
    # Test the scraper
    fetch_and_import_yesterday()

"""
Import script to set up 2024 data

This will:
1. Initialize the database
2. Set starting surplus for Jan 1, 2024: 7,238,896,492 grains
3. Import all 2024 daily consumption data from the website
4. Set the 2023 rice price: $0.0000071042 per grain
"""

from database import init_db, set_config, insert_rice_price
from scraper import import_historical_data
from datetime import datetime

def main():
    print("Initializing database...")
    init_db()

    print("\nSetting starting surplus...")
    # Starting surplus on Jan 1, 2024
    set_config('starting_surplus_grains', '7238896492')
    set_config('starting_surplus_date', '2024-01-01')
    print("Starting surplus set: 7,238,896,492 grains on 2024-01-01")

    print("\nSetting 2023 rice price...")
    insert_rice_price(2023, 0.0000071042, 'WFP average for 2023')
    print("Rice price set: $0.0000071042 per grain (2023)")

    print("\nImporting 2024 daily consumption data...")
    start_date = datetime(2024, 1, 1).date()
    end_date = datetime(2024, 12, 31).date()
    imported = import_historical_data(start_date, end_date)
    print(f"Imported {imported} days of 2024 data")

    print("\n" + "="*50)
    print("Import complete!")
    print("="*50)
    print("\nYou can now run the app with: python app.py")
    print("Then visit: http://localhost:5000")

if __name__ == '__main__':
    main()

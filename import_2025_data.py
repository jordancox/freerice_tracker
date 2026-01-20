"""
Import script for 2025 data

This will:
1. Update starting surplus to the ending balance from 2024: 1,843,129,892 grains
2. Update the starting date to Jan 1, 2025
3. Import all available 2025 daily consumption data from the website
"""

from database import set_config, calculate_current_surplus
from scraper import import_historical_data
from datetime import datetime

def main():
    # First, calculate what our surplus was at end of 2024
    print("Calculating 2024 ending surplus...")
    ending_2024_surplus = calculate_current_surplus()
    print(f"2024 ending surplus: {ending_2024_surplus:,.0f} grains")

    print("\nUpdating starting surplus for 2025...")
    # Set this as the starting surplus for 2025
    set_config('starting_surplus_grains', str(int(ending_2024_surplus)))
    set_config('starting_surplus_date', '2025-01-01')
    print(f"Starting surplus set: {int(ending_2024_surplus):,} grains on 2025-01-01")

    print("\nImporting 2025 daily consumption data...")
    start_date = datetime(2025, 1, 1).date()
    # Import all available 2025 data (up to today)
    imported = import_historical_data(start_date, end_date=None)
    print(f"Imported {imported} days of 2025 data")

    print("\n" + "="*50)
    print("2025 import complete!")
    print("="*50)

    # Show new current surplus
    new_surplus = calculate_current_surplus()
    print(f"\nCurrent surplus: {new_surplus:,.0f} grains")

if __name__ == '__main__':
    main()

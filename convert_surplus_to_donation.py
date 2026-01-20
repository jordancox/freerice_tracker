"""
Convert the starting surplus into a donation entry

This makes the dashboard clearer by showing ALL donations (including pre-2024)
in the "Total Donated" calculation.
"""

from database import set_config, insert_donation, get_latest_rice_price

# The starting surplus in grains
starting_surplus_grains = 7238896492

# Get the rice price to convert to USD
price_per_grain = get_latest_rice_price()
starting_surplus_usd = starting_surplus_grains * price_per_grain

print(f"Converting starting surplus to donation entry...")
print(f"  Grains: {starting_surplus_grains:,}")
print(f"  USD: ${starting_surplus_usd:,.2f}")

# Add the donation entry
insert_donation(
    date='2024-01-01',
    usd_amount=starting_surplus_usd,
    donor_name='Pre-2024 donations',
    notes='Cumulative surplus from donations prior to 2024'
)

# Set starting surplus to 0
set_config('starting_surplus_grains', '0')
set_config('starting_surplus_date', '2024-01-01')

print(f"\nDone! Starting surplus is now 0, and pre-2024 donations are tracked as a donation entry.")
print(f"This will show up in the donations list as 'Pre-2024 donations'")

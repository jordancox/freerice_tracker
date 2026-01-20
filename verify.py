from database import get_all_daily_rice, calculate_current_surplus, get_latest_rice_price

# Get all 2024 data
all_data = get_all_daily_rice()
total_consumed = sum(d['grains'] for d in all_data)
print(f'Total days imported: {len(all_data)}')
print(f'Date range: {all_data[0]["date"]} to {all_data[-1]["date"]}')
print(f'Total consumed: {total_consumed:,} grains')

# Calculate current surplus
surplus = calculate_current_surplus()
print(f'\nCurrent surplus: {surplus:,.0f} grains')

# Expected: 7,238,896,492 - consumed = surplus
expected = 7238896492 - total_consumed
print(f'Expected surplus: {expected:,} grains')
print(f'Match: {abs(surplus - expected) < 1}')

price = get_latest_rice_price()
print(f'\nRice price per grain: ${price}')
print(f'Surplus in USD: ${surplus * price:,.2f}')

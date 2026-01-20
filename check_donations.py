from database import get_donations, get_latest_rice_price, calculate_current_surplus

donations = get_donations()
price_per_grain = get_latest_rice_price()

print("All donations:")
print("="*70)
total_usd = 0
total_grains = 0

for d in donations:
    grains = d['usd_amount'] / price_per_grain
    total_usd += d['usd_amount']
    total_grains += grains
    print(f"{d['date']}: ${d['usd_amount']:,.2f} ({grains:,.0f} grains) - {d['donor_name']}")

print("="*70)
print(f"Total donated: ${total_usd:,.2f} ({total_grains:,.0f} grains)")

surplus = calculate_current_surplus()
print(f"\nCurrent surplus: {surplus:,.0f} grains (${surplus * price_per_grain:,.2f})")

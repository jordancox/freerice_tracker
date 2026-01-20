"""
Fix the configuration to properly handle 2024-2026 data

The issue: We imported 2024, 2025, and 2026 data, but the starting surplus
is set for 2025-01-01. This means it's calculating the surplus by subtracting
BOTH 2025 and 2026 consumption from the 2025 starting point.

Solution: Keep the starting surplus at 2024-01-01, so all years calculate correctly.
"""

from database import set_config, get_config

# Reset to original 2024 starting point
print("Setting starting surplus back to 2024-01-01...")
set_config('starting_surplus_grains', '7238896492')
set_config('starting_surplus_date', '2024-01-01')

print("Configuration updated:")
print(f"  Starting surplus: 7,238,896,492 grains")
print(f"  Starting date: 2024-01-01")
print("\nThis allows the system to properly calculate surplus across 2024, 2025, and 2026.")
print("\nNOTE: You likely have 2025 donations to add to cover the deficit!")

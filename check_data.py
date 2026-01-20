from database import get_db

with get_db() as conn:
    # Get date range
    result = conn.execute('''
        SELECT MIN(date) as min_date, MAX(date) as max_date, COUNT(*) as total_days
        FROM daily_rice_consumption
    ''').fetchone()

    print(f"Date range: {result['min_date']} to {result['max_date']}")
    print(f"Total days: {result['total_days']}")

    # Check 2025 data
    result_2025 = conn.execute('''
        SELECT COUNT(*) as count_2025, SUM(grains) as total_grains_2025
        FROM daily_rice_consumption
        WHERE date >= '2025-01-01' AND date < '2026-01-01'
    ''').fetchone()

    print(f"\n2025 data: {result_2025['count_2025']} days")
    print(f"2025 total consumed: {result_2025['total_grains_2025']:,} grains")

    # Check 2026 data
    result_2026 = conn.execute('''
        SELECT COUNT(*) as count_2026, SUM(grains) as total_grains_2026
        FROM daily_rice_consumption
        WHERE date >= '2026-01-01'
    ''').fetchone()

    print(f"\n2026 data: {result_2026['count_2026']} days")
    if result_2026['total_grains_2026']:
        print(f"2026 total consumed: {result_2026['total_grains_2026']:,} grains")

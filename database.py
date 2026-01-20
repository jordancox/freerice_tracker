import sqlite3
from datetime import datetime
from contextlib import contextmanager

DB_PATH = 'data/tracker.db'

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database with schema"""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS daily_rice_consumption (
                date DATE PRIMARY KEY,
                grains INTEGER NOT NULL,
                source TEXT DEFAULT 'auto',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                usd_amount DECIMAL(15,2) NOT NULL,
                donor_name TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS rice_prices (
                year INTEGER PRIMARY KEY,
                price_per_grain_usd DECIMAL(15,12) NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS system_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        print("Database initialized successfully")

def insert_daily_rice(date, grains, source='auto'):
    """Insert or update daily rice consumption"""
    with get_db() as conn:
        conn.execute('''
            INSERT OR REPLACE INTO daily_rice_consumption (date, grains, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (date, grains, source))
        conn.commit()

def insert_donation(date, usd_amount, donor_name='', notes=''):
    """Insert a new donation"""
    with get_db() as conn:
        conn.execute('''
            INSERT INTO donations (date, usd_amount, donor_name, notes)
            VALUES (?, ?, ?, ?)
        ''', (date, usd_amount, donor_name, notes))
        conn.commit()

def insert_rice_price(year, price_per_grain, notes=''):
    """Insert or update rice price for a year"""
    with get_db() as conn:
        conn.execute('''
            INSERT OR REPLACE INTO rice_prices (year, price_per_grain_usd, notes)
            VALUES (?, ?, ?)
        ''', (year, price_per_grain, notes))
        conn.commit()

def set_config(key, value):
    """Set a config value"""
    with get_db() as conn:
        conn.execute('''
            INSERT OR REPLACE INTO system_config (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        conn.commit()

def get_config(key, default=None):
    """Get a config value"""
    with get_db() as conn:
        result = conn.execute('SELECT value FROM system_config WHERE key = ?', (key,)).fetchone()
        return result['value'] if result else default

def get_daily_rice(limit=30):
    """Get recent daily rice consumption"""
    with get_db() as conn:
        rows = conn.execute('''
            SELECT date, grains, source FROM daily_rice_consumption
            ORDER BY date DESC LIMIT ?
        ''', (limit,)).fetchall()
        return [dict(row) for row in rows]

def get_all_daily_rice():
    """Get all daily rice consumption for calculations"""
    with get_db() as conn:
        rows = conn.execute('''
            SELECT date, grains FROM daily_rice_consumption ORDER BY date ASC
        ''').fetchall()
        return [dict(row) for row in rows]

def get_donations():
    """Get all donations"""
    with get_db() as conn:
        rows = conn.execute('''
            SELECT id, date, usd_amount, donor_name, notes FROM donations
            ORDER BY date DESC
        ''').fetchall()
        return [dict(row) for row in rows]

def get_rice_prices():
    """Get all rice prices"""
    with get_db() as conn:
        rows = conn.execute('''
            SELECT year, price_per_grain_usd, notes FROM rice_prices
            ORDER BY year DESC
        ''').fetchall()
        return [dict(row) for row in rows]

def get_latest_rice_price():
    """Get the most recent rice price per grain"""
    with get_db() as conn:
        result = conn.execute('''
            SELECT price_per_grain_usd FROM rice_prices
            ORDER BY year DESC LIMIT 1
        ''').fetchone()
        return float(result['price_per_grain_usd']) if result else None

def calculate_current_surplus():
    """Calculate current surplus in grains"""
    starting_surplus = float(get_config('starting_surplus_grains', 0))

    # Sum all consumption
    total_consumed = 0
    for row in get_all_daily_rice():
        total_consumed += row['grains']

    # Sum all donations (convert to grains)
    total_donated_grains = 0
    price_per_grain = get_latest_rice_price()
    if price_per_grain:
        for donation in get_donations():
            total_donated_grains += donation['usd_amount'] / price_per_grain

    surplus = starting_surplus + total_donated_grains - total_consumed
    return surplus

def delete_donation(donation_id):
    """Delete a donation"""
    with get_db() as conn:
        conn.execute('DELETE FROM donations WHERE id = ?', (donation_id,))
        conn.commit()

if __name__ == '__main__':
    init_db()

# Freerice Donation Tracker

A simple web dashboard to track rice consumption vs donations for freerice.com.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Import 2024 data and initialize database:
```bash
python import_2024_data.py
```

3. Run the app:
```bash
python app.py
```

4. Visit: http://localhost:5000

## Features

- **Current Surplus**: See total rice surplus in grains and USD
- **Charts**: Visualize surplus trend and daily consumption
- **Donations**: Track donations and automatically convert to grains
- **Rice Prices**: Manage WFP rice prices by year
- **Daily Fetch**: Manually fetch yesterday's data or set up automated cron job

## Automated Daily Fetching

To automatically fetch data every day, add this to your crontab:

```bash
# Edit crontab
crontab -e

# Add this line to run at 8am daily:
0 8 * * * cd /path/to/freerice_tracker && /path/to/python scraper.py >> logs/cron.log 2>&1
```

## Data Model

- **Starting surplus**: Jan 1, 2024 = 7,238,896,492 grains
- **Rice price**: Uses latest available price (2023 = $0.0000071042/grain)
- **Daily consumption**: Fetched from https://engine.freerice.com/stats/rice/daily.html

## Calculation

```
Current Surplus = Starting Surplus + (Total Donations / Price Per Grain) - Total Consumption
```

## Files

- `app.py` - Flask web server
- `database.py` - SQLite database operations
- `scraper.py` - Fetch daily stats from freerice.com
- `import_2024_data.py` - One-time import script
- `templates/dashboard.html` - Dashboard UI
- `static/style.css` - Styling
- `data/tracker.db` - SQLite database (created on first run)

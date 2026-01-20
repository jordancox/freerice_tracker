# Quick Start Guide

## Running the App

**Simple way:**
```bash
cd ~/projects/freerice_tracker
./start.sh
```

Then open: http://localhost:5000

**Or manually:**
```bash
python app.py
```

## What You Can Do

### Fetch Latest Data
- Click "Fetch Latest Data" button on the dashboard
- Automatically imports all missing days up to yesterday

### Add Donations
- Use the "Add Donation" form
- Enter date, USD amount, and donor name
- System automatically converts to grains based on current rice price

### Update Rice Prices
- When you get new WFP prices, add them via "Add/Update Rice Price" form
- The system always uses the most recent year's price for calculations

### Manual Corrections
- If daily data is wrong, use "Add/Update Daily Rice Entry" to fix it

## File Structure

```
freerice_tracker/
├── app.py                  # Main Flask app
├── database.py             # Database operations
├── scraper.py              # Daily data fetcher
├── start.sh                # Easy startup script
├── stop.sh                 # Stop the server
├── data/
│   └── tracker.db          # Your SQLite database
├── templates/
│   └── dashboard.html      # Dashboard UI
└── static/
    └── style.css           # Styles
```

## Automated Fetching (Optional)

To automatically fetch data daily, you can set up a cron job:

```bash
crontab -e
```

Add this line to run daily at 8am:
```
0 8 * * * cd /Users/jordancox/projects/freerice_tracker && /usr/bin/python3 fetch_data.py >> logs/cron.log 2>&1
```

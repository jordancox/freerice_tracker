# Quick Start Guide

## You're all set up! Here's what's been done:

1. **Database created** with all 2024 data imported (366 days)
2. **Starting surplus** set to 7,238,896,492 grains (Jan 1, 2024)
3. **2023 rice price** configured: $0.0000071042 per grain
4. **Current surplus**: ~1.84 billion grains (as of Dec 31, 2024)

## Running the Dashboard

```bash
python app.py
```

Then open: http://localhost:5000

## What you can do:

### Daily Updates
- Click "Fetch Yesterday's Data" button to manually pull the latest day
- Or set up a cron job (see README.md) to automate it

### Add Donations
- Use the "Add Donation" form
- Enter date, USD amount, and donor name
- System automatically converts to grains based on current rice price

### Update Rice Prices
- When you get 2024/2025 WFP prices, add them via "Add/Update Rice Price" form
- The system always uses the most recent year's price

### Manual Corrections
- If daily data is wrong, use "Add/Update Daily Rice Entry" to fix it

## Important Notes

**Current discrepancy**: The system shows 1,843,129,892 grains ending surplus for 2024, but you mentioned 1,873,940,322. The ~30M grain difference might be:
- Donations from 2024 you need to add
- Manual adjustments from your spreadsheet
- Different calculation methods

Once you add any missing 2024 donations, the numbers should align.

## Next Steps

1. Add any 2024 donations you find
2. Add 2024 rice price when available (currently using 2023 price)
3. Start fetching 2025 daily data
4. Set up cron job for automation (when ready)

## File Structure

```
freerice_tracker/
├── app.py                  # Main Flask app
├── database.py             # Database operations
├── scraper.py              # Daily data fetcher
├── import_2024_data.py     # Already run - don't run again
├── verify.py               # Check calculations anytime
├── requirements.txt        # Already installed
├── README.md               # Full documentation
├── data/
│   └── tracker.db          # Your SQLite database
├── templates/
│   └── dashboard.html      # Dashboard UI
└── static/
    └── style.css           # Styles
```

## Hosting Later

When ready to deploy:
- Option 1: Simple VPS (DigitalOcean, Linode) - $5-10/month
- Option 2: PythonAnywhere (free tier available)
- Option 3: Fly.io (free tier)
- Option 4: Your domain with a small server

The entire app is self-contained - just needs Python 3.7+ and can run anywhere.

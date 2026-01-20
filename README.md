# Freerice Donation Tracker

A simple static web app to track rice consumption vs donations for freerice.com. No server required - runs entirely in your browser with localStorage.

## Usage

1. **Open the app**: Just open `index.html` in your browser, or visit the GitHub Pages site
2. **Import rice data**:
   - Go to https://engine.freerice.com/stats/rice/daily.html
   - View page source (Cmd+U or Ctrl+U)
   - Copy everything
   - Paste into the "Import Rice Data" textarea
   - Click "Import Data"
3. **Add donations**: Use the form to add donations with date, amount, and donor name
4. **Update rice price**: Change the price per grain when you get new WFP data

## Features

- Current surplus with color-coded status (green/yellow/red)
- Estimated depletion date based on 30-day average
- Track donations and automatically convert to grains
- All data stored in browser localStorage (persists across sessions)
- No server or database needed
- Can be hosted on GitHub Pages for free

## GitHub Pages Deployment

1. Go to your repository settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "main" branch
4. Click "Save"
5. Your site will be live at: `https://jordancox.github.io/freerice_tracker/`

## Data Storage

All data is stored locally in your browser's localStorage. To backup your data:
- Open browser console (F12)
- Type: `localStorage`
- Copy the values to save them

To import data on a new browser, set the values in console before opening the app.

## Technical Details

- Pure HTML/CSS/JavaScript
- No dependencies or build process
- Works offline after first load
- Data format: JSON in localStorage
  - `dailyData`: Object of date -> grains
  - `donations`: Array of donation objects
  - `ricePrice`: Current price per grain

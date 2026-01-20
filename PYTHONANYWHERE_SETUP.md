# PythonAnywhere Deployment Guide

Follow these steps to deploy the Freerice Tracker on PythonAnywhere's free tier.

## Step 1: Sign Up

1. Go to https://www.pythonanywhere.com
2. Click "Pricing & signup"
3. Choose "Create a Beginner account" (Free)
4. Complete the signup process

## Step 2: Clone Your Repository

1. Once logged in, go to the **Consoles** tab
2. Click "Bash" to start a new console
3. Run these commands:

```bash
git clone https://github.com/jordancox/freerice_tracker.git
cd freerice_tracker
```

## Step 3: Create Virtual Environment and Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Import Initial Data

```bash
python import_2024_data.py
python import_2025_data.py
python fix_config.py
python convert_surplus_to_donation.py
```

This will:
- Create the database
- Import all 2024-2026 data
- Set up your starting surplus as a donation
- Configure everything properly

## Step 5: Create Web App

1. Go to the **Web** tab
2. Click "Add a new web app"
3. Choose "Manual configuration" (not Flask wizard)
4. Select **Python 3.10** (or latest available)
5. Click "Next"

## Step 6: Configure Web App

On the Web tab, you'll need to configure:

### Source code directory:
```
/home/YOUR_USERNAME/freerice_tracker
```

### Working directory:
```
/home/YOUR_USERNAME/freerice_tracker
```

### Virtualenv:
```
/home/YOUR_USERNAME/freerice_tracker/venv
```

## Step 7: Configure WSGI File

1. On the Web tab, click on the WSGI configuration file link (e.g., `/var/www/your_username_pythonanywhere_com_wsgi.py`)
2. Delete all the contents
3. Replace with this:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/freerice_tracker'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment to point to your project
os.chdir(project_home)

# Import your Flask app
from app import app as application
```

4. **IMPORTANT:** Replace `YOUR_USERNAME` with your actual PythonAnywhere username
5. Click "Save"

## Step 8: Reload and Test

1. Go back to the **Web** tab
2. Click the big green **Reload** button
3. Click the link to your site: `https://YOUR_USERNAME.pythonanywhere.com`

Your app should now be live!

## Step 9: Add Your Accenture Donation

Since the database is fresh, you'll need to re-add your donation:
1. Visit your live site
2. Scroll to "Add Donation"
3. Enter:
   - Date: 2025-12-25
   - Amount: 75000
   - Donor: accenture
   - Notes: (optional)
4. Click "Add"

## Updating Your Site Later

When you make changes to the code:

1. Go to **Consoles** tab → Open a Bash console
2. Run:
```bash
cd freerice_tracker
git pull origin main
```
3. Go to **Web** tab → Click **Reload**

## Fetching Daily Data

Since cron jobs aren't available on the free tier:
- Just click "Fetch Latest Data" on your dashboard whenever you visit
- It will automatically fill in all missing days

## Troubleshooting

**500 Internal Server Error:**
- Check the error log on the Web tab
- Make sure WSGI file has correct username
- Make sure virtualenv path is correct

**Database not found:**
- Run the import scripts from the Bash console
- Check that you're in the `/home/YOUR_USERNAME/freerice_tracker` directory

**Modules not found:**
- Activate virtualenv: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`
- Reload the web app

## Custom Domain (Optional - Requires Paid Tier)

If you upgrade to a paid tier ($5/month), you can use your own domain instead of the pythonanywhere.com subdomain.

---

**Your site will be at:** `https://YOUR_USERNAME.pythonanywhere.com`

Enjoy your live Freerice Tracker!

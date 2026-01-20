# Fly.io Deployment Guide

Deploy the Freerice Tracker on Fly.io's free tier with persistent storage.

## Prerequisites

Install the Fly.io CLI:

**macOS:**
```bash
brew install flyctl
```

**Linux/WSL:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows:**
```powershell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

## Step 1: Sign Up and Login

```bash
flyctl auth signup
# OR if you already have an account:
flyctl auth login
```

## Step 2: Deploy Your App

From your local project directory:

```bash
cd ~/projects/freerice_tracker

# Launch the app (this will use the existing fly.toml)
flyctl launch --no-deploy

# When prompted:
# - App name: freerice-tracker (or choose your own)
# - Region: Choose closest to you
# - PostgreSQL: No
# - Redis: No

# Create the persistent volume for the database
flyctl volumes create freerice_data --size 1 --region sjc

# Deploy!
flyctl deploy
```

## Step 3: Access Your App

Your app will be live at: `https://freerice-tracker.fly.dev`

(Or whatever app name you chose)

## Updating the App

When you make changes:

```bash
git pull  # if pulling from GitHub
flyctl deploy
```

## Fetching New Data

The "Fetch Latest Data" button will work automatically since Fly.io doesn't block outbound connections.

## Setting Up Scheduled Data Fetching (Optional)

Fly.io doesn't have built-in cron on free tier, but you can use GitHub Actions or an external cron service to ping an endpoint.

Create a new endpoint in your app or use a service like cron-job.org to call:
```
https://your-app.fly.dev/
```

Then click the fetch button manually when you visit.

## Monitoring

View logs:
```bash
flyctl logs
```

Check app status:
```bash
flyctl status
```

SSH into your app:
```bash
flyctl ssh console
```

## Costs

**Free tier includes:**
- Up to 3 shared-cpu VMs
- 3GB persistent volumes
- 160GB outbound transfer

Your app will automatically scale to zero when not in use (free tier) and wake up when accessed.

## Custom Domain (Optional)

If you have a domain:

```bash
flyctl certs add yourdomain.com
flyctl certs add www.yourdomain.com
```

Then add these DNS records:
- A record: `@` → (IP from flyctl ips list)
- AAAA record: `@` → (IPv6 from flyctl ips list)
- CNAME: `www` → `yourdomain.com`

## Troubleshooting

**App not starting:**
```bash
flyctl logs
```

**Database not initializing:**
```bash
flyctl ssh console
ls -la /app/data
```

**Need to reset database:**
```bash
flyctl volumes delete freerice_data
flyctl volumes create freerice_data --size 1 --region sjc
flyctl deploy
```

---

**Your app will be at:** `https://freerice-tracker.fly.dev` (or your chosen name)

The database will persist across deploys, and the "Fetch Latest Data" button will work perfectly!

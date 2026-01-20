# GitHub Actions Setup

The app uses GitHub Actions to fetch daily rice data and sync it to Fly.io.

## How It Works

1. **GitHub Actions runs daily at 8am UTC** (midnight PST)
2. The workflow fetches yesterday's rice data from freerice.com
3. It sends the data to your Fly.io app via the `/api/import-day` endpoint
4. Your app stores it in the database

This works around freerice.com blocking cloud hosting IPs, since GitHub Actions runs on different infrastructure.

## Setup Instructions

### 1. Add GitHub Secret

Go to your repository settings and add a secret:

1. Visit: https://github.com/jordancox/freerice_tracker/settings/secrets/actions
2. Click "New repository secret"
3. Name: `API_TOKEN`
4. Value: `ade2a20525d1bd1f05b842302654d70040140401a3109db84f51c76c357e099c`
5. Click "Add secret"

### 2. That's it!

The GitHub Action will run automatically every day. You can also trigger it manually:

1. Go to: https://github.com/jordancox/freerice_tracker/actions
2. Click "Fetch Daily Rice Data" workflow
3. Click "Run workflow"

## Testing

To test the workflow immediately:

1. Go to: https://github.com/jordancox/freerice_tracker/actions
2. Click on "Fetch Daily Rice Data"
3. Click "Run workflow" → "Run workflow"
4. Watch the progress

After it completes, check your Fly.io app to see if the data was imported.

## Security

The API endpoint requires a secret token (`API_TOKEN`) to prevent unauthorized access. This token is:
- Stored as a secret in Fly.io (environment variable)
- Stored as a secret in GitHub Actions
- Never exposed in logs or code

## Manual Sync (if needed)

If you need to manually import historical data:

1. Run the workflow multiple times manually
2. Or SSH into Fly.io and run the import scripts
3. Or run locally and upload the database

## Troubleshooting

**Workflow fails with "Failed to send data":**
- Check that the GitHub secret `API_TOKEN` is set correctly
- Check Fly.io logs: `flyctl logs --app freerice-tracker`

**No data being imported:**
- Check the workflow logs in GitHub Actions
- Verify freerice.com is accessible from GitHub Actions

**401 Unauthorized:**
- The API token doesn't match. Verify both GitHub and Fly.io have the same token.

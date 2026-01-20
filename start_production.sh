#!/bin/bash

# Initialize database if it doesn't exist
if [ ! -f /app/data/tracker.db ]; then
    echo "Database not found, initializing..."
    python import_2024_data.py
    python import_2025_data.py
    python fix_config.py
    python convert_surplus_to_donation.py
    echo "Database initialized!"
fi

# Start the application
exec gunicorn --bind 0.0.0.0:8080 --workers 1 app:app

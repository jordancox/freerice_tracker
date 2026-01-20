#!/bin/bash

# Freerice Tracker Startup Script

cd "$(dirname "$0")"

echo "Starting Freerice Tracker..."
echo ""
echo "The app will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py

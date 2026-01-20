#!/bin/bash

# Stop the Freerice Tracker if it's running

echo "Stopping Freerice Tracker..."

# Find and kill any running Flask processes on port 5000
lsof -ti:5000 | xargs kill 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Stopped successfully"
else
    echo "No running instance found"
fi

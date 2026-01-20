#!/usr/bin/env python3
"""
Simple script to fetch all missing data
Can be run manually or via cron job
"""

from scraper import fetch_and_import_missing

if __name__ == '__main__':
    fetch_and_import_missing()

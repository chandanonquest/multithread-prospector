#!/usr/bin/env python3
"""
sync_deepgram_to_sheets.py
Uploads prospects_deepgram.csv to Google Sheets via sheets_logger.py
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from sheets_logger import create_and_populate_from_csv

def main():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prospects_deepgram.csv")
    title = "Deepgram - High-Intent B2B Prospecting Leads"
    print(f"Creating Google Sheet '{title}' from {csv_path}...")
    res = create_and_populate_from_csv(title, csv_path)
    print("Success!")
    print(f"Spreadsheet ID: {res.get('spreadsheet_id')}")
    print(f"Spreadsheet URL: {res.get('url')}")

if __name__ == "__main__":
    main()

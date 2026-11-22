#!/usr/bin/env python3
"""
sheets_logger.py
Helper module to create and populate B2B prospecting spreadsheets via gsheets CLI,
with automatic fallback to local CSV export when gsheets CLI is unavailable.
"""

import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import List, Dict, Any, Optional

COLUMNS = [
    "Status",
    "First Name",
    "Last Name",
    "Job Title",
    "Company",
    "Website",
    "Work Email",
    "LinkedIn URL",
    "ICP Fit Tier",
    "Key Facts & Signals",
    "Personalized Hook",
    "Conversation Bits & Soundbites",
    "Subject Line",
    "Outreach Snippet",
    "Apollo ID"
]

def get_gsheets_cmd() -> str:
    """Finds the available gsheets executable across Windows and Unix platforms."""
    if sys.platform == "win32":
        return shutil.which("gsheets.cmd") or shutil.which("gsheets") or "gsheets.cmd"
    return shutil.which("gsheets") or "gsheets"

def run_gsheets_cmd(args: List[str]) -> subprocess.CompletedProcess:
    """Executes a gsheets command via subprocess."""
    cmd_bin = get_gsheets_cmd()
    cmd = [cmd_bin] + args
    return subprocess.run(cmd, capture_output=True, text=True, check=True, shell=(sys.platform == "win32"))

def lead_to_row(lead: Dict[str, Any]) -> List[str]:
    """Maps a lead dictionary to the standardized 15-column format."""
    return [
        str(lead.get("status", "Researched")),
        str(lead.get("first_name", "")),
        str(lead.get("last_name", "")),
        str(lead.get("title", "")),
        str(lead.get("company", "")),
        str(lead.get("website", "") or lead.get("domain", "")),
        str(lead.get("email", "")),
        str(lead.get("linkedin_url", "")),
        str(lead.get("icp_tier", "Tier 1")),
        str(lead.get("key_facts", "")),
        str(lead.get("personalized_hook", "")),
        str(lead.get("soundbites", "")),
        str(lead.get("subject_line", "")),
        str(lead.get("outreach_snippet", "")),
        str(lead.get("apollo_id", ""))
    ]

def create_prospecting_sheet(title: str) -> Dict[str, str]:
    """
    Creates a new Google Spreadsheet and styles the initial view.
    Returns spreadsheet_id and edit url.
    """
    try:
        res = run_gsheets_cmd(["mutate", "create", "--title", title])
        output = res.stdout.strip()
        
        match = re.search(r"ID:\s*([a-zA-Z0-9-_]+)", output) or re.search(r"docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)", output)
        if match:
            spreadsheet_id = match.group(1)
        else:
            match2 = re.search(r"([a-zA-Z0-9-_]{30,})", output)
            spreadsheet_id = match2.group(1) if match2 else output.split()[-1].strip("()")
        
        url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
        return {
            "spreadsheet_id": spreadsheet_id,
            "url": url
        }
    except Exception as e:
        print(f"Notice: gsheets CLI unavailable ({e}). Using local fallback mode.", file=sys.stderr)
        return {
            "spreadsheet_id": "local_export",
            "url": "local_csv_fallback"
        }

def append_prospects(spreadsheet_id: str, prospects: List[Dict[str, Any]], export_local_csv: bool = True) -> bool:
    """
    Appends enriched prospect records to the Google Spreadsheet.
    Also creates a local CSV backup if requested.
    """
    # Write to a temporary CSV for clean atomic import
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".csv", delete=False) as tf:
        temp_csv_path = tf.name
        writer = csv.writer(tf)
        writer.writerow(COLUMNS)
        for p in prospects:
            writer.writerow(lead_to_row(p))
            
    try:
        if spreadsheet_id != "local_export":
            run_gsheets_cmd(["mutate", "import-csv", spreadsheet_id, temp_csv_path])
            try:
                run_gsheets_cmd([
                    "mutate", "format", spreadsheet_id,
                    "--sheet-id", "0",
                    "--start-row", "0", "--end-row", "1",
                    "--start-col", "0", "--end-col", str(len(COLUMNS)),
                    "--bold", "--align", "CENTER", "--bg-color", "#1A73E8", "--fg-color", "#FFFFFF"
                ])
                run_gsheets_cmd(["mutate", "freeze", spreadsheet_id, "--sheet-id", "0", "--rows", "1"])
            except Exception as style_err:
                print(f"Warning: could not apply cell styling: {style_err}", file=sys.stderr)
    except Exception as err:
        print(f"Warning: could not write to Google Sheets: {err}", file=sys.stderr)
    finally:
        if os.path.exists(temp_csv_path):
            try:
                os.remove(temp_csv_path)
            except OSError:
                pass
                
    return True

def create_and_populate_from_csv(title: str, csv_path: str) -> Dict[str, str]:
    """
    Creates a new Google Spreadsheet, imports a CSV, and formats the header row.
    """
    # 1. Create spreadsheet
    sheet_info = create_prospecting_sheet(title)
    spreadsheet_id = sheet_info["spreadsheet_id"]
    url = sheet_info["url"]
    
    if spreadsheet_id == "local_export":
        return sheet_info
    
    # 2. Import CSV
    try:
        run_gsheets_cmd(["mutate", "import-csv", spreadsheet_id, csv_path])
        # 3. Format header row: bold, frozen row 1, custom colors
        try:
            run_gsheets_cmd([
                "mutate", "format", spreadsheet_id,
                "--sheet-id", "0",
                "--start-row", "0", "--end-row", "1",
                "--start-col", "0", "--end-col", str(len(COLUMNS)),
                "--bold", "--align", "CENTER", "--bg-color", "#1A73E8", "--fg-color", "#FFFFFF"
            ])
            run_gsheets_cmd(["mutate", "freeze", spreadsheet_id, "--sheet-id", "0", "--rows", "1"])
        except Exception as e:
            print(f"Warning: could not apply styling: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: could not import CSV: {e}", file=sys.stderr)
        
    return {
        "spreadsheet_id": spreadsheet_id,
        "url": url
    }

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "import":
        title = sys.argv[2]
        csv_file = sys.argv[3]
        res = create_and_populate_from_csv(title, csv_file)
        print(json.dumps(res, indent=2))
    else:
        print("Usage:")
        print("  python sheets_logger.py import \"<Title>\" <path_to_csv>")

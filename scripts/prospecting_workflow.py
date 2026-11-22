#!/usr/bin/env python3
"""
prospecting_workflow.py
Orchestrates ICP-based lead research, hook generation, and Google Sheets export.
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Any

try:
    from sheets_logger import create_prospecting_sheet, append_prospects
except ImportError:
    from .sheets_logger import create_prospecting_sheet, append_prospects

def research_and_enrich_lead(lead: Dict[str, Any], icp: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standardizes and enriches a lead record with synthesized research,
    personalized hooks, and conversation bits.
    """
    first_name = lead.get("first_name", "")
    last_name = lead.get("last_name", "")
    full_name = f"{first_name} {last_name}".strip()
    title = lead.get("title", "Leader")
    company = lead.get("company", "the company")
    domain = lead.get("website") or lead.get("domain", "")
    
    # 1. Key Facts & Signals synthesis
    facts = lead.get("key_facts") or (
        f"• Leading {title} initiatives at {company}.\n"
        f"• Aligns with {icp.get('target_vertical', 'B2B')} target segment in the {icp.get('target_size', 'mid-market')} range.\n"
        f"• High relevance to {icp.get('core_offering', 'core product')} workflow optimization."
    )
    
    # 2. Personalized Hook
    hook = lead.get("personalized_hook") or (
        f"Saw the momentum your team is driving at {company} around {title.lower()} priorities. "
        f"Curious how you're tackling {icp.get('primary_pain_point', 'scaling bottlenecks')} as your org expands."
    )
    
    # 3. Conversation Bits / Soundbites
    soundbites = lead.get("soundbites") or (
        f"Soundbite 1: 'Most {title}s we speak with in {icp.get('target_vertical', 'your space')} are trying to cut down cycle times without overhauling existing systems.' | "
        f"Soundbite 2: 'We typically see teams at {company}'s stage achieve a 30-40% reduction in friction within 45 days.'"
    )
    
    # 4. Subject Line & Outreach Snippet
    subject_line = lead.get("subject_line") or f"quick question re: {company}'s workflow"
    outreach = lead.get("outreach_snippet") or (
        f"Hi {first_name},\n\n"
        f"{hook}\n\n"
        f"We recently partnered with similar teams to solve {icp.get('primary_pain_point', 'this exact challenge')}, "
        f"delivering {icp.get('key_benefit', 'meaningful efficiency gains')} in under a month.\n\n"
        f"Open to a brief 10-minute idea exchange next Tuesday, or is this currently handled in-house?\n\n"
        f"Best,\n[Your Name]"
    )
    
    return {
        "status": lead.get("status", "Researched"),
        "first_name": first_name,
        "last_name": last_name,
        "title": title,
        "company": company,
        "website": domain,
        "email": lead.get("email", ""),
        "linkedin_url": lead.get("linkedin_url", ""),
        "icp_tier": lead.get("icp_tier", "Tier 1"),
        "key_facts": facts,
        "personalized_hook": hook,
        "soundbites": soundbites,
        "subject_line": subject_line,
        "outreach_snippet": outreach,
        "apollo_id": lead.get("apollo_id", "")
    }

def run_pipeline(
    company_name: str,
    icp_data: Dict[str, Any],
    leads_data: List[Dict[str, Any]],
    skip_sheets: bool = False,
    output_csv: Optional[str] = None
) -> Dict[str, Any]:
    """
    Runs enrichment and logs all leads to a Google Sheet and/or local CSV.
    """
    enriched_leads = [research_and_enrich_lead(l, icp_data) for l in leads_data]
    result: Dict[str, Any] = {
        "company": company_name,
        "leads_count": len(enriched_leads),
        "status": "success"
    }

    if output_csv:
        import csv
        from sheets_logger import COLUMNS, lead_to_row
        os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
        with open(output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(COLUMNS)
            for lead in enriched_leads:
                writer.writerow(lead_to_row(lead))
        print(f"Exported {len(enriched_leads)} leads to local CSV: {output_csv}")
        result["csv_path"] = output_csv

    if not skip_sheets:
        sheet_title = f"{company_name} - Prospecting & Outreach Pipeline"
        print(f"Creating Google Spreadsheet: '{sheet_title}'...")
        sheet_info = create_prospecting_sheet(sheet_title)
        spreadsheet_id = sheet_info["spreadsheet_id"]
        sheet_url = sheet_info["url"]
        
        if spreadsheet_id != "local_export":
            print(f"Spreadsheet created: {sheet_url}")
            print(f"Appending {len(enriched_leads)} enriched leads...")
            append_prospects(spreadsheet_id, enriched_leads)
            print("Export to Google Sheets complete!")
            result["spreadsheet_id"] = spreadsheet_id
            result["url"] = sheet_url
        else:
            print("Google Sheets integration skipped (gsheets CLI in local mode).")

    result["leads"] = enriched_leads
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run prospecting enrichment and logging pipeline.")
    parser.add_argument("--company", required=True, help="Name of the company/product being prospected for")
    parser.add_argument("--input-file", help="Path to JSON file containing ICP and raw leads")
    parser.add_argument("--skip-sheets", action="store_true", help="Skip Google Sheets creation and only process data")
    parser.add_argument("--output-csv", help="Optional path to save leads as CSV")
    parser.add_argument("--output-json", help="Optional path to save enriched leads as JSON")
    args = parser.parse_args()
    
    if args.input_file and os.path.exists(args.input_file):
        with open(args.input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            icp = data.get("icp", {})
            leads = data.get("leads", [])
    else:
        # Default mock structure for verification
        icp = {
            "core_offering": "AI Revenue Operations Platform",
            "target_vertical": "B2B SaaS",
            "target_size": "50-500 employees",
            "primary_pain_point": "pipeline slippage and scattered sales intelligence",
            "key_benefit": "25% faster deal velocity"
        }
        leads = [
            {
                "first_name": "Sarah",
                "last_name": "Jenkins",
                "title": "VP of Revenue Operations",
                "company": "CloudFlow Technologies",
                "website": "cloudflow.io",
                "email": "sarah.jenkins@cloudflow.io",
                "linkedin_url": "https://linkedin.com/in/sarah-jenkins-sample",
                "apollo_id": "apl_sample_01"
            }
        ]
        
    result = run_pipeline(
        company_name=args.company,
        icp_data=icp,
        leads_data=leads,
        skip_sheets=args.skip_sheets,
        output_csv=args.output_csv
    )
    
    if args.output_json:
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"Exported pipeline results to: {args.output_json}")
        
    print(f"\nPipeline finished for {args.company}: {result['leads_count']} leads processed.")

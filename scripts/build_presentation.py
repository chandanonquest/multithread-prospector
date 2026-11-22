#!/usr/bin/env python3
"""
build_presentation.py
Creates a professional Google Slides presentation showcasing the B2B Prospecting Swarm
skill and exports it to PDF.
"""

import json
import os
import re
import subprocess
import sys
import time

def run_cmd(args):
    cmd = ["gslides.cmd"] + args
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if res.returncode != 0:
        print(f"Error running {' '.join(cmd)}: {res.stderr}", file=sys.stderr)
    return res.stdout.strip()

slides_content = [
    {
        "title": "Autonomous B2B Prospecting & Swarm Enrichment",
        "subtitle": "End-to-End Pipeline: Deep ICP Formulation, Swarm Research, Cold Hooks, and Google Sheets Sync",
        "category": "Title Slide",
        "body": (
            "Antigravity Agent Automation Engine\n\n"
            "• Autonomous ICP Strategy & Buyer Persona Mapping\n"
            "• Apollo.io Organization & Lead Discovery\n"
            "• Multi-Agent Swarm Deep Research & Signal Extraction\n"
            "• Personalized Cold Hooks & Live Conversation Soundbites\n"
            "• Direct Integration with Google Drive & Google Sheets"
        )
    },
    {
        "title": "1. The B2B Prospecting Challenge & Autonomous Solution",
        "subtitle": "Eliminating manual research fatigue and generic outreach drop-off",
        "category": "Architecture",
        "body": (
            "The Problem:\n"
            "• Manual prospecting consumes 15+ hours/week per sales rep with <2% reply rates.\n"
            "• Inbound Drop-off: 95%+ of buyers bounce when facing static 'Book a Demo' forms.\n"
            "• Demo Fatigue: Sales reps waste 40%+ of capacity running repetitive basic tours.\n\n"
            "The Solution:\n"
            "• 5-Stage Autonomous Pipeline: Transforms raw product URL into CRM-ready intelligence.\n"
            "• Multi-Agent Swarm: Conducts concurrent deep-dives into company triggers and executive roles.\n"
            "• 15-Column Intelligence Sync: Formatted Google Sheets with hooks, soundbites, and email drafts."
        )
    },
    {
        "title": "2. Strategic ICP Formulation & Human Calibration Gate",
        "subtitle": "Precision targeting before spending credits or initiating outreach",
        "category": "Strategy",
        "body": (
            "Stage 1: Multi-Dimensional ICP Synthesis\n"
            "• Value Architecture: Deconstructs core value proposition, economic ROI, and primary friction points.\n"
            "• 4-Dimensional Mapping: Firmographics, Technographics, Buyer Personas, and Buying Signals.\n"
            "• Automated Search Translation: Formulates Apollo search filters (titles, seniorities, headcount ranges).\n\n"
            "Stage 2: Human-in-the-Loop Confirmation Gate\n"
            "• Pauses to review targeting criteria, persona priorities, and batch size.\n"
            "• Prevents wasted API credits and ensures tight alignment with GTM goals."
        )
    },
    {
        "title": "3. Apollo Discovery & Parallel Swarm Research",
        "subtitle": "Live firmographic telemetry combined with multi-agent deep research",
        "category": "Enrichment",
        "body": (
            "Stage 3: Apollo.io Live Integration\n"
            "• Enriches target accounts with employee counts, 6m/12m growth rates, and department headcounts.\n"
            "• Uncovers installed technographics, tech stack dependencies, and company keywords.\n\n"
            "Stage 4: Agent Swarm Research & Signal Extraction\n"
            "• Concurrent Worker Agents: Investigates company news, executive history, and recent posts.\n"
            "• Verifiable Fact Synthesis: 3–5 sharp bullet points per lead detailing operational reality.\n"
            "• High-Intent Triggers: GTM team expansions, funding announcements, and tool migrations."
        )
    },
    {
        "title": "4. Personalized Outreach & Google Drive Sync",
        "subtitle": "Generating high-converting sales assets and real-time spreadsheet logging",
        "category": "Outreach",
        "body": (
            "Stage 5: High-Converting Outreach Assets\n"
            "• Pattern-Interrupt Hooks: 1–2 sentence openers referencing specific milestones.\n"
            "• Live Conversation Soundbites: High-impact one-liners tailored for cold calls and voice notes.\n"
            "• Full Cold Email Drafts: Conversational, metric-backed drafts with low-friction CTAs.\n\n"
            "Stage 6: Google Sheets & Drive Sync\n"
            "• Direct API Integration: Creates new Google Spreadsheets with frozen, colored header rows.\n"
            "• 15 Intelligence Columns: Status, Contact Info, ICP Tier, Facts, Hooks, Soundbites, and Drafts."
        )
    },
    {
        "title": "5. Case Study: Storylane RepX",
        "subtitle": "Live execution across top US B2B SaaS startups",
        "category": "Case Study",
        "body": (
            "Case Study Details:\n"
            "• Target Product: Storylane RepX (Autonomous Inbound Sales Agent & Interactive Demos).\n"
            "• Batch Size: 10 high-intent US B2B SaaS accounts (11–500 employees).\n"
            "• Balanced Persona Mix: 60% Founders/CEOs (PLG), 20% CMOs, 20% VPs of Sales.\n\n"
            "Featured Target Accounts:\n"
            "• Dock (Alex Kracov), Spekit (Ian Lowe & Evan Horibe), Statsig (Sam Maher),\n"
            "  RudderStack (Eric Omwega), Cal.com (Peer Richelsen), Accord (Ross Rich),\n"
            "  Paragon (Brandon Huang), Vitally (Jamie Davidson), Hex (Barry McCardel).\n"
            "• Google Sheet created and populated with full dossier in user's Google Drive."
        )
    },
    {
        "title": "6. Credential Security & Zero-Token Fast-Start",
        "subtitle": "Governed operations, instant reusability, and token conservation",
        "category": "Governance",
        "body": (
            "API Key Governance:\n"
            "• Pre-Execution Confirmation: Mandatory user prompt before consuming Apollo API keys.\n"
            "• Seamless Key Rotation: Allows instant key changes via config/credentials.json.\n\n"
            "Fast-Start Session Memory:\n"
            "• Zero-Token Waste: New sessions instantly discover cached ICPs and previous lead datasets.\n"
            "• No Redundant Scraping: Existing leads are never re-queried without explicit instruction.\n"
            "• Continuous Execution: Workspace is permanently equipped with the prospecting skill."
        )
    }
]

def main():
    print("Creating Google Slides presentation...")
    out = run_cmd(["mutate", "create", "--title", "Autonomous B2B Prospecting & Swarm Enrichment"])
    match = re.search(r"ID:\s*([a-zA-Z0-9-_]+)", out)
    if not match:
        print("Failed to get presentation ID:", out)
        return
    pres_id = match.group(1)
    pres_url = f"https://docs.google.com/presentation/d/{pres_id}/edit"
    print(f"Presentation created: {pres_url}")
    
    # Get initial slides list
    slides_info = run_cmd(["readonly", "list-slides", pres_id])
    
    for i, slide_data in enumerate(slides_content):
        print(f"Adding slide {i+1}: {slide_data['title']}...")
        add_out = run_cmd(["mutate", "add-slide", pres_id])
        slide_id_match = re.search(r"Added slide:\s*([a-zA-Z0-9-_]+)", add_out)
        if not slide_id_match:
            print("Failed to add slide:", add_out)
            continue
        slide_id = slide_id_match.group(1)
        
        # Set professional dark navy background
        run_cmd(["mutate", "set-background", pres_id, "--slide", slide_id, "--color", "#0F172A"])
        
        # Add Header Box
        header_text = f"{slide_data['title']}\n{slide_data['subtitle']}"
        run_cmd([
            "mutate", "add-textbox", pres_id,
            "--slide", slide_id,
            "--text", header_text,
            "--x", "40", "--y", "30",
            "--width", "640", "--height", "80"
        ])
        
        # Add Body Box
        run_cmd([
            "mutate", "add-textbox", pres_id,
            "--slide", slide_id,
            "--text", slide_data["body"],
            "--x", "40", "--y", "125",
            "--width", "640", "--height", "250"
        ])
        time.sleep(0.5)

    # Delete the initial default empty slide if present
    default_slide_match = re.search(r"\b1\s+([a-zA-Z0-9-_]+)", slides_info)
    if default_slide_match:
        first_slide_id = default_slide_match.group(1)
        run_cmd(["mutate", "delete-slide", pres_id, first_slide_id])
        
    print("\nExporting presentation to PDF...")
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Autonomous_B2B_Prospecting_Swarm.pdf")
    run_cmd(["readonly", "export", pres_id, pdf_path, "--format", "pdf"])
    print(f"PDF exported successfully to: {pdf_path}")
    
    summary = {
        "presentation_id": pres_id,
        "presentation_url": pres_url,
        "pdf_path": pdf_path,
        "slide_count": len(slides_content)
    }
    with open("presentation_result.json", "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()

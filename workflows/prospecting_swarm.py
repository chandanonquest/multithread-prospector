"""
Dynamic Agent Swarm Workflow for ICP Prospecting
Can be executed directly via the run_workflow tool.
"""

from sheets_logger import create_prospecting_sheet, append_prospects

async def main():
    company = args.get("company", "Target Company")
    product_desc = args.get("product_description", "")
    
    # Phase 1: ICP Definition & Review
    phase("ICP Formulation")
    log(f"Formulating and reviewing ICP for {company}...")
    
    # Phase 2: Lead Retrieval (Apollo MCP)
    phase("Lead Discovery")
    log("Querying Apollo MCP for decision-maker contacts...")
    raw_leads = args.get("leads", [])
    
    # Phase 3: Parallel Swarm Research
    phase("Swarm Deep Research")
    log(f"Fanning out research swarm across {len(raw_leads)} leads...")
    
    async def research_worker(lead):
        name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}"
        company_name = lead.get('company', '')
        
        # Parallel researcher subagent
        prompt = (
            f"Perform deep background research on {name}, {lead.get('title')} at {company_name} ({lead.get('website', '')}). "
            f"Find 3-5 verifiable bullet points covering recent company news, hiring trends, tech stack, and personal focus areas."
        )
        # In run_workflow, agent(...) returns an awaitable
        res = await agent(
            prompt=prompt,
            role=f"Researcher: {name}",
            model="flash",
            schema={
                "type": "object",
                "properties": {
                    "key_facts": {"type": "string"},
                    "operational_context": {"type": "string"}
                },
                "required": ["key_facts"]
            }
        )
        return {**lead, **res}

    researched_leads = await parallel(raw_leads, research_worker)
    
    # Phase 4: Hook & Soundbite Generation
    phase("Outreach Personalization")
    log("Crafting personalized hooks, soundbites, and cold outreach snippets...")
    
    async def copywriter_worker(lead):
        prompt = (
            f"Using the researched facts for {lead.get('first_name')} at {lead.get('company')}:\n"
            f"Facts: {lead.get('key_facts')}\n"
            f"Craft: (1) A punchy personalized hook referencing their operational reality, "
            f"(2) Two conversation bits/soundbites for cold calls/voice notes, "
            f"(3) A 3-4 word subject line, (4) A concise cold email snippet."
        )
        res = await agent(
            prompt=prompt,
            role=f"Copywriter: {lead.get('first_name')}",
            model="flash",
            schema={
                "type": "object",
                "properties": {
                    "personalized_hook": {"type": "string"},
                    "soundbites": {"type": "string"},
                    "subject_line": {"type": "string"},
                    "outreach_snippet": {"type": "string"}
                },
                "required": ["personalized_hook", "soundbites", "subject_line", "outreach_snippet"]
            }
        )
        return {**lead, **res}

    fully_enriched_leads = await parallel(researched_leads, copywriter_worker)
    
    # Phase 5: Export to Google Sheets
    phase("Google Sheets Export")
    log("Writing enriched prospects to Google Drive...")
    sheet_title = f"{company} - Prospecting Intelligence"
    sheet_info = create_prospecting_sheet(sheet_title)
    append_prospects(sheet_info["spreadsheet_id"], fully_enriched_leads)
    
    log(f"Successfully logged to: {sheet_info['url']}")
    print(sheet_info['url'])

await main()

#!/usr/bin/env python3
"""
generate_batch_leads.py
Compiles 10 enriched leads matching Storylane RepX ICP, crafts personalized
hooks, soundbites, and outreach snippets, and logs them to Google Sheets.
"""

import json
import sys
import os

sys.path.append(os.path.dirname(__file__))
from sheets_logger import create_prospecting_sheet, append_prospects

leads = [
    {
        "status": "Researched",
        "first_name": "Alex",
        "last_name": "Kracov",
        "title": "Founder & CEO",
        "company": "Dock",
        "website": "dock.us",
        "email": "alex@dock.us",
        "linkedin_url": "https://www.linkedin.com/in/alexkracov/",
        "icp_tier": "Tier 1 - Founder/PLG",
        "key_facts": (
            "• Scaled Lattice marketing from early stage to $100M+ ARR before founding Dock (digital sales rooms & client workspaces).\n"
            "• Dock has 26 employees (+12.5% 12-month headcount growth per Apollo).\n"
            "• Publicly advocates for modern buyer-enablement and frictionless, transparent sales experiences.\n"
            "• Dock’s site relies heavily on product tours and visuals to explain mutual action plans and client portals."
        ),
        "personalized_hook": (
            "Loved your episode on buyer-led sales—you’ve been proving that modern B2B buyers hate black-box sales cycles. "
            "Given how visual Dock’s sales rooms are, curious if you've thought about letting website visitors test-drive a live room autonomously before requesting a call."
        ),
        "soundbites": (
            "Soundbite 1: 'You built Dock so buyers don't get stuck in 10-step email threads; RepX does the exact same thing for your homepage demo.' | "
            "Soundbite 2: 'Saves your team from running 20-minute basic walkthroughs for seed-stage startups, letting them self-close while passing enterprise intent straight to you.'"
        ),
        "subject_line": "buyer-led demos for dock",
        "outreach_snippet": (
            "Hi Alex,\n\n"
            "Loved your take on buyer-led sales—you’ve been proving for years that forcing modern buyers into friction-filled discovery calls just kills momentum.\n\n"
            "Given how visual Dock’s sales rooms are, curious if you've explored letting visitors test-drive a dynamic, interactive workspace directly on your site based on their specific use case (without human intervention).\n\n"
            "Storylane RepX turns website traffic into an interactive demo sandbox 24/7. SMB prospects self-qualify and close faster, while enterprise buyers hand your reps deep feature-level intent before the first call.\n\n"
            "Open to a brief 5-min look, or is your current inbound tour already converting at target?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "dock_kracov_01"
    },
    {
        "status": "Researched",
        "first_name": "Ian",
        "last_name": "Lowe",
        "title": "Chief Marketing Officer",
        "company": "Spekit",
        "website": "spekit.com",
        "email": "ian.lowe@spekit.com",
        "linkedin_url": "https://www.linkedin.com/in/ianlowe/",
        "icp_tier": "Tier 1 - Marketing Leader",
        "key_facts": (
            "• CMO at Spekit (just-in-time enablement & digital adoption platform); team size ~96 employees.\n"
            "• Apollo department breakdown shows 15 in marketing and 32 in sales.\n"
            "• Heavy focus on inbound demand generation and conversion optimization across sales enablement buyers.\n"
            "• Primary site CTA is currently 'Get a Demo' gated form with 5+ fields, creating friction for busy enablement leads."
        ),
        "personalized_hook": (
            "Saw Spekit's recent campaigns around embedding training directly in the flow of work. "
            "Since your core value is eliminating friction in software adoption, curious if gating your product behind a traditional demo form is causing inbound drop-off."
        ),
        "soundbites": (
            "Soundbite 1: 'If Spekit's promise is learning software in the flow of work, buyers should experience Spekit in the flow of your website.' | "
            "Soundbite 2: 'RepX lets enablement managers try your in-app highlights on their own terms, doubling tour engagement without burning rep hours.'"
        ),
        "subject_line": "inbound demo conversion at spekit",
        "outreach_snippet": (
            "Hi Ian,\n\n"
            "Caught Spekit's recent push around 'just-in-time' enablement in Salesforce and Slack. Your core value is literally eliminating friction in how users adopt tools.\n\n"
            "That's why I wanted to ask: are your inbound visitors getting that same zero-friction experience on spekit.com, or are they hitting the standard 'Schedule a Demo' form and bouncing?\n\n"
            "Storylane RepX gives website visitors an AI-guided, interactive demo tailored to their role (Sales vs RevOps vs Support). Smaller teams self-qualify on autopilot, while Evan’s sales team gets behavioral dossiers on high-value accounts.\n\n"
            "Worth a quick chat next week to see how it benchmarks against standard demo forms?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "spekit_lowe_02"
    },
    {
        "status": "Researched",
        "first_name": "Evan",
        "last_name": "Horibe",
        "title": "Vice President of Sales",
        "company": "Spekit",
        "website": "spekit.com",
        "email": "evan.horibe@spekit.com",
        "linkedin_url": "https://www.linkedin.com/in/evanhoribe/",
        "icp_tier": "Tier 1 - Sales Leader",
        "key_facts": (
            "• VP of Sales at Spekit leading a 32-person commercial & enterprise sales organization.\n"
            "• Responsible for quota attainment, inbound pipeline velocity, and sales cycle efficiency.\n"
            "• Spekit caters to both mid-market sales teams and enterprise rollouts, leading to disparate inbound qualification needs.\n"
            "• Sales reps currently spend significant time running intro overview demos for low-intent or smaller tier prospects."
        ),
        "personalized_hook": (
            "Noticed Spekit's sales team is scaling to support mid-market demand. "
            "Curious how much rep bandwidth is currently burned doing 20-minute intro tours for prospects who really just wanted to see the UI first."
        ),
        "soundbites": (
            "Soundbite 1: 'Your AEs shouldn't be human screen-sharers for tier-3 inbound leads; let RepX automate the tour and send you pre-warmed buyers.' | "
            "Soundbite 2: 'When enterprise buyers test-drive your flows beforehand, your reps enter the discovery call already knowing which workflows they clicked.'"
        ),
        "subject_line": "rep demo fatigue at spekit",
        "outreach_snippet": (
            "Hi Evan,\n\n"
            "Leading a 30+ person sales org at Spekit, I imagine protecting your AEs' calendar for high-ACV opportunities is a constant battle.\n\n"
            "Most VP of Sales we partner with tell us their reps burn 35%+ of their week giving repetitive 'feature tours' to smaller accounts who just wanted to see how Spekit surfaces tips in Salesforce.\n\n"
            "With Storylane RepX, those inbound visitors test-drive an interactive, role-specific demo on their own. Smaller accounts move themselves through the funnel, while your AEs receive the exact click-stream data before stepping into enterprise meetings.\n\n"
            "Would you be against a 10-minute walk-through to see how this frees up rep capacity?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "spekit_horibe_03"
    },
    {
        "status": "Researched",
        "first_name": "Sam",
        "last_name": "Maher",
        "title": "Head of Sales",
        "company": "Statsig",
        "website": "statsig.com",
        "email": "sam@statsig.com",
        "linkedin_url": "https://www.linkedin.com/in/sammaher/",
        "icp_tier": "Tier 1 - Sales Leader",
        "key_facts": (
            "• Leads sales at Statsig (feature management & experimentation platform, ~180 employees).\n"
            "• Product is inherently developer and product-manager focused; tech buyers have strong resistance to sales calls.\n"
            "• Statsig competes against LaunchDarkly and Optimizely, winning primarily on ease of deployment and developer experience.\n"
            "• Rapid enterprise adoption requiring high-velocity sales qualification."
        ),
        "personalized_hook": (
            "Given that Statsig sells to engineers and product leaders who notoriously hate 'talking to sales' just to evaluate feature flags, "
            "curious how your team bridges the gap between passive website visitors and qualified pipeline."
        ),
        "soundbites": (
            "Soundbite 1: 'Engineers won't book a call to see feature flags, but they will click through an interactive sandbox in 90 seconds.' | "
            "Soundbite 2: 'RepX lets technical prospects test your console interactively, handing your sales team exact signals on whether they care about experimentation vs gate rollouts.'"
        ),
        "subject_line": "statsig developer demo flow",
        "outreach_snippet": (
            "Hi Sam,\n\n"
            "Statsig's momentum against LaunchDarkly is awesome to see. But selling to engineers and PMs comes with a classic headache: technical buyers hate booking a sales call just to get a peek at the console.\n\n"
            "Storylane RepX solves this by embedding an AI-guided interactive product tour right on your site. Prospects can test-drive Statsig's feature gating or experimentation dashboards in an autonomous sandbox tailored to their use case.\n\n"
            "Your sales team gets notified with exact telemetry on what they tested, transforming cold discovery calls into warm technical conversations.\n\n"
            "Open to a quick 5-min look next week, or is your inbound conversion already where you want it?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "statsig_maher_04"
    },
    {
        "status": "Researched",
        "first_name": "Eric",
        "last_name": "Omwega",
        "title": "Vice President of Marketing",
        "company": "RudderStack",
        "website": "rudderstack.com",
        "email": "eric.omwega@rudderstack.com",
        "linkedin_url": "https://www.linkedin.com/in/ericomwega/",
        "icp_tier": "Tier 1 - Marketing Leader",
        "key_facts": (
            "• VP of Marketing at RudderStack (warehouse-native Customer Data Platform, ~130 employees).\n"
            "• Apollo indicates RudderStack operates in highly technical data engineering, competing with Segment and mParticle.\n"
            "• Running multi-channel demand generation campaigns to attract data architects, engineers, and growth marketers.\n"
            "• Technical architecture diagrams and SDK integrations require clear, interactive visual demonstration."
        ),
        "personalized_hook": (
            "Saw RudderStack’s latest content on warehouse-first customer data pipelines. "
            "Data engineers are notoriously skeptical of marketing fluff—curious how you're letting them interactively inspect RudderStack's event routing without forcing a demo form."
        ),
        "soundbites": (
            "Soundbite 1: 'Data engineers bounce the second they see a 6-field form; give them an interactive architecture demo and capture high-intent pipeline.' | "
            "Soundbite 2: 'RepX delivers 24/7 interactive product tours that match the technical depth your buyers expect.'"
        ),
        "subject_line": "interactive demo for rudderstack",
        "outreach_snippet": (
            "Hi Eric,\n\n"
            "Love RudderStack’s positioning around warehouse-native CDPs. But as you know better than anyone, data engineers and architects will do anything to avoid a generic 'Book a Demo' form.\n\n"
            "Storylane RepX allows technical buyers to test-drive an interactive tour of RudderStack’s pipelines, transformations, and warehouse syncs on their own terms.\n\n"
            "The AI agent personalizes the walkthrough based on whether they use Snowflake, BigQuery, or Redshift, and routes high-intent enterprise accounts straight to your sales team with full intent history.\n\n"
            "Would you be open to seeing a 2-minute mockup of how this looks for RudderStack?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "rudderstack_omwega_05"
    },
    {
        "status": "Researched",
        "first_name": "Peer",
        "last_name": "Richelsen",
        "title": "Co-Founder & Co-CEO",
        "company": "Cal.com",
        "website": "cal.com",
        "email": "peer@cal.com",
        "linkedin_url": "https://www.linkedin.com/in/peer-h/",
        "icp_tier": "Tier 1 - Founder/PLG",
        "key_facts": (
            "• Co-Founder & Co-CEO of Cal.com (open-source scheduling infrastructure, ~39 employees).\n"
            "• Champion of product-led growth (PLG), radical transparency, and developer-first distribution.\n"
            "• Rapidly expanding enterprise offering (routing forms, organization scheduling, HIPAA compliance).\n"
            "• High website traffic globally, with massive international inbound outside US business hours."
        ),
        "personalized_hook": (
            "Love the radical transparency and PLG speed you've built into Cal.com. "
            "Given how much global after-hours traffic hits your site, curious how you handle enterprise visitors who want to see organization routing without waiting for US business hours."
        ),
        "soundbites": (
            "Soundbite 1: 'Cal.com perfected the booking link; RepX does the same for the product demo—zero friction, instant evaluation.' | "
            "Soundbite 2: 'Lets your European and APAC enterprise visitors test-drive team workflows at 2 AM while passing full intent to your inbox.'"
        ),
        "subject_line": "cal.com interactive product tours",
        "outreach_snippet": (
            "Hi Peer,\n\n"
            "Big fan of what you and the team are building with Cal.com—the PLG flywheel and open-source momentum are unmatched.\n\n"
            "Even though scheduling is your bread and butter, many enterprise buyers want to visualize team routing forms and white-label features *before* they commit to a call or trial.\n\n"
            "Storylane RepX provides an autonomous, AI-driven interactive demo right on your site. International and after-hours visitors get an instant, tailored walkthrough, while self-serve users can upgrade on the spot.\n\n"
            "Worth a quick look, or is your current conversion flywheel already running at peak efficiency?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "cal_richelsen_06"
    },
    {
        "status": "Researched",
        "first_name": "Ross",
        "last_name": "Rich",
        "title": "Co-Founder & CEO",
        "company": "Accord",
        "website": "inaccord.com",
        "email": "ross@inaccord.com",
        "linkedin_url": "https://www.linkedin.com/in/rossrich/",
        "icp_tier": "Tier 1 - Founder/PLG",
        "key_facts": (
            "• Co-Founder & CEO of Accord (customer collaboration platform for mutual action plans, ~230 employees).\n"
            "• Former sales leader at Stripe; recognized industry expert on buyer-first sales methodologies and B2B alignment.\n"
            "• Accord's mission is eliminating misalignment between B2B buyers and sellers.\n"
            "• High synergy with interactive product previews that empower buyers during evaluation."
        ),
        "personalized_hook": (
            "Loved your posts on modern buyer enablement—you’ve been preaching for years that B2B deals fail when buyers aren't equipped to champion the tool internally. "
            "Curious if you’ve considered giving your website visitors an interactive Accord workspace to play with before they book a call."
        ),
        "soundbites": (
            "Soundbite 1: 'You built Accord to eliminate buyer friction post-demo; RepX eliminates the friction pre-demo.' | "
            "Soundbite 2: 'Let buyers experience an interactive mutual action plan in 60 seconds on inaccord.com, turning passive traffic into active pipeline.'"
        ),
        "subject_line": "buyer enablement on inaccord.com",
        "outreach_snippet": (
            "Hi Ross,\n\n"
            "Your insights on Stripe’s sales motion and buyer-first enablement have shaped how a lot of GTM teams think about deals today.\n\n"
            "Since Accord’s entire philosophy centers on empowering the buyer, I’m curious: why make interested buyers wait for a discovery call just to experience how a Mutual Action Plan works?\n\n"
            "Storylane RepX lets prospects test-drive a tailored, interactive Accord workspace autonomously directly on your website. SMBs qualify themselves and check out, while enterprise accounts get routed to your team with full engagement telemetry.\n\n"
            "Open to checking out a 3-minute demo, or is your inbound team already fully booked?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "accord_rich_07"
    },
    {
        "status": "Researched",
        "first_name": "Brandon",
        "last_name": "Huang",
        "title": "Co-Founder & CEO",
        "company": "Paragon",
        "website": "useparagon.com",
        "email": "brandon@useparagon.com",
        "linkedin_url": "https://www.linkedin.com/in/brandon-huang/",
        "icp_tier": "Tier 1 - Founder/PLG",
        "key_facts": (
            "• Co-Founder & CEO of Paragon (embedded integrations platform for SaaS apps, ~170 employees).\n"
            "• Scaled Paragon through Y Combinator and Series A/B.\n"
            "• Target audience is product managers and software engineering leaders who demand immediate proof of capability.\n"
            "• Sells embedded SDKs and integration workflows where visualization is critical to closing deals."
        ),
        "personalized_hook": (
            "Saw Paragon’s recent launches around AI agent integrations. "
            "Engineering leads evaluating embedded auth and workflows want proof that implementation is easy—curious if you're letting them click through the integration builder directly on your site."
        ),
        "soundbites": (
            "Soundbite 1: 'Product leaders don't want a slide deck on embedded integrations; they want to click through the workflow builder.' | "
            "Soundbite 2: 'RepX lets technical visitors build a mock integration on your site, moving SMB accounts to checkout while passing enterprise intent to sales.'"
        ),
        "subject_line": "interactive demo for paragon",
        "outreach_snippet": (
            "Hi Brandon,\n\n"
            "Huge fan of Paragon’s trajectory in embedded integrations. Product managers and engineers evaluating integration platforms are notoriously hands-on—they want to see how the SDK and workflow engine feel before talking to anyone.\n\n"
            "Storylane RepX lets visitors test-drive an interactive, use-case specific demo of Paragon directly in their browser without human rep assistance.\n\n"
            "It gives technical buyers the instant verification they want, while routing enterprise accounts to your sales team with exact insights on which integrations they explored.\n\n"
            "Would you be open to a quick 5-min look next Tuesday?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "paragon_huang_08"
    },
    {
        "status": "Researched",
        "first_name": "Jamie",
        "last_name": "Davidson",
        "title": "Co-Founder & CEO",
        "company": "Vitally",
        "website": "vitally.io",
        "email": "jamie@vitally.io",
        "linkedin_url": "https://www.linkedin.com/in/jamiedavidson/",
        "icp_tier": "Tier 1 - Founder/PLG",
        "key_facts": (
            "• Co-Founder & CEO of Vitally (next-generation Customer Success platform, ~140 employees).\n"
            "• Competes aggressively against legacy CS tools like Gainsight and ChurnZero on modern UI and real-time automation.\n"
            "• High traffic from CS directors, RevOps leaders, and post-sales executives.\n"
            "• Website currently pushes visitors to 'Book a Demo' forms, creating latency in competitive evaluations."
        ),
        "personalized_hook": (
            "Vitally wins deals against Gainsight every day because your UI is so much cleaner and faster. "
            "Curious if you’re using that UI advantage on your homepage by letting CS leaders interact with Vitally’s playbooks before scheduling a call."
        ),
        "soundbites": (
            "Soundbite 1: 'Your biggest weapon against Gainsight is how intuitive Vitally is; let prospects click through it in seconds on your homepage.' | "
            "Soundbite 2: 'RepX saves your AEs from running basic intro demos for 10-person CS teams so they can focus on high-ACV expansions.'"
        ),
        "subject_line": "vitally's ui advantage on inbound",
        "outreach_snippet": (
            "Hi Jamie,\n\n"
            "Vitally’s growth against legacy players like Gainsight is super impressive—and your biggest wedge is clearly how modern, intuitive, and fast your platform feels.\n\n"
            "Which got me thinking: when a CS leader visits vitally.io, why make them wait 2 days for a sales call to see that difference?\n\n"
            "With Storylane RepX, visitors can immediately test-drive an interactive tour of Vitally’s health scores, notes, and playbooks tailored to their tech stack. Smaller accounts self-serve and upgrade, while enterprise CS leaders arrive at AE meetings already sold on the UI.\n\n"
            "Would you be against taking a quick look at how this benchmarks for high-growth B2B SaaS?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "vitally_davidson_09"
    },
    {
        "status": "Researched",
        "first_name": "Barry",
        "last_name": "McCardel",
        "title": "Co-Founder & CEO",
        "company": "Hex",
        "website": "hex.tech",
        "email": "barry@hex.tech",
        "linkedin_url": "https://www.linkedin.com/in/bmccardel/",
        "icp_tier": "Tier 1 - Founder/PLG",
        "key_facts": (
            "• Co-Founder & CEO of Hex (collaborative data workspace for analytics and AI, ~170 employees).\n"
            "• Backed by Sequoia, a16z, and Snowflake Ventures; +53.8% 12-month headcount growth per Apollo.\n"
            "• Hex has a vibrant product-led community of data scientists, analytics engineers, and business leaders.\n"
            "• The product's visual interactive notebook is its key selling point; ideal fit for autonomous interactive demos."
        ),
        "personalized_hook": (
            "Hex’s growth in collaborative analytics is incredible—your interactive notebooks are the kind of product that people only truly understand once they play with it. "
            "Curious how you're capturing inbound visitors who want to test-drive Hex's reactive UI without waiting for a rep."
        ),
        "soundbites": (
            "Soundbite 1: 'Hex is visual by nature; letting website visitors run interactive SQL/Python blocks right on your site converts passive readers into active users.' | "
            "Soundbite 2: 'RepX personalizes the demo based on their data stack (Snowflake vs Databricks) and passes rich intent straight to your sales team.'"
        ),
        "subject_line": "hex interactive product sandbox",
        "outreach_snippet": (
            "Hi Barry,\n\n"
            "Huge fan of Hex’s mission to make data science collaborative. The reactive compute and visual notebook UI are what set Hex apart—and it’s the exact kind of product where 'seeing is believing.'\n\n"
            "Storylane RepX allows your website visitors to experience an autonomous, interactive demo of Hex tailored to their role (Data Analyst vs Analytics Engineer vs Business Lead) right inside their browser.\n\n"
            "SMB and individual practitioners move quickly down the self-serve path, while enterprise data teams get routed to your AEs with full context on which data connections they tested.\n\n"
            "Open to a brief 5-minute look next week, or is your current conversion flywheel already humming?\n\n"
            "Best,\n[Your Name]"
        ),
        "apollo_id": "hex_mccardel_10"
    }
]

def main():
    sheet_title = "Storylane RepX - B2B Prospecting Leads (Top 10 High-Intent)"
    print(f"Creating Google Spreadsheet: '{sheet_title}'...")
    sheet_info = create_prospecting_sheet(sheet_title)
    spreadsheet_id = sheet_info["spreadsheet_id"]
    sheet_url = sheet_info["url"]
    print(f"Spreadsheet created: {sheet_url}")
    
    print(f"Appending {len(leads)} enriched prospect records...")
    append_prospects(spreadsheet_id, leads)
    print("All records successfully written and formatted!")
    
    output_result = {
        "spreadsheet_id": spreadsheet_id,
        "url": sheet_url,
        "lead_count": len(leads)
    }
    with open("prospecting_batch_result.json", "w") as f:
        json.dump(output_result, f, indent=2)

if __name__ == "__main__":
    main()

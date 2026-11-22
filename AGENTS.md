# Prospecting Workspace Rules & Operating Protocol

These rules apply unconditionally across all conversations in this repository.

---

## 1. API Key Security & Confirmation Protocol (MANDATORY)
* **Never use Apollo or external paid APIs silently.**
* **Pre-Execution Confirmation**: Before making any Apollo API request (search, match, organization enrichment), you **MUST** prompt the user with their active masked key:
  > *"I am ready to run this query via Apollo using active API key `[MASKED_ACTIVE_KEY]`. Would you like to proceed with this key, or enter a different key?"*
* **Option to Change**: If the user provides a different API key, update `.env` and `config/credentials.json` immediately and use the new key from then on.
* **Zero Public Leakage**: Never commit real API keys, tokens, or credentials to git. All keys must remain in local, gitignored files (`.env`, `config/credentials.json`).

---

## 2. Fast-Start & Token Optimization (New Session Startup)
To prevent wasting tokens re-reading old session logs or asking redundant onboarding questions when a new conversation starts:
* **Immediate State Recognition**:
  * Check existing ICP files (`icp_*.md`, `icp_*.json` or `examples/`).
  * Check existing lead datasets (`prospects_*.csv`, `prospects_*.md`).
  * Check Google Drive / GSheets credentials and connected Google Workspace account.
* **Do NOT Re-scrape**: Never re-query or re-research companies or leads that are already saved in local datasets unless explicitly instructed to refresh them.
* **Direct Action Prompt**: Greet the user with a concise 2-sentence status of existing projects and ask directly which target company/product they want to prospect for next.

---

## 3. Skill & Tool Execution Standards
* **ICP Before Search**: Always validate or formulate the detailed ICP (Firmographics, Buyer Personas, Triggers, Apollo Filters) and get user confirmation before executing searches.
* **Swarm Research**: Fan out parallel research agents to extract 3–5 verifiable bullet points covering company growth, tech stack, and personal role priorities.
* **Google Sheets Logging**: Always use `scripts/sheets_logger.py` (`gsheets mutate import-csv`) to generate a professionally formatted spreadsheet with frozen, colored header rows in Google Drive, or fallback to local CSV when offline.

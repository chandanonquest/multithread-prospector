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
* **Company Suitability First**: Always qualify and analyze the company's macro situation, growth velocity, tech stack, and pain points before querying individual people. Generate a dedicated company intelligence dossier (`dossiers/dossier_<company_slug>.md`) for each qualified account.
* **Multi-Thread Stakeholder Ladder**: Map out contacts across 3 tiers (Managers for ground-truth warm-up -> Directors for functional championship -> VPs/CXOs for executive sign-off) to take multiple strategic shots per account.
* **Live-Call Google Sheets**: Always use `scripts/sheets_logger.py` (`gsheets mutate import-csv`) to populate the 17-column multi-thread matrix with company scenario and individual soundbites, frozen row 1, and colored headers, or fallback to local CSV when offline.

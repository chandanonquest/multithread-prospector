# Ideal Customer Profile (ICP) Framework

When analyzing a company and its products, extract and structure the following dimensions:

## 1. Product & Value Architecture
- **Core Value Proposition**: The singular primary benefit delivered.
- **Key Capabilities & Differentiators**: What sets it apart from incumbents.
- **Economic Impact**: How it increases revenue, cuts costs, or reduces risk.

## 2. Firmographic Target Boundaries
- **Industry Verticals**: Specific primary and secondary NAICS/industry groups.
- **Company Headcount**: E.g., Seed (1-10), Growth (11-50), Mid-Market (51-200, 201-500), Enterprise (500+).
- **Revenue / Funding Tier**: Minimum ARR or funding stage (Series A, B, Bootstrapped > \$5M).
- **Geography**: Primary operating locations (US, EMEA, APAC, global).
- **Business Model**: B2B SaaS, Marketplace, Fintech, Healthcare IT, E-commerce, etc.

## 3. Technographic & Stack Signals
- **Prerequisite Technologies**: Systems they must run (e.g., Salesforce, Snowflake, AWS, Kubernetes).
- **Complementary Tools**: Software that enhances compatibility.
- **Competitive Tools**: Competitor products indicating budget and recognized need.

## 4. Buyer Personas & Organizational Mapping
- **Economic Buyer**: Holds budget authority (e.g., CRO, CTO, VP Engineering, CFO).
- **Champion / Primary User**: Suffers the daily pain, drives internal advocacy (e.g., Dir of RevOps, Lead DevOps).
- **Key Influencers / Evaluators**: Security, Procurement, Legal.

## 5. Triggers & Buying Signals
- **Organizational Triggers**: New executive hires, team restructuring, sudden hiring spikes in relevant roles.
- **Operational Triggers**: Tech stack migrations, expansion into new markets, compliance deadlines.
- **Financial Triggers**: Recent funding announcements, M&A activity.

## 6. Apollo Search Filter Mapping
Translate the ICP directly into Apollo search parameters:
- `person_titles`: `["VP of Engineering", "Head of Infrastructure", "Director of Platform"]`
- `person_seniorities`: `["director", "vp", "c_suite"]`
- `organization_num_employees_ranges`: `["51,200", "201,500"]`
- `organization_locations`: `["United States", "Canada"]`
- `q_organization_keyword_tags`: `["SaaS", "Cloud", "Fintech"]`

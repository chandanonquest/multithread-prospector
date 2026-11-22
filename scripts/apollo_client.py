#!/usr/bin/env python3
"""
apollo_client.py
Interface for interacting with Apollo.io REST endpoints with secure credential management.
Supports organization enrichment and people/contact search with zero hardcoded secrets.
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "credentials.json")
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

def _load_env_file() -> Dict[str, str]:
    """Lightweight zero-dependency .env loader."""
    env_vars = {}
    if os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    env_vars[key] = val
        except Exception:
            pass
    return env_vars

def get_apollo_key() -> str:
    """
    Retrieves Apollo API key securely from:
    1. OS environment variable (APOLLO_API_KEY)
    2. Local .env file (APOLLO_API_KEY)
    3. Local config/credentials.json
    Raises ValueError if no key is configured. NEVER falls back to hardcoded strings.
    """
    # 1. Environment variable
    key = os.environ.get("APOLLO_API_KEY", "").strip()
    if key:
        return key

    # 2. Local .env
    env_vars = _load_env_file()
    key = env_vars.get("APOLLO_API_KEY", "").strip()
    if key:
        return key

    # 3. Local config/credentials.json
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                key = data.get("credentials", {}).get("apollo", {}).get("api_key", "").strip()
                if key:
                    return key
        except Exception:
            pass

    return ""

def require_apollo_key() -> str:
    """Returns the Apollo API key or raises a user-friendly error."""
    key = get_apollo_key()
    if not key:
        raise ValueError(
            "Apollo API key not found! Please set APOLLO_API_KEY in your local .env file, "
            "set the environment variable, or configure config/credentials.json locally. "
            "See .env.example for guidance."
        )
    return key

def set_apollo_key(new_key: str, plan: str = "Free") -> bool:
    """Updates the stored Apollo API key in local config/credentials.json."""
    data = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    
    if "credentials" not in data:
        data["credentials"] = {}
    data["credentials"]["apollo"] = {
        "service": "Apollo.io",
        "api_key": new_key,
        "plan": plan
    }
    
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return True

def mask_key(key: str) -> str:
    """Masks an API key for safe display in logs and prompts."""
    if not key or len(key) < 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"

BASE_URL = "https://api.apollo.io/v1"

def _make_request(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json_body: Optional[Dict[str, Any]] = None,
    method: str = "GET"
) -> Dict[str, Any]:
    """Executes an authenticated HTTP request to Apollo REST API."""
    key = require_apollo_key()
    url = f"{BASE_URL}/{endpoint}"
    
    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"
    
    headers = {
        "x-api-key": key,
        "Content-Type": "application/json"
    }
    
    data = json.dumps(json_body).encode("utf-8") if json_body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return json.loads(err_body)
        except Exception:
            return {"error": str(e), "status_code": e.code, "body": err_body}
    except Exception as e:
        return {"error": str(e)}

def check_health() -> Dict[str, Any]:
    """Checks Apollo API connection health."""
    return _make_request("auth/health")

def enrich_organization(domain: str) -> Dict[str, Any]:
    """
    Enriches organization details including technographics, department sizes,
    and headcount growth via Apollo.
    """
    res = _make_request("organizations/enrich", {"domain": domain})
    org = res.get("organization", {})
    if not org:
        return res
    
    tech_stack = [t.get("name") for t in org.get("technologies", [])[:20]]
    department_counts = org.get("departmental_head_count", {})
    
    return {
        "name": org.get("name"),
        "primary_domain": org.get("primary_domain"),
        "industry": org.get("industry"),
        "estimated_num_employees": org.get("estimated_num_employees"),
        "headcount_6m_growth": org.get("organization_headcount_six_month_growth"),
        "headcount_12m_growth": org.get("organization_headcount_twelve_month_growth"),
        "department_headcounts": department_counts,
        "technologies": tech_stack,
        "keywords": org.get("keywords", [])[:15],
        "linkedin_url": org.get("linkedin_url"),
        "phone": org.get("primary_phone", {}).get("number")
    }

def search_people(
    person_titles: Optional[List[str]] = None,
    person_seniorities: Optional[List[str]] = None,
    organization_locations: Optional[List[str]] = None,
    organization_num_employees_ranges: Optional[List[str]] = None,
    q_organization_keyword_tags: Optional[List[str]] = None,
    per_page: int = 10,
    page: int = 1
) -> Dict[str, Any]:
    """
    Directly queries Apollo mixed_people/search endpoint for prospective decision makers.
    """
    payload: Dict[str, Any] = {
        "page": page,
        "per_page": per_page
    }
    if person_titles:
        payload["person_titles"] = person_titles
    if person_seniorities:
        payload["person_seniorities"] = person_seniorities
    if organization_locations:
        payload["organization_locations"] = organization_locations
    if organization_num_employees_ranges:
        payload["organization_num_employees_ranges"] = organization_num_employees_ranges
    if q_organization_keyword_tags:
        payload["q_organization_keyword_tags"] = q_organization_keyword_tags
        
    return _make_request("mixed_people/search", json_body=payload, method="POST")

if __name__ == "__main__":
    current_key = get_apollo_key()
    if current_key:
        print("Configured Apollo Key:", mask_key(current_key))
        print("Health check:", check_health())
    else:
        print("No Apollo API key detected. Please configure .env or config/credentials.json locally.")

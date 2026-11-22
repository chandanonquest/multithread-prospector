#!/usr/bin/env python3
"""
verify_no_secrets.py
Pre-commit / CI scanner that validates that no real API keys, credentials,
or sensitive PII are tracked or committed to version control.
"""

import os
import re
import sys
from typing import List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Suspicious key patterns to detect
SECRET_PATTERNS = [
    (r"(?i)m2fcvh[a-zA-Z0-9_-]{16}", "Apollo Active API Key"),
    (r"(?i)api_key[\"']?\s*[:=]\s*[\"']([a-zA-Z0-9_-]{20,})[\"']", "Generic API Key Assignment"),
    (r"(?i)x-api-key[\"']?\s*[:=]\s*[\"']([a-zA-Z0-9_-]{20,})[\"']", "Header API Key"),
    (r"AIza[0-9A-Za-z-_]{35}", "Google API Key"),
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"sk-[a-zA-Z0-9]{32,}", "OpenAI Secret Key"),
    (r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", "Private Key Header"),
]

# Patterns allowed in example/template files
PLACEHOLDER_SUBSTRINGS = [
    "YOUR_APOLLO_API_KEY_HERE",
    "your_apollo_api_key_here",
    "[MASKED_ACTIVE_KEY]",
    "your_email@gmail.com",
    "placeholder",
    "sample",
    "example",
    "****"
]

IGNORED_DIRS = {".git", "__pycache__", ".venv", "venv", "env", "node_modules"}
IGNORED_FILES = {".env", "credentials.json", "mcp_config.json"}

def is_secret_allowed(match_text: str) -> bool:
    for ph in PLACEHOLDER_SUBSTRINGS:
        if ph in match_text:
            return True
    return False

def scan_file(filepath: str) -> List[Tuple[int, str, str]]:
    """Scans a file for potential secrets. Returns (line_no, description, line)."""
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, 1):
                # Skip comments that explain patterns
                if "verify_no_secrets.py" in filepath and "r\"" in line:
                    continue
                for pattern, desc in SECRET_PATTERNS:
                    match = re.search(pattern, line)
                    if match:
                        matched_str = match.group(0)
                        if not is_secret_allowed(matched_str) and not is_secret_allowed(line):
                            findings.append((line_no, desc, line.strip()))
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    return findings

def check_gitignore() -> bool:
    """Verifies that .gitignore contains mandatory secret exclusions."""
    gitignore_path = os.path.join(PROJECT_ROOT, ".gitignore")
    if not os.path.exists(gitignore_path):
        print("FAIL: .gitignore does not exist!")
        return False
        
    required_ignores = [".env", "config/credentials.json", ".agents/plugins/apollo/mcp_config.json"]
    with open(gitignore_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    missing = [req for req in required_ignores if req not in content]
    if missing:
        print(f"FAIL: .gitignore is missing mandatory rules: {missing}")
        return False
        
    return True

def main():
    print("=" * 60)
    print("Running Repository Secret & Credential Pre-flight Scan")
    print("=" * 60)
    
    # 1. Verify .gitignore
    if not check_gitignore():
        sys.exit(1)
    print("[PASS] .gitignore includes all mandatory secret rules.")
    
    # 2. Walk project and scan all tracked/candidate files
    all_findings = []
    total_files = 0
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        # Check if directory itself should be ignored
        rel_root = os.path.relpath(root, PROJECT_ROOT)
        
        for file in files:
            # Skip local untracked secret files
            if file in IGNORED_FILES:
                continue
            if file.startswith("prospects_") or file.startswith("icp_") or file.endswith(".pdf"):
                # Untracked output data files
                continue
                
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, PROJECT_ROOT)
            
            total_files += 1
            findings = scan_file(filepath)
            if findings:
                for line_no, desc, line in findings:
                    all_findings.append((rel_path, line_no, desc, line))

    print(f"[INFO] Scanned {total_files} repository files.")
    
    if all_findings:
        print("\n" + "!" * 60)
        print("FAIL: Potential secrets or unmasked keys found in tracked files:")
        print("!" * 60)
        for rel_path, line_no, desc, line in all_findings:
            print(f"  • {rel_path}:{line_no} [{desc}] -> {line[:60]}...")
        print("\nPlease remove the secret or use environment variables before committing.")
        sys.exit(1)
        
    print("[PASS] ZERO hardcoded secrets detected in repository files!")
    print("=" * 60)
    sys.exit(0)

if __name__ == "__main__":
    main()

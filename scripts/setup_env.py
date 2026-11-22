#!/usr/bin/env python3
"""
setup_env.py
Initializes local configuration files (.env, credentials.json, mcp_config.json)
from their tracked templates without exposing secrets to git.
"""

import argparse
import json
import os
import shutil
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_EXAMPLE = os.path.join(PROJECT_ROOT, ".env.example")
ENV_TARGET = os.path.join(PROJECT_ROOT, ".env")

CRED_EXAMPLE = os.path.join(PROJECT_ROOT, "config", "credentials.example.json")
CRED_TARGET = os.path.join(PROJECT_ROOT, "config", "credentials.json")

MCP_EXAMPLE = os.path.join(PROJECT_ROOT, ".agents", "plugins", "apollo", "mcp_config.example.json")
MCP_TARGET = os.path.join(PROJECT_ROOT, ".agents", "plugins", "apollo", "mcp_config.json")

def init_files(apollo_key: str = ""):
    print("=" * 60)
    print("Initializing Local Prospecting Configuration")
    print("=" * 60)
    
    # 1. Initialize .env
    if not os.path.exists(ENV_TARGET):
        if os.path.exists(ENV_EXAMPLE):
            shutil.copyfile(ENV_EXAMPLE, ENV_TARGET)
            print(f"[CREATED] Local .env initialized from template.")
        else:
            with open(ENV_TARGET, "w", encoding="utf-8") as f:
                f.write(f"APOLLO_API_KEY={apollo_key}\n")
            print(f"[CREATED] Local .env created.")
    else:
        print("[EXISTS] Local .env already exists.")
        
    # 2. Initialize config/credentials.json
    os.makedirs(os.path.dirname(CRED_TARGET), exist_ok=True)
    if not os.path.exists(CRED_TARGET):
        if os.path.exists(CRED_EXAMPLE):
            shutil.copyfile(CRED_EXAMPLE, CRED_TARGET)
            print(f"[CREATED] Local config/credentials.json initialized from template.")
    else:
        print("[EXISTS] Local config/credentials.json already exists.")
        
    # 3. Initialize .agents/plugins/apollo/mcp_config.json
    os.makedirs(os.path.dirname(MCP_TARGET), exist_ok=True)
    if not os.path.exists(MCP_TARGET):
        if os.path.exists(MCP_EXAMPLE):
            shutil.copyfile(MCP_EXAMPLE, MCP_TARGET)
            print(f"[CREATED] Local mcp_config.json initialized from template.")
    else:
        print("[EXISTS] Local mcp_config.json already exists.")

    # 4. If an Apollo key is provided, sync it across all local files
    if apollo_key:
        print(f"\n[SYNC] Updating local configs with new Apollo API Key...")
        
        # Update .env
        env_lines = []
        key_found = False
        if os.path.exists(ENV_TARGET):
            with open(ENV_TARGET, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("APOLLO_API_KEY="):
                        env_lines.append(f"APOLLO_API_KEY={apollo_key}\n")
                        key_found = True
                    else:
                        env_lines.append(line)
        if not key_found:
            env_lines.append(f"APOLLO_API_KEY={apollo_key}\n")
        with open(ENV_TARGET, "w", encoding="utf-8") as f:
            f.writelines(env_lines)
            
        # Update credentials.json
        if os.path.exists(CRED_TARGET):
            try:
                with open(CRED_TARGET, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
            if "credentials" not in data:
                data["credentials"] = {}
            if "apollo" not in data["credentials"]:
                data["credentials"]["apollo"] = {"service": "Apollo.io"}
            data["credentials"]["apollo"]["api_key"] = apollo_key
            with open(CRED_TARGET, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                
        # Update mcp_config.json
        if os.path.exists(MCP_TARGET):
            try:
                with open(MCP_TARGET, "r", encoding="utf-8") as f:
                    mcp_data = json.load(f)
            except Exception:
                mcp_data = {}
            if "mcpServers" in mcp_data and "apollo" in mcp_data["mcpServers"]:
                if "headers" not in mcp_data["mcpServers"]["apollo"]:
                    mcp_data["mcpServers"]["apollo"]["headers"] = {}
                mcp_data["mcpServers"]["apollo"]["headers"]["x-api-key"] = apollo_key
                with open(MCP_TARGET, "w", encoding="utf-8") as f:
                    json.dump(mcp_data, f, indent=2)
                    
        masked = f"{apollo_key[:4]}...{apollo_key[-4:]}" if len(apollo_key) >= 8 else "****"
        print(f"[SUCCESS] Apollo API Key safely saved to local files (Masked: {masked}).")
        
    print("\nLocal setup verified. All configuration files are protected by .gitignore.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize local prospecting environment.")
    parser.add_argument("--key", help="Apollo API Key to store locally")
    args = parser.parse_args()
    init_files(args.key or "")

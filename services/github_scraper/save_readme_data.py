#!/usr/bin/env python3
"""
GitHub README Data Saver

This script fetches data from the GitHub README Scraper API and saves it locally
in an organized directory structure.
"""
import json
import os
import sys
import requests
from pathlib import Path
from typing import Dict, List, Any

# API Configuration
API_BASE_URL = "http://127.0.0.1:8001/api"

def ensure_dir(directory: str) -> None:
    """Create directory if it doesn't exist"""
    Path(directory).mkdir(parents=True, exist_ok=True)

def save_json(data: Dict[str, Any], filepath: str) -> None:
    """Save data as a JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved: {filepath}")

def fetch_and_save_readmes(username: str, include_orgs: bool = True, output_dir: str = "output") -> None:
    """Fetch and save README data from a GitHub user and their organizations"""
    base_output_dir = os.path.join(output_dir, username)
    ensure_dir(base_output_dir)
    
    print(f"🔍 Fetching data for GitHub user: {username}")
    
    # Save user repositories
    print(f"📚 Fetching repositories...")
    repos_response = requests.get(f"{API_BASE_URL}/users/{username}/repositories")
    
    if repos_response.status_code == 200:
        repos_data = repos_response.json()
        save_json(repos_data, os.path.join(base_output_dir, "repositories.json"))
        print(f"Found {repos_data['count']} repositories")
    else:
        print(f"❌ Error fetching repositories: {repos_response.status_code}")
        return
    
    # Save user READMEs
    print(f"📝 Fetching READMEs (include_orgs={include_orgs})...")
    readmes_response = requests.get(
        f"{API_BASE_URL}/users/{username}/readmes?include_orgs={str(include_orgs).lower()}"
    )
    
    if readmes_response.status_code == 200:
        readmes_data = readmes_response.json()
        save_json(readmes_data, os.path.join(base_output_dir, "all_readmes.json"))
        print(f"Found {readmes_data['count']} READMEs")
        
        # Create individual README files organized by repo
        readme_dir = os.path.join(base_output_dir, "readmes")
        ensure_dir(readme_dir)
        
        for readme in readmes_data["readmes"]:
            # Create directories for organization repos
            if readme["is_from_org"] and readme["org_name"]:
                repo_dir = os.path.join(readme_dir, "organizations", readme["org_name"])
            else:
                repo_dir = os.path.join(readme_dir, "personal")
            
            ensure_dir(repo_dir)
            
            # Save README content and metadata separately
            repo_name = readme["repo_name"]
            
            # Save README content as markdown
            with open(os.path.join(repo_dir, f"{repo_name}_README.md"), 'w', encoding='utf-8') as f:
                f.write(readme["content"])
            
            # Save repo metadata as JSON
            metadata = {k: v for k, v in readme.items() if k != "content"}
            save_json(metadata, os.path.join(repo_dir, f"{repo_name}_metadata.json"))
    else:
        print(f"❌ Error fetching READMEs: {readmes_response.status_code}")
    
    # Save user organizations if requested
    if include_orgs:
        print(f"🏢 Fetching organizations...")
        orgs_response = requests.get(f"{API_BASE_URL}/users/{username}/organizations")
        
        if orgs_response.status_code == 200:
            orgs_data = orgs_response.json()
            save_json(orgs_data, os.path.join(base_output_dir, "organizations.json"))
            print(f"Found {orgs_data['count']} organizations")
        else:
            print(f"❌ Error fetching organizations: {orgs_response.status_code}")
    
    print(f"✅ All data saved successfully to: {base_output_dir}")
    print(f"📁 Directory structure:")
    print(f"  {base_output_dir}/")
    print(f"  ├── repositories.json            # All repositories")
    print(f"  ├── all_readmes.json             # All READMEs with metadata")
    print(f"  ├── organizations.json           # Organizations info")
    print(f"  └── readmes/                     # Individual READMEs")
    print(f"      ├── personal/                # User's personal repos")
    print(f"      │   ├── {repos_data['repositories'][0]['name'] if repos_data['count'] > 0 else 'repo'}_README.md")
    print(f"      │   └── {repos_data['repositories'][0]['name'] if repos_data['count'] > 0 else 'repo'}_metadata.json")
    print(f"      └── organizations/           # Organization repos")
    print(f"          └── [org_name]/          # Organized by org name")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python save_readme_data.py [github_username] [include_orgs=true/false] [output_dir=output]")
        sys.exit(1)
    
    username = sys.argv[1]
    include_orgs = True if len(sys.argv) < 3 else sys.argv[2].lower() == "true"
    output_dir = "output" if len(sys.argv) < 4 else sys.argv[3]
    
    fetch_and_save_readmes(username, include_orgs, output_dir)

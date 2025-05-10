#!/usr/bin/env python3
"""
GitHub README Scraper

This script fetches all README files from public repositories of a specified GitHub user
and saves them to a JSON file in the bucket directory.
"""

import os
import json
import base64
import argparse
import requests
from datetime import datetime
from github import Github
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_github_token():
    """Get GitHub token from environment variables."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GitHub token not found. Please ensure GITHUB_TOKEN is set in .env file.")
    return token

def fetch_readme_content(repo):
    """Fetch README content from a repository."""
    try:
        # Try to get README with various common filenames
        for readme_name in ["README.md", "README", "readme.md", "Readme.md", "readme"]:
            try:
                # First try using the API to get the raw content
                try:
                    # Direct download URL for README (handles large files)
                    raw_url = f"https://raw.githubusercontent.com/{repo.full_name}/{repo.default_branch}/{readme_name}"
                    response = requests.get(raw_url)
                    if response.status_code == 200:
                        return response.text
                except Exception:
                    pass
                    
                # Fall back to GitHub API if direct download fails
                contents = repo.get_contents(readme_name)
                if isinstance(contents, list):
                    # If get_contents returns a list, find the README in it
                    for content in contents:
                        if content.name.lower().startswith("readme"):
                            contents = content
                            break
                    else:
                        continue
                
                # Decode content from base64
                if contents.encoding == "base64":
                    return base64.b64decode(contents.content).decode('utf-8')
                return contents.content
                
            except Exception:
                continue
                
        # If no README found with common names, return empty string
        return ""
        
    except Exception as e:
        print(f"Error fetching README from {repo.full_name}: {str(e)}")
        return ""

def scrape_github_readmes(username):
    """
    Scrape README files from all public repositories of a GitHub user.
    
    Args:
        username: GitHub username
        
    Returns:
        Dictionary with repository names as keys and README contents as values
    """
    token = get_github_token()
    g = Github(token)
    
    try:
        # Get the user and their repositories
        user = g.get_user(username)
        repos = user.get_repos(type="public")
        
        # Create a dictionary to store repository names and their README contents
        readmes = {}
        
        print(f"Fetching READMEs from {username}'s repositories...")
        
        # Iterate through repositories
        for repo in repos:
            print(f"Processing {repo.full_name}...")
            
            # Get README content
            readme_content = fetch_readme_content(repo)
            
            # Get repository languages - extract only the names without byte counts
            languages_dict = repo.get_languages()
            languages = list(languages_dict.keys()) if languages_dict else []
            
            # Add to dictionary
            readmes[repo.full_name] = {
                "name": repo.name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "last_updated": repo.updated_at.isoformat() if repo.updated_at else None,
                "languages": languages,
                "readme": readme_content
            }
            
        return readmes
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {}

def save_to_json(data, username):
    """Save data to JSON file in the bucket directory."""
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename with username and timestamp
    filename = f"{username}_github_readmes_{timestamp}.json"
    
    # Path to bucket directory
    bucket_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "bucket")
    
    # Full path to output file
    output_path = os.path.join(bucket_dir, filename)
    
    # Save data to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved README data to {output_path}")
    return output_path

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Scrape README files from all public repositories of a GitHub user')
    parser.add_argument('username', type=str, help='GitHub username')
    args = parser.parse_args()
    
    # Scrape READMEs
    readmes = scrape_github_readmes(args.username)
    
    # Check if any READMEs were found
    if not readmes:
        print(f"No repositories found for user {args.username} or an error occurred.")
        return
    
    # Save to JSON
    output_path = save_to_json(readmes, args.username)
    print(f"Scraped {len(readmes)} repositories from {args.username}.")
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()

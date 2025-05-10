#!/usr/bin/env python3
"""
GitHub README Direct Downloader

Downloads GitHub READMEs and repository metadata directly using PyGithub
without relying on the API server.
"""
import os
import json
import base64
import time
from pathlib import Path
from dotenv import load_dotenv
from github import Github, RateLimitExceededException, GithubException

# Load environment variables
load_dotenv()

# Config
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is required")

def ensure_dir(directory):
    """Create directory if it doesn't exist"""
    Path(directory).mkdir(parents=True, exist_ok=True)

def handle_rate_limit(github_client):
    """Handle GitHub API rate limits by waiting if needed"""
    rate_limit = github_client.get_rate_limit()
    core = rate_limit.core
    
    if core.remaining < 10:
        reset_time = core.reset.timestamp() - time.time()
        if reset_time > 0:
            print(f"⚠️ Rate limit nearly exceeded. Waiting for {reset_time:.2f} seconds")
            time.sleep(reset_time + 1)

def fetch_github_data(username, include_orgs=True, output_dir="output"):
    """Fetch GitHub data for a user and save locally"""
    # Initialize GitHub client
    github_client = Github(GITHUB_TOKEN)
    
    # Create output directory
    base_dir = os.path.join(output_dir, username)
    ensure_dir(base_dir)
    readme_dir = os.path.join(base_dir, "readmes")
    ensure_dir(readme_dir)
    
    print(f"🔍 Fetching GitHub data for: {username}")
    
    try:
        # Get user
        handle_rate_limit(github_client)
        user = github_client.get_user(username)
        
        # Get user's repositories
        print(f"📚 Fetching repositories...")
        repos = []
        personal_readme_dir = os.path.join(readme_dir, "personal")
        ensure_dir(personal_readme_dir)
        
        for repo in user.get_repos():
            repo_data = {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "html_url": repo.html_url,
                "language": repo.language,
                "stars_count": repo.stargazers_count,
                "forks_count": repo.forks_count,
                "watchers_count": repo.watchers_count,
                "open_issues_count": repo.open_issues_count,
                "created_at": repo.created_at.isoformat() if repo.created_at else None,
                "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                "topics": repo.get_topics(),
                "is_private": repo.private,
                "homepage": repo.homepage,
            }
            
            # Get license information if available
            if repo.license and hasattr(repo.license, "name"):
                repo_data["license_name"] = repo.license.name
            
            repos.append(repo_data)
            
            # Save repo metadata
            repo_metadata_path = os.path.join(personal_readme_dir, f"{repo.name}_metadata.json")
            with open(repo_metadata_path, 'w', encoding='utf-8') as f:
                json.dump(repo_data, f, indent=2, ensure_ascii=False)
            
            # Try to get README
            try:
                handle_rate_limit(github_client)
                readme = repo.get_readme()
                
                # Decode content from base64
                readme_content = base64.b64decode(readme.content).decode('utf-8')
                
                # Save README content
                readme_path = os.path.join(personal_readme_dir, f"{repo.name}_README.md")
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(readme_content)
                print(f"  ✅ Saved README for: {repo.name}")
            
            except (GithubException, UnicodeDecodeError) as e:
                print(f"  ⚠️ No README found for {repo.name}: {str(e)}")
        
        # Save all repositories data
        repos_path = os.path.join(base_dir, "repositories.json")
        with open(repos_path, 'w', encoding='utf-8') as f:
            json.dump({
                "username": username,
                "repositories": repos,
                "count": len(repos)
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(repos)} repositories")
        
        # Get organizations if requested
        if include_orgs:
            print(f"🏢 Fetching organizations...")
            orgs = []
            
            for org in user.get_orgs():
                handle_rate_limit(github_client)
                
                org_data = {
                    "login": org.login,
                    "name": org.name,
                    "url": org.html_url,
                    "description": org.description,
                }
                orgs.append(org_data)
                
                # Create org directory
                org_dir = os.path.join(readme_dir, "organizations", org.login)
                ensure_dir(org_dir)
                
                # Get org repositories
                try:
                    print(f"  📂 Fetching repositories for org: {org.login}")
                    org_repos = []
                    
                    for repo in org.get_repos():
                        handle_rate_limit(github_client)
                        
                        repo_data = {
                            "name": repo.name,
                            "full_name": repo.full_name,
                            "description": repo.description,
                            "html_url": repo.html_url,
                            "language": repo.language,
                            "stars_count": repo.stargazers_count,
                            "forks_count": repo.forks_count,
                            "watchers_count": repo.watchers_count,
                            "open_issues_count": repo.open_issues_count,
                            "created_at": repo.created_at.isoformat() if repo.created_at else None,
                            "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                            "topics": repo.get_topics(),
                            "is_private": repo.private,
                            "homepage": repo.homepage,
                            "is_from_org": True,
                            "org_name": org.login
                        }
                        
                        # Get license information if available
                        if repo.license and hasattr(repo.license, "name"):
                            repo_data["license_name"] = repo.license.name
                        
                        org_repos.append(repo_data)
                        
                        # Save repo metadata
                        repo_metadata_path = os.path.join(org_dir, f"{repo.name}_metadata.json")
                        with open(repo_metadata_path, 'w', encoding='utf-8') as f:
                            json.dump(repo_data, f, indent=2, ensure_ascii=False)
                        
                        # Try to get README
                        try:
                            handle_rate_limit(github_client)
                            readme = repo.get_readme()
                            
                            # Decode content from base64
                            readme_content = base64.b64decode(readme.content).decode('utf-8')
                            
                            # Save README content
                            readme_path = os.path.join(org_dir, f"{repo.name}_README.md")
                            with open(readme_path, 'w', encoding='utf-8') as f:
                                f.write(readme_content)
                            print(f"    ✅ Saved README for: {repo.name}")
                        
                        except (GithubException, UnicodeDecodeError) as e:
                            print(f"    ⚠️ No README found for {repo.name}: {str(e)}")
                    
                    # Save org repositories
                    org_repos_path = os.path.join(org_dir, "_repositories.json")
                    with open(org_repos_path, 'w', encoding='utf-8') as f:
                        json.dump({
                            "org_name": org.login,
                            "repositories": org_repos,
                            "count": len(org_repos)
                        }, f, indent=2, ensure_ascii=False)
                
                except GithubException as e:
                    print(f"  ❌ Error fetching repositories for {org.login}: {str(e)}")
            
            # Save all organizations data
            orgs_path = os.path.join(base_dir, "organizations.json")
            with open(orgs_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "username": username,
                    "organizations": orgs,
                    "count": len(orgs)
                }, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {len(orgs)} organizations")
        
        print(f"🎉 All data successfully saved to: {base_dir}")
        return True
    
    except RateLimitExceededException:
        print("❌ GitHub API rate limit exceeded. Try again later.")
        return False
    
    except GithubException as e:
        print(f"❌ GitHub API error: {str(e)}")
        return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python direct_download.py [github_username] [include_orgs=true/false] [output_dir=output]")
        sys.exit(1)
    
    username = sys.argv[1]
    include_orgs = True if len(sys.argv) < 3 else sys.argv[2].lower() == "true"
    output_dir = "output" if len(sys.argv) < 4 else sys.argv[3]
    
    success = fetch_github_data(username, include_orgs, output_dir)
    if success:
        print("✅ Download complete!")
    else:
        print("❌ Download failed!")

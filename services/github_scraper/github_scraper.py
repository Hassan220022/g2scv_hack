"""
GitHub README Scraper Module
- Fetches READMEs from user repositories and organizations
- Handles pagination, rate limits, and authentication
"""
import base64
import json
import os
import time
from typing import Dict, List, Optional, Union, Any

import requests
from github import Github, GithubException, RateLimitExceededException
from pydantic import BaseModel

class GitHubReadme(BaseModel):
    """Model for README content"""
    repo_name: str
    repo_full_name: str
    repo_description: Optional[str] = None
    repo_url: str
    content: str
    html_url: str
    size: int
    encoding: str
    is_from_org: bool = False
    org_name: Optional[str] = None
    # About section metadata
    topics: List[str] = []
    website: Optional[str] = None
    homepage_url: Optional[str] = None
    language: Optional[str] = None
    stars_count: int = 0
    forks_count: int = 0
    watchers_count: int = 0
    open_issues_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    license_name: Optional[str] = None

class GitHubOrg(BaseModel):
    """Model for organization data"""
    login: str
    name: Optional[str] = None
    url: str
    repos_url: str
    description: Optional[str] = None

class GitHubScraper:
    """GitHub API client for scraping READMEs from user and org repositories"""
    
    def __init__(self, token: str):
        """Initialize with GitHub token"""
        self.token = token
        self.github_client = Github(token)
        self.session = self._create_session()
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-README-Scraper/1.0"
        }
        
    def _create_session(self) -> requests.Session:
        """Create a resilient session with retries"""
        session = requests.Session()
        session.headers.update({
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-README-Scraper/1.0"
        })
        return session
    
    def _handle_rate_limit(self) -> None:
        """Handle GitHub API rate limits by waiting if needed"""
        rate_limit = self.github_client.get_rate_limit()
        core = rate_limit.core
        
        if core.remaining < 10:
            reset_time = core.reset.timestamp() - time.time()
            if reset_time > 0:
                print(f"Rate limit nearly exceeded. Waiting for {reset_time:.2f} seconds")
                time.sleep(reset_time + 1)
    
    def get_user_repos(self, username: str) -> List[Dict[str, Any]]:
        """Get all repositories for a user"""
        try:
            self._handle_rate_limit()
            user = self.github_client.get_user(username)
            repos = []
            
            for repo in user.get_repos():
                repos.append({
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "html_url": repo.html_url,
                    "url": repo.url,
                    "is_private": repo.private
                })
            
            return repos
        except RateLimitExceededException:
            self._handle_rate_limit()
            return self.get_user_repos(username)
        except GithubException as e:
            print(f"Error getting repositories for user {username}: {e}")
            return []
    
    def get_user_orgs(self, username: str) -> List[GitHubOrg]:
        """Get organizations a user belongs to"""
        try:
            self._handle_rate_limit()
            
            # Check if we're querying the authenticated user
            auth_user_response = self.session.get(f"{self.api_base}/user")
            auth_user = auth_user_response.json().get("login", "")
            
            if auth_user.lower() == username.lower():
                # Get all orgs including private memberships
                url = f"{self.api_base}/user/orgs"
            else:
                # Get only public orgs
                url = f"{self.api_base}/users/{username}/orgs"
            
            orgs = []
            page = 1
            
            while True:
                response = self.session.get(f"{url}?page={page}&per_page=100")
                if response.status_code != 200:
                    break
                
                org_data = response.json()
                if not org_data:
                    break
                
                for org in org_data:
                    orgs.append(GitHubOrg(
                        login=org["login"],
                        name=org.get("name"),
                        url=org["url"],
                        repos_url=org["repos_url"],
                        description=org.get("description")
                    ))
                
                page += 1
            
            return orgs
        except Exception as e:
            print(f"Error getting organizations for user {username}: {e}")
            return []
    
    def get_org_repos(self, org_name: str) -> List[Dict[str, Any]]:
        """Get all repositories for an organization"""
        try:
            self._handle_rate_limit()
            org = self.github_client.get_organization(org_name)
            repos = []
            
            for repo in org.get_repos():
                repos.append({
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "html_url": repo.html_url,
                    "url": repo.url,
                    "is_private": repo.private
                })
            
            return repos
        except RateLimitExceededException:
            self._handle_rate_limit()
            return self.get_org_repos(org_name)
        except GithubException as e:
            print(f"Error getting repositories for organization {org_name}: {e}")
            return []
    
    def get_readme(self, owner: str, repo: str, is_org: bool = False, org_name: str = None) -> Optional[GitHubReadme]:
        """Get README for a specific repository"""
        try:
            self._handle_rate_limit()
            
            # Get repository to fetch additional metadata
            repo_obj = self.github_client.get_repo(f"{owner}/{repo}")
            
            # Get README content
            try:
                readme = repo_obj.get_readme()
                
                # Decode content from base64
                content = base64.b64decode(readme.content).decode("utf-8")
                
                # Get repository topics/tags
                topics = repo_obj.get_topics()
                
                # Get license information if available
                license_name = None
                if repo_obj.license and repo_obj.license.name:
                    license_name = repo_obj.license.name
                
                return GitHubReadme(
                    repo_name=repo_obj.name,
                    repo_full_name=repo_obj.full_name,
                    repo_description=repo_obj.description,
                    repo_url=repo_obj.html_url,
                    content=content,
                    html_url=readme.html_url,
                    size=readme.size,
                    encoding=readme.encoding,
                    is_from_org=is_org,
                    org_name=org_name,
                    # About section metadata
                    topics=topics,
                    website=repo_obj.homepage,
                    homepage_url=repo_obj.homepage,
                    language=repo_obj.language,
                    stars_count=repo_obj.stargazers_count,
                    forks_count=repo_obj.forks_count,
                    watchers_count=repo_obj.watchers_count,
                    open_issues_count=repo_obj.open_issues_count,
                    created_at=repo_obj.created_at.isoformat() if repo_obj.created_at else None,
                    updated_at=repo_obj.updated_at.isoformat() if repo_obj.updated_at else None,
                    license_name=license_name
                )
            except GithubException as e:
                if e.status == 404:
                    print(f"README not found for {owner}/{repo}")
                return None
                
        except RateLimitExceededException:
            self._handle_rate_limit()
            return self.get_readme(owner, repo, is_org, org_name)
        except GithubException as e:
            print(f"Error getting README for {owner}/{repo}: {e}")
            return None
    
    def get_all_user_readmes(self, username: str, include_orgs: bool = True) -> List[GitHubReadme]:
        """Get all READMEs from user repositories and optionally organization repositories"""
        all_readmes = []
        
        # Get user's repositories
        user_repos = self.get_user_repos(username)
        for repo in user_repos:
            repo_name = repo["name"]
            readme = self.get_readme(username, repo_name)
            if readme:
                all_readmes.append(readme)
        
        # Get organization repositories if requested
        if include_orgs:
            orgs = self.get_user_orgs(username)
            for org in orgs:
                org_repos = self.get_org_repos(org.login)
                for repo in org_repos:
                    repo_name = repo["name"]
                    readme = self.get_readme(org.login, repo_name, is_org=True, org_name=org.login)
                    if readme:
                        all_readmes.append(readme)
        
        return all_readmes

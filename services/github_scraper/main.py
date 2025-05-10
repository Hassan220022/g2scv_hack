"""
GitHub README Scraper API
FastAPI application to scrape READMEs from GitHub users and organizations
"""
import os
from typing import Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from github_scraper import GitHubScraper, GitHubReadme, GitHubOrg

# Load environment variables
load_dotenv()

# Get GitHub token from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is required")

# Create FastAPI app
app = FastAPI(
    title="GitHub README Scraper API",
    description="API for scraping README files from GitHub users and organizations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class UserRepositoriesResponse(BaseModel):
    username: str
    repositories: List[Dict]
    count: int

class OrganizationsResponse(BaseModel):
    username: str
    organizations: List[GitHubOrg]
    count: int

class ReadmesResponse(BaseModel):
    username: str
    include_orgs: bool
    readmes: List[GitHubReadme]
    count: int

# Dependency to get the GitHub scraper client
def get_github_scraper():
    try:
        return GitHubScraper(token=GITHUB_TOKEN)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize GitHub client: {str(e)}"
        )

@app.get("/", tags=["Status"])
async def read_root():
    """API Health Check"""
    return {"status": "healthy", "message": "GitHub README Scraper API is running"}

@app.get("/api/users/{username}/repositories", response_model=UserRepositoriesResponse, tags=["Repositories"])
async def get_user_repositories(
    username: str,
    github_scraper: GitHubScraper = Depends(get_github_scraper)
):
    """Get all repositories for a GitHub user"""
    try:
        repos = github_scraper.get_user_repos(username)
        return {
            "username": username,
            "repositories": repos,
            "count": len(repos)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get repositories: {str(e)}"
        )

@app.get("/api/users/{username}/organizations", response_model=OrganizationsResponse, tags=["Organizations"])
async def get_user_organizations(
    username: str,
    github_scraper: GitHubScraper = Depends(get_github_scraper)
):
    """Get all organizations a GitHub user belongs to"""
    try:
        orgs = github_scraper.get_user_orgs(username)
        return {
            "username": username,
            "organizations": orgs,
            "count": len(orgs)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get organizations: {str(e)}"
        )

@app.get("/api/organizations/{org_name}/repositories", response_model=UserRepositoriesResponse, tags=["Repositories"])
async def get_organization_repositories(
    org_name: str,
    github_scraper: GitHubScraper = Depends(get_github_scraper)
):
    """Get all repositories for a GitHub organization"""
    try:
        repos = github_scraper.get_org_repos(org_name)
        return {
            "username": org_name,  # Using username field for org name
            "repositories": repos,
            "count": len(repos)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get organization repositories: {str(e)}"
        )

@app.get("/api/users/{username}/readmes", response_model=ReadmesResponse, tags=["READMEs"])
async def get_user_readmes(
    username: str,
    include_orgs: bool = Query(True, description="Include READMEs from the user's organizations"),
    github_scraper: GitHubScraper = Depends(get_github_scraper)
):
    """Get all READMEs from a GitHub user's repositories and optionally their organizations"""
    try:
        readmes = github_scraper.get_all_user_readmes(username, include_orgs)
        return {
            "username": username,
            "include_orgs": include_orgs,
            "readmes": readmes,
            "count": len(readmes)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get READMEs: {str(e)}"
        )

@app.get("/api/repositories/{owner}/{repo}/readme", response_model=GitHubReadme, tags=["READMEs"])
async def get_repository_readme(
    owner: str,
    repo: str,
    github_scraper: GitHubScraper = Depends(get_github_scraper)
):
    """Get README from a specific repository"""
    try:
        readme = github_scraper.get_readme(owner, repo)
        if not readme:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"README not found for repository {owner}/{repo}"
            )
        return readme
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get README: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

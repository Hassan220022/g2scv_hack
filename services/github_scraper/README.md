# GitHub README Scraper API

A FastAPI-based API for scraping README files from GitHub users and organizations. This API allows you to fetch all README files from a GitHub user's personal repositories as well as repositories from organizations they belong to.

## Features

- Fetch all repositories for a GitHub user
- Get all organizations a user belongs to (both public and private with proper authentication)
- Get all repositories for an organization
- Fetch README files from repositories
- Get all READMEs from a user's repositories and their organizations
- Handle GitHub API rate limits
- Error handling and resilient API design

## Requirements

- Python 3.7+
- GitHub Personal Access Token with `repo` and `read:org` scopes

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your GitHub token:
   ```
   GITHUB_TOKEN=your_github_personal_access_token_here
   ```

## Usage

1. Start the API server:
   ```bash
   uvicorn main:app --reload
   ```

2. The API will be available at http://localhost:8000

3. API Documentation is available at http://localhost:8000/docs

## API Endpoints

### Health Check
- `GET /`: Check if the API is running

### Repositories
- `GET /api/users/{username}/repositories`: Get all repositories for a GitHub user
- `GET /api/organizations/{org_name}/repositories`: Get all repositories for a GitHub organization

### Organizations
- `GET /api/users/{username}/organizations`: Get all organizations a GitHub user belongs to

### READMEs
- `GET /api/users/{username}/readmes`: Get all READMEs from a user's repositories and optionally their organizations
- `GET /api/repositories/{owner}/{repo}/readme`: Get README from a specific repository

## Authentication

The API requires a GitHub Personal Access Token with the following scopes:
- `repo`: For accessing repositories, including private ones
- `read:org`: For accessing organization information

You can create a token at https://github.com/settings/tokens

## Rate Limits

The GitHub API has rate limits (5,000 requests per hour for authenticated requests). The API includes rate limit handling that will wait if the limit is about to be reached.

## Example Usage

### Request

```
GET /api/users/octocat/readmes?include_orgs=true
```

### Response

```json
{
  "username": "octocat",
  "include_orgs": true,
  "readmes": [
    {
      "repo_name": "Hello-World",
      "repo_full_name": "octocat/Hello-World",
      "repo_description": "My first repository on GitHub!",
      "repo_url": "https://github.com/octocat/Hello-World",
      "content": "# Hello World\n\nThis is a sample README file.",
      "html_url": "https://github.com/octocat/Hello-World/blob/main/README.md",
      "size": 256,
      "encoding": "base64",
      "is_from_org": false,
      "org_name": null
    },
    {
      "repo_name": "test-repo",
      "repo_full_name": "github/test-repo",
      "repo_description": "Test repository",
      "repo_url": "https://github.com/github/test-repo",
      "content": "# Test Repository\n\nThis is a test repository README.",
      "html_url": "https://github.com/github/test-repo/blob/main/README.md",
      "size": 128,
      "encoding": "base64",
      "is_from_org": true,
      "org_name": "github"
    }
  ],
  "count": 2
}
```

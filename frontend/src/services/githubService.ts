import axios from 'axios';
import { API_ENDPOINTS, GITHUB_API_TOKEN } from './apiConfig';

/**
 * GitHub Scraping Service
 * Integrates with the GitHub scraper backend to extract README data and repositories
 */

interface GitHubReadme {
  repo_name: string;
  repo_full_name: string;
  repo_description?: string;
  repo_url: string;
  content: string;
  html_url: string;
  size: number;
  encoding: string;
  is_from_org: boolean;
  org_name?: string;
  topics: string[];
  language?: string;
  stars_count: number;
  forks_count: number;
  updated_at?: string;
}

interface Repository {
  name: string;
  full_name: string;
  description?: string;
  html_url: string;
  url: string;
  is_private: boolean;
}

interface Organization {
  login: string;
  name?: string;
  url: string;
  repos_url: string;
  description?: string;
}

interface GitHubUserData {
  username: string;
  readmes: GitHubReadme[];
  repositories: Repository[];
  organizations: Organization[];
  error?: string;
}

/**
 * Create axios instance with authentication
 */
const githubApiClient = axios.create({
  headers: {
    Authorization: GITHUB_API_TOKEN ? `token ${GITHUB_API_TOKEN}` : undefined,
    Accept: 'application/json',
  }
});

/**
 * Format the endpoint URL by replacing path parameters
 */
function formatEndpoint(endpoint: string, params: Record<string, string>): string {
  let formattedEndpoint = endpoint;
  
  for (const [key, value] of Object.entries(params)) {
    formattedEndpoint = formattedEndpoint.replace(`{${key}}`, value);
  }
  
  return formattedEndpoint;
}

/**
 * Fetch all README files for a GitHub user
 */
async function fetchUserReadmes(username: string, includeOrgs: boolean = true): Promise<GitHubReadme[]> {
  try {
    const endpoint = formatEndpoint(API_ENDPOINTS.github.userReadmes, { username });
    const response = await githubApiClient.get(endpoint, {
      params: { include_orgs: includeOrgs }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error fetching GitHub READMEs:', error);
    throw error;
  }
}

/**
 * Fetch repositories for a GitHub user
 */
async function fetchUserRepositories(username: string): Promise<any> {
  try {
    const endpoint = formatEndpoint(API_ENDPOINTS.github.repositories, { username });
    const response = await githubApiClient.get(endpoint);
    
    return response.data;
  } catch (error) {
    console.error('Error fetching GitHub repositories:', error);
    throw error;
  }
}

/**
 * Fetch organizations for a GitHub user
 */
async function fetchUserOrganizations(username: string): Promise<any> {
  try {
    const endpoint = formatEndpoint(API_ENDPOINTS.github.organizations, { username });
    const response = await githubApiClient.get(endpoint);
    
    return response.data;
  } catch (error) {
    console.error('Error fetching GitHub organizations:', error);
    throw error;
  }
}

/**
 * Main function to scrape GitHub data for a user
 */
export async function scrapeGitHubData(username: string): Promise<any> {
  try {
    // Run all requests in parallel for efficiency
    const [readmes, repositories, organizations] = await Promise.all([
      fetchUserReadmes(username),
      fetchUserRepositories(username),
      fetchUserOrganizations(username)
    ]);

    return {
      username,
      readmes,
      repositories,
      organizations
    };
  } catch (error) {
    console.error('Error scraping GitHub data:', error);
    return {
      username,
      readmes: [],
      repositories: [],
      organizations: [],
      error: error instanceof Error ? error.message : 'Unknown error occurred'
    };
  }
}

/**
 * Scrapes GitHub repositories and README content for a given username
 * @param username GitHub username
 * @returns Raw GitHub repository data including READMEs
 */
export async function scrapeGitHubProjects(username: string): Promise<any> {
  try {
    // Validate GitHub username format
    if (!username || username.trim() === '') {
      throw new Error('GitHub username is required');
    }

    console.log('Scraping GitHub projects for:', username);
    console.log('GitHub service URL:', GITHUB_SERVICE_URL);
    
    // Call the GitHub scraping backend service
    const response = await axios.get(`${GITHUB_SERVICE_URL}/scrape/github`, {
      params: { username }
    });

    console.log('GitHub API response received');
    
    // Check if we got valid response
    if (!response.data || !Array.isArray(response.data.repositories)) {
      throw new Error('No GitHub repositories found or invalid response format');
    }

    console.log(`Found ${response.data.repositories.length} repositories`);
    
    // Return the raw response data without transformation
    // This will be sent directly to the backend LLM
    return response.data;
  } catch (error) {
    console.error('Error scraping GitHub projects:', error);
    throw error;
  }
}

/**
 * Extract skills and technologies from GitHub READMEs
 */
export function extractSkillsFromReadmes(readmes: GitHubReadme[]): string[] {
  // Common tech keywords to look for in READMEs
  const techKeywords = [
    'javascript', 'typescript', 'python', 'java', 'c#', 'c++', 'ruby', 'php', 'go', 'swift',
    'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'laravel', 
    'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'firebase', 'mongodb', 'mysql', 
    'postgresql', 'redux', 'graphql', 'rest api', 'ci/cd', 'git', 'tensorflow', 'pytorch',
    'machine learning', 'data science', 'blockchain', 'devops', 'microservices'
  ];

  const foundSkills = new Set<string>();
  
  for (const readme of readmes) {
    const content = readme.content.toLowerCase();
    const repoName = readme.repo_name.toLowerCase();
    
    // Add repository language if available
    if (readme.language) {
      foundSkills.add(readme.language);
    }
    
    // Add topics/tags
    for (const topic of readme.topics) {
      foundSkills.add(topic);
    }
    
    // Look for tech keywords in content
    for (const keyword of techKeywords) {
      if (content.includes(keyword) || repoName.includes(keyword)) {
        foundSkills.add(keyword);
      }
    }
  }
  
  return Array.from(foundSkills);
}

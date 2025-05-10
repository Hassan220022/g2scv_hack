/**
 * API Configuration
 * 
 * Centralized configuration for API endpoints used in the application.
 * These can be easily changed for different environments.
 */

// Base URLs for different services
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const OCR_SERVICE_URL = import.meta.env.VITE_OCR_SERVICE_URL || 'http://localhost:8000';
export const GITHUB_SERVICE_URL = import.meta.env.VITE_GITHUB_SERVICE_URL || 'http://localhost:8000';

// API tokens
export const APIFY_API_TOKEN = import.meta.env.VITE_APIFY_API_TOKEN || 'apify_api_we5mJBL0T4QXw0c6PmaYSTVifa9KLU3SLTEX';
export const GITHUB_API_TOKEN = import.meta.env.VITE_GITHUB_API_TOKEN || '';

// Service-specific endpoints
export const API_ENDPOINTS = {
  // LinkedIn service (using direct Apify integration)
  linkedIn: {
    scrape: `${API_BASE_URL}/api/linkedin/scrape`,
    confirm: `${API_BASE_URL}/api/linkedin/confirm-receipt`,
  },
  
  // GitHub service (direct integration with our backend)
  github: {
    userReadmes: `${GITHUB_SERVICE_URL}/api/users/{username}/readmes`,
    repositories: `${GITHUB_SERVICE_URL}/api/users/{username}/repositories`,
    organizations: `${GITHUB_SERVICE_URL}/api/users/{username}/organizations`,
    repositoryReadme: `${GITHUB_SERVICE_URL}/api/repositories/{owner}/{repo}/readme`,
  },
  
  // CV parsing service (using OCR backend)
  cv: {
    parse: `${OCR_SERVICE_URL}/parse`,
  },
  
  // Resume generation service
  resume: {
    generate: `${API_BASE_URL}/api/resume/generate`,
  },
};

// Direct Apify actor IDs
export const APIFY_ACTORS = {
  linkedIn: '2SyF0bVxmgGr8IVCZ', // LinkedIn scraper actor ID
}; 
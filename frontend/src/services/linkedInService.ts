import { ApifyClient } from 'apify-client';
import { APIFY_API_TOKEN, APIFY_ACTORS } from './apiConfig';

/**
 * LinkedIn Profile Scraping Service
 * Uses Apify to scrape LinkedIn profiles and returns raw JSON data
 */

/**
 * Scrapes a LinkedIn profile using Apify
 * @param profileUrl LinkedIn profile URL
 * @returns Raw LinkedIn profile data from Apify
 */
export async function scrapeLinkedInProfile(profileUrl: string): Promise<any> {
  try {
    // Validate LinkedIn URL format
    if (!profileUrl.includes('linkedin.com/in/')) {
      throw new Error('Invalid LinkedIn URL format. URL must contain "linkedin.com/in/"');
    }

    console.log('Initializing Apify client with token:', APIFY_API_TOKEN ? 'Token provided' : 'No token');
    
    // Initialize the Apify client
    const apifyClient = new ApifyClient({
      token: APIFY_API_TOKEN,
    });

    // Prepare input for the LinkedIn scraper actor
    const input = {
      profileUrls: [profileUrl]
    };

    console.log('Calling LinkedIn scraper with URL:', profileUrl);
    
    // Run the actor and wait for it to finish
    console.log('Using Apify actor ID:', APIFY_ACTORS.linkedIn);
    const run = await apifyClient.actor(APIFY_ACTORS.linkedIn).call(input);
    
    console.log('Apify run completed, dataset ID:', run.defaultDatasetId);
    
    // Fetch results from the dataset
    const { items } = await apifyClient.dataset(run.defaultDatasetId).listItems();
    
    // Check if we got any results
    if (items.length === 0) {
      throw new Error('LinkedIn profile not found or failed to scrape');
    }

    console.log('Successfully retrieved LinkedIn profile data');
    
    // Return the raw profile data without transforming it
    // This will be sent directly to the backend LLM
    return items[0];
  } catch (error) {
    console.error('Error scraping LinkedIn profile:', error);
    throw error;
  }
}

# LinkedIn Scraper API

A FastAPI-based service for scraping LinkedIn profiles using Apify and storing the raw data in a designated bucket directory.

## Features

- Scrape LinkedIn profiles using Apify's advanced scraping actor
- Save raw profile data as JSON files to a bucket directory
- Simple API with a single endpoint for profile scraping
- FastAPI server with CORS support

## Prerequisites

- Python 3.8+
- Apify API token (set in `.env` file)
- Properly configured `.env` file with required credentials

## Setup

1. Make sure you have the following environment variables in your `.env` file:

```
APIFY_WEB_API_KEY=your_apify_api_key
APIFY_ACTOR_ID=2SyF0bVxmgGr8IVCZ
```

2. Install the required dependencies:

```bash
pip install fastapi uvicorn apify-client python-dotenv
```

3. Start the FastAPI server:

```bash
cd services/linkedin_scraper
python -m uvicorn linkedin_api:app --reload --host 0.0.0.0 --port 8004
```

## API Usage

The API provides a single endpoint for scraping LinkedIn profiles:

### POST /scrape-linkedin

Scrapes a LinkedIn profile and saves the raw data to the bucket directory.

**Request Body:**

```json
{
  "url": "https://www.linkedin.com/in/profile-identifier"
}
```

**Response:**

```json
{
  "success": true,
  "message": "LinkedIn data saved successfully",
  "run_id": "apify_run_id",
  "dataset_id": "apify_dataset_id",
  "saved_to": "/path/to/bucket/linkedin_profile_identifier_timestamp.json",
  "item_count": 1
}
```

## Example Usage

### Using Python Requests

```python
import requests

# API endpoint
api_url = "http://localhost:8004/scrape-linkedin"

# LinkedIn profile URL to scrape
profile_url = "https://www.linkedin.com/in/williamhgates"

# Request payload
payload = {
    "url": profile_url
}

# Make the API request
response = requests.post(api_url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    print(f"Profile data saved to: {result.get('saved_to')}")
else:
    print(f"Error: {response.text}")
```

### Using cURL

```bash
curl -X 'POST' \
  'http://localhost:8004/scrape-linkedin' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://www.linkedin.com/in/williamhgates"
  }'
```

## Testing the API

The repository includes a test script (`test_scraper.py`) to verify API functionality:

```bash
python test_scraper.py
```

## Data Format

The raw LinkedIn profile data is saved as a JSON file with the following format:

```json
[
  {
    "linkedinUrl": "https://www.linkedin.com/in/profile-id",
    "firstName": "First",
    "lastName": "Last",
    "fullName": "First Last",
    "headline": "Professional Headline",
    "connections": 500,
    "followers": 1000,
    "email": "example@company.com",
    "jobTitle": "Job Title",
    "companyName": "Company Name",
    "experiences": [...],
    "educations": [...],
    "skills": [...],
    ...
  }
]
```

## Important Notes

- The API uses Apify's LinkedIn scraper actor which has usage limits based on your Apify account
- Scraped profile data is stored in the bucket directory at: `/Users/mikawi/Developer/hackathon/g2scv_n/bucket/`
- Each profile is saved with a unique filename format: `linkedin_profile_{profile_id}_{timestamp}.json`
- Make sure your Apify API token is valid and has sufficient credits
- Respect LinkedIn's terms of service when using this scraper

## License

MIT

# LinkedIn Profile Scraper API (with Apify Integration)

This project provides a FastAPI-based backend to scrape LinkedIn public profiles using the Apify platform, and to serve the data to a client (such as a Flutter app) in a structured JSON format. Data is deleted from Apify storage only after you confirm it has been saved locally.

## Features
- **Scrape LinkedIn profiles** using Apify's LinkedIn Actor
- **Two-step data handling**: data is deleted from Apify only after the client confirms receipt
- **Flutter/mobile-ready** JSON response
- **CORS enabled** for easy integration with web and mobile apps
- **Secure**: API keys are stored in `.env` and not committed to version control

## API Endpoints

### 1. Scrape LinkedIn Profile
`POST /scrape-linkedin`

Request body:
```json
{
  "url": "https://www.linkedin.com/in/mikawi/"
}
```

Response:
```json
{
  "data": [ ...profileData... ],
  "run_id": "...",
  "dataset_id": "..."
}
```

### 2. Confirm Data Receipt & Delete from Apify
`POST /confirm-data-receipt`

Request body:
```json
{
  "run_id": "...",
  "dataset_id": "..."
}
```

Response:
```json
{
  "message": "Data successfully deleted from Apify"
}
```

## Quickstart

1. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
2. **Set your Apify API key** in `.env`:
   ```env
   APIFY_WEB_API_KEY=your_apify_token_here
   ```
3. **Run the API**
   ```sh
   uvicorn linkedin_api:app --reload --port 8004
   ```
4. **Use the API** from your Flutter/mobile/web app as described above.

## Notes
- The API will only delete Apify data after you explicitly confirm receipt.
- You can view your Apify runs and datasets here (for debugging):
  <!-- supreme_coder/linkedin-profile-scraper -->

## Security
- **Never commit your `.env` file or API keys to version control.**
- The `.gitignore` is set up to ignore `.env` and other sensitive files.

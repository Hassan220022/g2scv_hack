import os
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables from .env file
load_dotenv()

# Get API token from environment variable
api_token = os.getenv("APIFY_WEB_API_KEY")

# Initialize the ApifyClient with your API token
client = ApifyClient(api_token)

# Prepare the Actor input
run_input = {
        "profileUrls": ["https://www.linkedin.com/in/mikawi/"]
}

# Run the Actor and wait for it to finish
print("Starting LinkedIn profile scraping with Apify...")
print(f"Using API token: {api_token[:10]}...{api_token[-4:]}")  # Show partial token for verification
run = client.actor("yZnhB5JewWf9xSmoM").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
print(f"Scraping complete. Dataset ID: {run['defaultDatasetId']}")
print("Results:")

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    # Pretty print the profiles with some basic info
    print(f"\n{'=' * 50}")
    print(f"Profile: {item.get('profile', {}).get('displayName', 'Unknown')}")
    print(f"Headline: {item.get('profile', {}).get('headline', 'N/A')}")
    print(f"Location: {item.get('profile', {}).get('locationName', 'N/A')}")
    print(f"Company: {item.get('profile', {}).get('companyName', 'N/A')}")
    print(f"{'=' * 50}\n")

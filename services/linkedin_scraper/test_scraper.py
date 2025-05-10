import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the API endpoint (assuming the FastAPI server is running locally)
API_URL = "http://localhost:8004/scrape-linkedin"

def test_linkedin_scraping():
    """Test scraping a LinkedIn profile and saving raw data to the bucket"""
    
    # LinkedIn profile URL to scrape
    profile_url = "https://www.linkedin.com/in/mikawi"
    
    # Request payload
    payload = {
        "url": profile_url
    }
    
    try:
        # Make the API request
        print(f"Sending request to scrape LinkedIn profile: {profile_url}")
        response = requests.post(API_URL, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            print(f"\nScraping Result:")
            print(f"  Status: {result.get('success')}")
            print(f"  Message: {result.get('message')}")
            print(f"  Items Retrieved: {result.get('item_count')}")
            print(f"  Data saved to: {result.get('saved_to')}")
            print(f"  Run ID: {result.get('run_id')}")
            print(f"  Dataset ID: {result.get('dataset_id')}")
            
            # Check if the file was actually created
            file_path = result.get('saved_to')
            if file_path and os.path.exists(file_path):
                file_size = os.path.getsize(file_path) / 1024  # Size in KB
                print(f"\nFile verified: {os.path.basename(file_path)} ({file_size:.1f} KB)")
                
                # Show file content preview
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        print("\nFile contains valid LinkedIn profile data:")
                        profile = data[0]
                        print(f"  Name: {profile.get('fullName', 'N/A')}")
                        print(f"  Headline: {profile.get('headline', 'N/A')}")
                        print(f"  Location: {profile.get('addressWithCountry', 'N/A')}")
                        print(f"  Company: {profile.get('companyName', 'N/A')}")
                        print(f"  # of Experiences: {len(profile.get('experiences', []))}")
                        print(f"  # of Updates: {len(profile.get('updates', []))}")
                        print(f"  # of Skills: {len(profile.get('skills', []))}")
                    else:
                        print("\nWarning: File doesn't contain the expected LinkedIn profile data structure")
            else:
                print(f"\nWarning: File {file_path} does not exist!")
                
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_linkedin_scraping()

import os
import json
import datetime
import uuid
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables
load_dotenv()

# Get API token
APIFY_API_KEY = os.getenv("APIFY_WEB_API_KEY")
if not APIFY_API_KEY:
    raise ValueError("APIFY_WEB_API_KEY environment variable is not set")

# Set Apify Actor ID
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID")
if not APIFY_ACTOR_ID:
    raise ValueError("APIFY_ACTOR_ID environment variable is not set")

# Set bucket directory path
BUCKET_DIR = "/Users/mikawi/Developer/hackathon/g2scv_n/bucket"
# Create bucket directory if it doesn't exist
os.makedirs(BUCKET_DIR, exist_ok=True)

# Initialize the ApifyClient
apify_client = ApifyClient(APIFY_API_KEY)

# Create FastAPI app
app = FastAPI(
    title="LinkedIn Profile API",
    description="API to fetch LinkedIn profile data and delete it from Apify storage after use",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LinkedInURLRequest(BaseModel):
    url: str = Field(..., description="LinkedIn profile URL")

class DeleteApifyDataRequest(BaseModel):
    run_id: str = Field(..., description="Apify run ID to delete")
    dataset_id: str = Field(..., description="Apify dataset ID to delete")

class LinkedInProfileResponse(BaseModel):
    id: Optional[str] = None
    profileId: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    occupation: Optional[str] = None
    publicIdentifier: Optional[str] = None
    trackingId: Optional[str] = None
    pictureUrl: Optional[str] = None
    coverImageUrl: Optional[str] = None
    countryCode: Optional[str] = None
    geoUrn: Optional[str] = None
    positions: Optional[List[Dict[str, Any]]] = []
    educations: Optional[List[Dict[str, Any]]] = []
    certifications: Optional[List[Dict[str, Any]]] = []
    courses: Optional[List[Dict[str, Any]]] = []
    honors: Optional[List[Dict[str, Any]]] = []
    languages: Optional[List[str]] = []
    skills: Optional[List[str]] = []
    volunteerExperiences: Optional[List[Dict[str, Any]]] = []
    headline: Optional[str] = None
    summary: Optional[str] = None
    student: Optional[bool] = False
    industryName: Optional[str] = None
    industryUrn: Optional[str] = None
    geoLocationName: Optional[str] = None
    geoCountryName: Optional[str] = None
    jobTitle: Optional[str] = None
    companyName: Optional[str] = None
    companyPublicId: Optional[str] = None
    companyLinkedinUrl: Optional[str] = None
    following: Optional[bool] = None
    followable: Optional[bool] = None
    followersCount: Optional[int] = None
    connectionsCount: Optional[int] = None
    connectionType: Optional[str] = None
    inputUrl: Optional[str] = None

class ScrapingResponse(BaseModel):
    data: List[LinkedInProfileResponse]
    run_id: str
    dataset_id: str

def delete_apify_data(run_id: str, dataset_id: str):
    """Delete data from Apify"""
    try:
        # First delete the dataset
        dataset_client = apify_client.dataset(dataset_id)
        dataset_client.delete()
        print(f"Successfully deleted dataset: {dataset_id}")
        
        # Then delete the run
        run_client = apify_client.run(run_id)
        run_client.delete()
        print(f"Successfully deleted run: {run_id}")
        return True
    except Exception as e:
        print(f"Error deleting Apify data: {str(e)}")
        return False

@app.post("/scrape-linkedin", response_model=dict)
async def scrape_linkedin_profile(request: LinkedInURLRequest):
    """
    Scrape a LinkedIn profile and save raw data directly to the bucket
    """
    try:
        # Prepare Actor input
        run_input = {
            "profileUrls": [request.url]
        }
        
        # Run the LinkedIn scraper Actor
        print(f"Starting LinkedIn profile scraping for URL: {request.url}")
        run = apify_client.actor(APIFY_ACTOR_ID).call(run_input=run_input)
        
        if not run or "defaultDatasetId" not in run:
            raise HTTPException(status_code=500, detail="Failed to get results from LinkedIn scraper")
        
        # Fetch data from the Actor's dataset
        dataset_id = run["defaultDatasetId"]
        run_id = run["id"]
        
        print(f"Scraping complete. Fetching data from dataset: {dataset_id}")
        
        # Get all raw items from the dataset
        raw_data = []
        for item in apify_client.dataset(dataset_id).iterate_items():
            raw_data.append(item)
        
        # If no items were found, return an error
        if not raw_data:
            raise HTTPException(status_code=404, detail="No LinkedIn profile data found for the provided URL")
        
        # Extract profile identifier from the URL
        profile_id = request.url.split("/")[-1].split("?")[0]
        
        # Generate a unique filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"linkedin_profile_{profile_id}_{timestamp}.json"
        file_path = os.path.join(BUCKET_DIR, filename)
        
        # Save raw LinkedIn data exactly as received - no parsing
        # The example data shows the expected format is a direct JSON array
        
        # Save raw data to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)
            
        print(f"LinkedIn profile data saved to {file_path}")
            
        # Return basic info about the saved data
        return {
            "success": True,
            "message": "LinkedIn data saved successfully",
            "run_id": run_id,
            "dataset_id": dataset_id,
            "saved_to": file_path,
            "item_count": len(raw_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping LinkedIn profile: {str(e)}")

@app.post("/confirm-data-receipt")
async def confirm_data_receipt(request: DeleteApifyDataRequest):
    """
    Confirm that data has been received and saved locally, then delete it from Apify
    
    This endpoint should be called after the client has successfully saved the data
    """
    try:
        success = delete_apify_data(request.run_id, request.dataset_id)
        if success:
            return {"message": "Data successfully deleted from Apify"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete data from Apify")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error confirming data receipt: {str(e)}")

@app.get("/")
async def root():
    return {"message": "LinkedIn API is running. Use /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("linkedin_api:app", host="0.0.0.0", port=8004, reload=True)

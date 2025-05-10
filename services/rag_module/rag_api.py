# rag_api.py

import os
import json
import glob
import math
import numpy as np
from typing import Dict, Any, List, Optional, Union, Tuple
from fastapi import FastAPI, HTTPException, Body, Query
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import openai
import re
from pathlib import Path

# Load environment variables (especially OPENAI_API_KEY)
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize OpenAI client (ensure you have the 'openai' library installed: pip install openai)
# Make sure you are using openai >= 1.0
# If not, update your client initialization code. For example:
# client = openai.OpenAI(api_key=OPENAI_API_KEY)

# For openai < 1.0.0
# openai.api_key = OPENAI_API_KEY
# For openai >= 1.0.0
client = openai.OpenAI(api_key=OPENAI_API_KEY)


app = FastAPI(
    title="RAG CV Generation API",
    description="API to generate LaTeX CVs from LinkedIn, GitHub, and OCR data using an LLM and search GitHub READMEs.",
    version="1.0.0"
)

# --- Pydantic Models ---
class RAGRequest(BaseModel):
    linkedin_data: Dict[str, Any] = Field(..., description="Parsed JSON data from LinkedIn.")
    github_data: Dict[str, Any] = Field(..., description="Parsed JSON data from GitHub.")
    cv_ocr_data: Dict[str, Any] = Field(..., description="Parsed JSON data from CV OCR.")
    cv_template_style: Optional[str] = Field("default", description="Identifier for the CV LaTeX template/style to use.")
    # You could add more parameters here, e.g., custom instructions, target role for the CV

class RAGResponse(BaseModel):
    latex_cv: str = Field(..., description="The generated CV in LaTeX format.")
    model_used: str = Field(..., description="The LLM model used for generation.")
    usage_stats: Optional[Dict[str, Any]] = Field(None, description="Token usage statistics from the LLM API.")

class RepoReadmeQueryRequest(BaseModel):
    query: str = Field(..., description="Query to search for in repository READMEs.")
    top_k: int = Field(3, description="Number of top results to return.")
    
class RepoReadmeResponse(BaseModel):
    repo_name: str = Field(..., description="Full repository name including owner.")
    repo_info: Dict[str, Any] = Field(..., description="Repository metadata.")
    readme_content: str = Field(..., description="README content of the repository.")
    similarity_score: float = Field(..., description="Similarity score of the query to the README content.")

# --- Helper Functions ---

def load_json_from_path(file_path: str) -> Dict[str, Any]:
    """Loads JSON data from a given file path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format in file: {file_path}")
        
def get_bucket_path() -> str:
    """Get the path to the bucket directory."""
    # Assuming the bucket directory is at the project root
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'bucket')

def find_latest_file(pattern: str) -> Optional[str]:
    """Find the latest file matching a pattern in the bucket directory."""
    bucket_dir = get_bucket_path()
    files = glob.glob(os.path.join(bucket_dir, pattern))
    
    # Also check in subdirectories (one level deep)
    for subdir in [d for d in os.listdir(bucket_dir) if os.path.isdir(os.path.join(bucket_dir, d))]:
        subdir_path = os.path.join(bucket_dir, subdir)
        files.extend(glob.glob(os.path.join(subdir_path, pattern)))
    
    if not files:
        return None
    
    # Return the most recently modified file
    return max(files, key=os.path.getmtime)

def load_latest_cv_ocr_data() -> Dict[str, Any]:
    """Load the latest CV OCR data from the bucket."""
    file_path = find_latest_file('cv_*_parsed.json')
    if not file_path:
        # Try alternative pattern
        file_path = find_latest_file('*_parsed.json')
    
    if not file_path:
        raise HTTPException(status_code=404, detail="No CV OCR data found")
    
    return load_json_from_path(file_path)

def load_latest_linkedin_data() -> Dict[str, Any]:
    """Load the latest LinkedIn data from the bucket."""
    file_path = find_latest_file('linkedin_*.json')
    if not file_path:
        raise HTTPException(status_code=404, detail="No LinkedIn data found")
    
    return load_json_from_path(file_path)

def load_github_data(username: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """Load GitHub data for a specific user or all available GitHub data."""
    if username:
        file_path = find_latest_file(f'github_data_{username}.json')
        if not file_path:
            raise HTTPException(status_code=404, detail=f"No GitHub data found for user: {username}")
    else:
        file_path = find_latest_file('github_data_*.json')
        if not file_path:
            raise HTTPException(status_code=404, detail="No GitHub data found")
    
    return load_json_from_path(file_path)

def generate_embeddings(text: str) -> List[float]:
    """Generate embeddings for text using OpenAI's embedding API."""
    try:
        # Truncate text to avoid token limit issues
        max_tokens = 8000  # Text embedding API has a limit
        truncated_text = text[:max_tokens * 4]  # Approximate character count
        
        response = client.embeddings.create(
            input=truncated_text,
            model="text-embedding-ada-002"  # Using Ada embedding model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")

def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    # Convert to numpy arrays for efficient calculation
    a = np.array(vec1)
    b = np.array(vec2)
    
    # Calculate cosine similarity
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    similarity = dot_product / (norm_a * norm_b)
    return float(similarity)  # Convert from numpy float to Python float
        
def get_bucket_path() -> str:
    """Get the path to the bucket directory."""
    # Assuming the bucket directory is at the project root
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'bucket')

def find_latest_file(pattern: str) -> Optional[str]:
    """Find the latest file matching a pattern in the bucket directory."""
    bucket_dir = get_bucket_path()
    files = glob.glob(os.path.join(bucket_dir, pattern))
    
    # Also check in subdirectories (one level deep)
    for subdir in [d for d in os.listdir(bucket_dir) if os.path.isdir(os.path.join(bucket_dir, d))]:
        subdir_path = os.path.join(bucket_dir, subdir)
        files.extend(glob.glob(os.path.join(subdir_path, pattern)))
    
    if not files:
        return None
    
    # Return the most recently modified file
    return max(files, key=os.path.getmtime)

def load_latest_cv_ocr_data() -> Dict[str, Any]:
    """Load the latest CV OCR data from the bucket."""
    file_path = find_latest_file('cv_*_parsed.json')
    if not file_path:
        # Try alternative pattern
        file_path = find_latest_file('*_parsed.json')
    
    if not file_path:
        raise HTTPException(status_code=404, detail="No CV OCR data found")
    
    return load_json_from_path(file_path)

def load_latest_linkedin_data() -> Dict[str, Any]:
    """Load the latest LinkedIn data from the bucket."""
    file_path = find_latest_file('linkedin_*.json')
    if not file_path:
        raise HTTPException(status_code=404, detail="No LinkedIn data found")
    
    return load_json_from_path(file_path)

def load_github_data(username: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """Load GitHub data for a specific user or all available GitHub data."""
    if username:
        file_path = find_latest_file(f'github_data_{username}.json')
        if not file_path:
            raise HTTPException(status_code=404, detail=f"No GitHub data found for user: {username}")
    else:
        file_path = find_latest_file('github_data_*.json')
        if not file_path:
            raise HTTPException(status_code=404, detail="No GitHub data found")
    
    return load_json_from_path(file_path)


def search_github_readmes(query: str, github_data: Dict[str, Dict[str, Any]], top_k: int = 3) -> List[RepoReadmeResponse]:
    """Search GitHub repository READMEs based on a query using embeddings and semantic similarity."""
    # Generate embedding for the query
    query_embedding = generate_embeddings(query)
    
    # Calculate similarity scores for each repository README
    results = []
    for repo_name, repo_info in github_data.items():
        readme_content = repo_info.get('readme', '')
        if not readme_content or len(readme_content.strip()) < 10:  # Skip empty or very short READMEs
            continue
        
        # Generate embedding for the README content
        try:
            readme_embedding = generate_embeddings(readme_content)
            similarity_score = calculate_cosine_similarity(query_embedding, readme_embedding)
            
            results.append(RepoReadmeResponse(
                repo_name=repo_name,
                repo_info={
                    'name': repo_info.get('name', ''),
                    'description': repo_info.get('description', ''),
                    'languages': repo_info.get('languages', []),
                    'stars': repo_info.get('stars', 0),
                    'forks': repo_info.get('forks', 0),
                    'last_updated': repo_info.get('last_updated', '')
                },
                readme_content=readme_content,
                similarity_score=similarity_score
            ))
        except Exception as e:
            print(f"Error processing {repo_name}: {str(e)}")
            continue
    
    # Sort by similarity score (descending) and return top_k results
    results.sort(key=lambda x: x.similarity_score, reverse=True)
    return results[:top_k]


def consolidate_and_prepare_data(
    linkedin_data: Dict[str, Any],
    github_data: Dict[str, Any],
    cv_ocr_data: Dict[str, Any]
) -> str:
    """
    Consolidates data from all sources and prepares a text representation for the LLM.
    Per user requirement: Pass LinkedIn and CV OCR data directly to the model without parsing.
    Only parse GitHub data for better processing.
    """
    # Start with raw LinkedIn data
    prepared_text = "=== LinkedIn Data (RAW) ===\n\n"
    prepared_text += json.dumps(linkedin_data, indent=2) + "\n\n"
    
    # Add raw CV OCR data
    prepared_text += "=== CV OCR Data (RAW) ===\n\n"
    prepared_text += json.dumps(cv_ocr_data, indent=2) + "\n\n"
    
    # Process only GitHub data for better readability
    prepared_text += "=== GitHub Projects ===\n\n"
    if github_data:
        for repo_full_name, repo_info in github_data.items():
            prepared_text += f"Project: {repo_info.get('name', repo_full_name)}\n"
            prepared_text += f"Description: {repo_info.get('description', 'N/A')}\n"
            prepared_text += f"Languages: {', '.join(repo_info.get('languages', []))}\n"
            prepared_text += f"Stars: {repo_info.get('stars', 0)}, Forks: {repo_info.get('forks', 0)}\n"
            if repo_info.get("readme"):
                 # Truncate README to avoid excessive tokens
                 prepared_text += f"README Snippet: {repo_info.get('readme', '')[:200]}...\n"
            prepared_text += "\n"

    return prepared_text.strip()


def construct_llm_prompt(
    prepared_data_str: str,
    cv_template_style: str = "default"
) -> str:
    """
    Constructs the prompt for the LLM to generate the LaTeX CV.
    """
    # Load the prompt template from external file
    prompt_template_path = os.path.join(os.path.dirname(__file__), 'cv_prompt_template.txt')
    
    # Load LaTeX template example
    latex_template_path = os.path.join(os.path.dirname(__file__), 'cv_temp.tex')
    
    try:
        # Read the prompt template
        with open(prompt_template_path, 'r') as f:
            prompt_template = f.read()
        
        # Read the LaTeX example
        with open(latex_template_path, 'r') as f:
            latex_example = f.read()
        
        # Format the prompt with the candidate data and the LaTeX example
        prompt = prompt_template.format(candidate_info=prepared_data_str)
        prompt += f"\n\n**LaTeX Template Example:**\n```latex\n{latex_example}\n```"
        
    except Exception as e:
        # Fallback if template files are not found
        print(f"Error loading templates: {str(e)}")
        prompt = f"""
You are an expert CV writer and LaTeX formatting assistant that creates ATS approved CVs.
Your task is to generate a professional and well-structured CV in LaTeX format based on the provided candidate information.

**Candidate Information:**
{prepared_data_str}

**Instructions for LaTeX CV Generation:**
1. Use a standard LaTeX article class with professional formatting.
2. The CV must include contact information, professional summary, work experience, education, skills, and projects.
3. Format the CV clearly and professionally with appropriate sections and formatting.
4. Return ONLY the LaTeX code, starting with \documentclass and ending with \end{{document}}.
"""
    
    return prompt


# --- API Endpoints ---

@app.post("/generate", response_model=RAGResponse)
async def generate_cv(request: RAGRequest = Body(...)):
    """
    Endpoint to generate a LaTeX CV using the RAG approach.
    Takes LinkedIn, GitHub, and CV OCR data to create a personalized LaTeX CV.
    """
    # Prepare the data for the LLM
    prepared_data = consolidate_and_prepare_data(
        request.linkedin_data,
        request.github_data,
        request.cv_ocr_data
    )
    
    # Create the prompt for the LLM
    prompt = construct_llm_prompt(prepared_data, request.cv_template_style)
    
    # Use OpenAI's API to generate the CV
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[
                {"role": "system", "content": "You are an expert CV writer and LaTeX formatting assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Slightly higher to encourage creativity in CV generation 
            max_tokens=4000   # Set an appropriate max_tokens (depends on OpenAI plan)
        )
        
        # Extract and clean up the response
        # Get the model's reply
        model_response = response.choices[0].message.content
        usage_data = response.usage.model_dump() if hasattr(response, 'usage') else None
        
        # Log the response and usage for debugging
        print(f"Model response received. Tokens used: {usage_data if usage_data else 'N/A'}")
        
        return RAGResponse(
            latex_cv=model_response,
            model_used="gpt-4.1-2025-04-14",
            usage_stats=usage_data
        )
        
    except Exception as e:
        # Log the error
        print(f"Error calling OpenAI API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating CV: {str(e)}")


@app.post("/search/github-readmes", response_model=List[RepoReadmeResponse])
async def search_github_readme(request: RepoReadmeQueryRequest = Body(...)):
    """
    Search GitHub repository READMEs based on a query.
    Returns top_k most relevant repositories with their READMEs.
    """
    try:
        # Load GitHub data
        github_data = load_github_data()
        
        # Search for relevant repositories
        results = search_github_readmes(request.query, github_data, request.top_k)
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching GitHub READMEs: {str(e)}")


@app.get("/data/github", response_model=Dict[str, Any])
async def get_github_data(username: Optional[str] = Query(None, description="GitHub username")):
    """
    Get GitHub data for a specific user or all available GitHub data.
    """
    try:
        return load_github_data(username)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving GitHub data: {str(e)}")


@app.get("/data/linkedin", response_model=Dict[str, Any])
async def get_linkedin_data():
    """
    Get the latest LinkedIn data.
    """
    try:
        return load_latest_linkedin_data()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving LinkedIn data: {str(e)}")


@app.get("/data/cv-ocr", response_model=Dict[str, Any])
async def get_cv_ocr_data():
    """
    Get the latest CV OCR data.
    """
    try:
        return load_latest_cv_ocr_data()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving CV OCR data: {str(e)}")


@app.get("/repo-info/{repo_name}", response_model=Dict[str, Any])
async def get_repo_info(repo_name: str):
    """
    Get information about a specific repository by name.
    The repo_name should be in format 'owner/repo'.
    """
    try:
        # Load GitHub data
        github_data = load_github_data()
        
        # Find the repository
        if repo_name not in github_data:
            raise HTTPException(status_code=404, detail=f"Repository {repo_name} not found")
        
        return github_data[repo_name]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving repository information: {str(e)}")


# Health check endpoint to verify the API is running
@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy"}
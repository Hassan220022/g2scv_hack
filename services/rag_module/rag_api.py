# rag_api.py

import os
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import openai

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
    description="API to generate LaTeX CVs from LinkedIn, GitHub, and OCR data using an LLM.",
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


def consolidate_and_prepare_data(
    linkedin_data: Dict[str, Any],
    github_data: Dict[str, Any],
    cv_ocr_data: Dict[str, Any]
) -> str:
    """
    Consolidates data from all sources and prepares a text representation for the LLM.
    This is a crucial step where you decide how to merge and prioritize information.
    For simplicity, this example will just serialize them, but in a real app,
    you'd intelligently merge fields (e.g., skills, experience).
    """
    prepared_text = "=== Candidate Information ===\n\n"

    # Contact Info (Prioritize CV OCR, then LinkedIn)
    prepared_text += "--- Contact Information ---\n"
    name = cv_ocr_data.get("name") or linkedin_data.get("firstName", "") + " " + linkedin_data.get("lastName", "")
    email = cv_ocr_data.get("email") or linkedin_data.get("emailAddress") # Assuming email is in linkedin_data
    phone = cv_ocr_data.get("phone") or linkedin_data.get("phoneNumber") # Assuming phone is in linkedin_data
    location = cv_ocr_data.get("location") or linkedin_data.get("locationName") or linkedin_data.get("geoLocationName")

    if name.strip(): prepared_text += f"Name: {name.strip()}\n"
    if email: prepared_text += f"Email: {email}\n"
    if phone: prepared_text += f"Phone: {phone}\n"
    if location: prepared_text += f"Location: {location}\n"
    prepared_text += "\n"

    # Summary (LinkedIn summary is often good)
    prepared_text += "--- Professional Summary ---\n"
    summary = linkedin_data.get("summary", cv_ocr_data.get("summary", "No summary provided."))
    prepared_text += f"{summary}\n\n"

    # Experience (Combine from LinkedIn and CV OCR, requires careful merging and deduplication)
    prepared_text += "--- Work Experience ---\n"
    # This is a simplified representation. Real merging would be more complex.
    if linkedin_data.get("positions"):
        for pos in linkedin_data["positions"]:
            prepared_text += f"Title: {pos.get('title', 'N/A')}\n"
            prepared_text += f"Company: {pos.get('companyName', 'N/A')}\n"
            prepared_text += f"Dates: {pos.get('dateRange', {}).get('start', {}).get('text', 'N/A')} - {pos.get('dateRange', {}).get('end', {}).get('text', 'Present')}\n"
            prepared_text += f"Description: {pos.get('description', 'N/A')}\n\n"
    # Add logic to integrate cv_ocr_data['experience'] here, avoiding duplicates

    # Education
    prepared_text += "--- Education ---\n"
    if linkedin_data.get("educations"):
        for edu in linkedin_data["educations"]:
            prepared_text += f"Degree: {edu.get('degreeName', 'N/A')}\n"
            prepared_text += f"School: {edu.get('schoolName', 'N/A')}\n"
            prepared_text += f"Dates: {edu.get('dateRange', {}).get('start', {}).get('text', 'N/A')} - {edu.get('dateRange', {}).get('end', {}).get('text', 'N/A')}\n\n"
    # Add logic to integrate cv_ocr_data['education']

    # Skills (Combine from LinkedIn and CV OCR)
    prepared_text += "--- Skills ---\n"
    skills_list = list(set(linkedin_data.get("skills", []) + cv_ocr_data.get("skills", [])))
    prepared_text += ", ".join(skills_list) + "\n\n"

    # Projects (From GitHub)
    prepared_text += "--- Projects (from GitHub) ---\n"
    if github_data:
        for repo_full_name, repo_info in github_data.items():
            prepared_text += f"Project: {repo_info.get('name', repo_full_name)}\n"
            prepared_text += f"Description: {repo_info.get('description', 'N/A')}\n"
            prepared_text += f"Languages: {', '.join(repo_info.get('languages', []))}\n"
            prepared_text += f"Stars: {repo_info.get('stars', 0)}, Forks: {repo_info.get('forks', 0)}\n"
            if repo_info.get("readme"):
                 prepared_text += f"README Snippet: {repo_info.get('readme', '')[:200]}...\n" # Truncate README
            prepared_text += "\n"

    return prepared_text.strip()


def construct_llm_prompt(
    prepared_data_str: str,
    cv_template_style: str = "default"
) -> str:
    """
    Constructs the prompt for the LLM to generate the LaTeX CV.
    """
    # This is a basic prompt. You'll want to refine this significantly.
    # Consider providing a full LaTeX CV template structure and asking the LLM to fill it.
    # For example, you might use a specific LaTeX class like 'moderncv' or 'AltaCV'.

    prompt = f"""
You are an expert CV writer and LaTeX formatting assistant that create ATS approved CVs.
Your task is to generate a professional and well-structured CV in LaTeX format based on the provided candidate information.
You must check the candidate information provided against the job description and requirements and ***IF HE IS NOT FIT FOR THE ROLE*** return the message 'You are not fit for this role."

**Candidate Information:**
{prepared_data_str}

**Instructions for LaTeX CV Generation:**
1.  Use a standard LaTeX article class or a common CV class (e.g., `article` with custom sections, or conceptually similar to `moderncv` or `res.cls`).
2.  The CV must include the following sections if information is available:
    * Contact Information (Name, Email, Phone, Location) - Display this prominently at the top.
    * Professional Summary
    * Work Experience (For each role: Title, Company, Dates, Key Responsibilities/Achievements)
    * Education (For each degree: Degree Name, School, Dates)
    * Skills (A list or categorized list of skills)
    * Projects (If available, from GitHub: Project Name, Description, Technologies Used, Link if possible - though links are not in the provided data)
3.  Format the CV clearly and professionally. Use appropriate LaTeX commands for sections, itemization, bolding key information, etc.
4.  Ensure the output is ONLY the LaTeX code, starting with `\\documentclass` and ending with `\\end{{document}}`. Do not include any explanations or conversational text before or after the LaTeX code.
5.  If certain information is missing for a standard section, omit the section or indicate 'N/A' gracefully if appropriate within the context of a CV.
6.  For Work Experience and Education, list items in reverse chronological order (most recent first). (The LLM should infer this, but explicit instruction helps).
7.  Pay attention to LaTeX special characters (e.g., %, &, _, #, {{, }}) and escape them properly if they appear in the input data and need to be rendered as text. For example, use `\\%` for percent, `\\&` for ampersand, `\\_` for underscore.
8. 


**LaTeX Output:**
```latex
[Your LaTeX code here]"""
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


**LaTeX Output Example:**
```latex
\documentclass[10pt, letterpaper]{article}

% Packages:
\usepackage[
    ignoreheadfoot, % set margins without considering header and footer
    top=2 cm, % seperation between body and page edge from the top
    bottom=2 cm, % seperation between body and page edge from the bottom
    left=2 cm, % seperation between body and page edge from the left
    right=2 cm, % seperation between body and page edge from the right
    footskip=1.0 cm, % seperation between body and footer
    % showframe % for debugging 
]{geometry} % for adjusting page geometry
\usepackage{titlesec} % for customizing section titles
\usepackage{tabularx} % for making tables with fixed width columns
\usepackage{array} % tabularx requires this
\usepackage[dvipsnames]{xcolor} % for coloring text
\definecolor{primaryColor}{RGB}{0, 0, 0} % define primary color
\usepackage{enumitem} % for customizing lists
\usepackage{fontawesome5} % for using icons
\usepackage{amsmath} % for math
\usepackage[
    pdftitle={John Doe's CV},
    pdfauthor={John Doe},
    pdfcreator={LaTeX with RenderCV},
    colorlinks=true,
    urlcolor=primaryColor
]{hyperref} % for links, metadata and bookmarks
\usepackage[pscoord]{eso-pic} % for floating text on the page
\usepackage{calc} % for calculating lengths
\usepackage{bookmark} % for bookmarks
\usepackage{lastpage} % for getting the total number of pages
\usepackage{changepage} % for one column entries (adjustwidth environment)
\usepackage{paracol} % for two and three column entries
\usepackage{ifthen} % for conditional statements
\usepackage{needspace} % for avoiding page brake right after the section title
\usepackage{iftex} % check if engine is pdflatex, xetex or luatex

% Ensure that generate pdf is machine readable/ATS parsable:
\ifPDFTeX
    \input{glyphtounicode}
    \pdfgentounicode=1
    \usepackage[T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage{lmodern}
\fi

\usepackage{charter}

% Some settings:
\raggedright
\AtBeginEnvironment{adjustwidth}{\partopsep0pt} % remove space before adjustwidth environment
\pagestyle{empty} % no header or footer
\setcounter{secnumdepth}{0} % no section numbering
\setlength{\parindent}{0pt} % no indentation
\setlength{\topskip}{0pt} % no top skip
\setlength{\columnsep}{0.15cm} % set column seperation
\pagenumbering{gobble} % no page numbering

\titleformat{\section}{\needspace{4\baselineskip}\bfseries\large}{}{0pt}{}[\vspace{1pt}\titlerule]

\titlespacing{\section}{
    % left space:
    -1pt
}{
    % top space:
    0.3 cm
}{
    % bottom space:
    0.2 cm
} % section title spacing

\renewcommand\labelitemi{$\vcenter{\hbox{\small$\bullet$}}$} % custom bullet points
\newenvironment{highlights}{
    \begin{itemize}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=0 cm + 10pt
    ]
}{
    \end{itemize}
} % new environment for highlights


\newenvironment{highlightsforbulletentries}{
    \begin{itemize}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=10pt
    ]
}{
    \end{itemize}
} % new environment for highlights for bullet entries

\newenvironment{onecolentry}{
    \begin{adjustwidth}{
        0 cm + 0.00001 cm
    }{
        0 cm + 0.00001 cm
    }
}{
    \end{adjustwidth}
} % new environment for one column entries

\newenvironment{twocolentry}[2][]{
    \onecolentry
    \def\secondColumn{#2}
    \setcolumnwidth{\fill, 4.5 cm}
    \begin{paracol}{2}
}{
    \switchcolumn \raggedleft \secondColumn
    \end{paracol}
    \endonecolentry
} % new environment for two column entries

\newenvironment{threecolentry}[3][]{
    \onecolentry
    \def\thirdColumn{#3}
    \setcolumnwidth{, \fill, 4.5 cm}
    \begin{paracol}{3}
    {\raggedright #2} \switchcolumn
}{
    \switchcolumn \raggedleft \thirdColumn
    \end{paracol}
    \endonecolentry
} % new environment for three column entries

\newenvironment{header}{
    \setlength{\topsep}{0pt}\par\kern\topsep\centering\linespread{1.5}
}{
    \par\kern\topsep
} % new environment for the header

\newcommand{\placelastupdatedtext}{% \placetextbox{<horizontal pos>}{<vertical pos>}{<stuff>}
  \AddToShipoutPictureFG*{% Add <stuff> to current page foreground
    \put(
        \LenToUnit{\paperwidth-2 cm-0 cm+0.05cm},
        \LenToUnit{\paperheight-1.0 cm}
    ){\vtop{{\null}\makebox[0pt][c]{
        \small\color{gray}\textit{Last updated in September 2024}\hspace{\widthof{Last updated in September 2024}}
    }}}%
  }%
}%

% save the original href command in a new command:
\let\hrefWithoutArrow\href

% new command for external links:


\begin{document}
    \newcommand{\AND}{\unskip
        \cleaders\copy\ANDbox\hskip\wd\ANDbox
        \ignorespaces
    }
    \newsavebox\ANDbox
    \sbox\ANDbox{$|$}

    \begin{header}
        \fontsize{25 pt}{25 pt}\selectfont John Doe

        \vspace{5 pt}

        \normalsize
        \mbox{Your Location}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{\hrefWithoutArrow{mailto:youremail@yourdomain.com}{youremail@yourdomain.com}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{\hrefWithoutArrow{tel:+90-541-999-99-99}{0541 999 99 99}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{\hrefWithoutArrow{https://yourwebsite.com/}{yourwebsite.com}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{\hrefWithoutArrow{https://linkedin.com/in/yourusername}{linkedin.com/in/yourusername}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{\hrefWithoutArrow{https://github.com/yourusername}{github.com/yourusername}}%
    \end{header}

    \vspace{5 pt - 0.3 cm}


    \section{Welcome to RenderCV!}



        
        \begin{onecolentry}
            \href{https://rendercv.com}{RenderCV} is a LaTeX-based CV/resume version-control and maintenance app. It allows you to create a high-quality CV or resume as a PDF file from a YAML file, with \textbf{Markdown syntax support} and \textbf{complete control over the LaTeX code}.
        \end{onecolentry}

        \vspace{0.2 cm}

        \begin{onecolentry}
            The boilerplate content was inspired by \href{https://github.com/dnl-blkv/mcdowell-cv}{Gayle McDowell}.
        \end{onecolentry}


    
    \section{Quick Guide}

    \begin{onecolentry}
        \begin{highlightsforbulletentries}


        \item Each section title is arbitrary and each section contains a list of entries.

        \item There are 7 unique entry types: \textit{BulletEntry}, \textit{TextEntry}, \textit{EducationEntry}, \textit{ExperienceEntry}, \textit{NormalEntry}, \textit{PublicationEntry}, and \textit{OneLineEntry}.

        \item Select a section title, pick an entry type, and start writing your section!

        \item \href{https://docs.rendercv.com/user_guide/}{Here}, you can find a comprehensive user guide for RenderCV.


        \end{highlightsforbulletentries}
    \end{onecolentry}

    \section{Education}



        
        \begin{twocolentry}{
            Sept 2000 – May 2005
        }
            \textbf{University of Pennsylvania}, BS in Computer Science\end{twocolentry}

        \vspace{0.10 cm}
        \begin{onecolentry}
            \begin{highlights}
                \item GPA: 3.9/4.0 (\href{https://example.com}{a link to somewhere})
                \item \textbf{Coursework:} Computer Architecture, Comparison of Learning Algorithms, Computational Theory
            \end{highlights}
        \end{onecolentry}



    
    \section{Experience}



        
        \begin{twocolentry}{
            June 2005 – Aug 2007
        }
            \textbf{Software Engineer}, Apple -- Cupertino, CA\end{twocolentry}

        \vspace{0.10 cm}
        \begin{onecolentry}
            \begin{highlights}
                \item Reduced time to render user buddy lists by 75\% by implementing a prediction algorithm
                \item Integrated iChat with Spotlight Search by creating a tool to extract metadata from saved chat transcripts and provide metadata to a system-wide search database
                \item Redesigned chat file format and implemented backward compatibility for search
            \end{highlights}
        \end{onecolentry}


        \vspace{0.2 cm}

        \begin{twocolentry}{
            June 2003 – Aug 2003
        }
            \textbf{Software Engineer Intern}, Microsoft -- Redmond, WA\end{twocolentry}

        \vspace{0.10 cm}
        \begin{onecolentry}
            \begin{highlights}
                \item Designed a UI for the VS open file switcher (Ctrl-Tab) and extended it to tool windows
                \item Created a service to provide gradient across VS and VS add-ins, optimizing its performance via caching
                \item Built an app to compute the similarity of all methods in a codebase, reducing the time from $\mathcal{O}(n^2)$ to $\mathcal{O}(n \log n)$
                \item Created a test case generation tool that creates random XML docs from XML Schema
                \item Automated the extraction and processing of large datasets from legacy systems using SQL and Perl scripts
            \end{highlights}
        \end{onecolentry}



    
    \section{Publications}



        
        \begin{samepage}
            \begin{twocolentry}{
                Jan 2004
            }
                \textbf{3D Finite Element Analysis of No-Insulation Coils}
            \end{twocolentry}

            \vspace{0.10 cm}
            
            \begin{onecolentry}
                \mbox{Frodo Baggins}, \mbox{\textbf{\textit{John Doe}}}, \mbox{Samwise Gamgee}

                \vspace{0.10 cm}
                
        \href{https://doi.org/10.1109/TASC.2023.3340648}{10.1109/TASC.2023.3340648}
        \end{onecolentry}
        \end{samepage}


    
    \section{Projects}



        
        \begin{twocolentry}{
            \href{https://github.com/sinaatalay/rendercv}{github.com/name/repo}
        }
            \textbf{Multi-User Drawing Tool}\end{twocolentry}

        \vspace{0.10 cm}
        \begin{onecolentry}
            \begin{highlights}
                \item Developed an electronic classroom where multiple users can simultaneously view and draw on a "chalkboard" with each person's edits synchronized
                \item Tools Used: C++, MFC
            \end{highlights}
        \end{onecolentry}


        \vspace{0.2 cm}

        \begin{twocolentry}{
            \href{https://github.com/sinaatalay/rendercv}{github.com/name/repo}
        }
            \textbf{Synchronized Desktop Calendar}\end{twocolentry}

        \vspace{0.10 cm}
        \begin{onecolentry}
            \begin{highlights}
                \item Developed a desktop calendar with globally shared and synchronized calendars, allowing users to schedule meetings with other users
                \item Tools Used: C\#, .NET, SQL, XML
            \end{highlights}
        \end{onecolentry}


        \vspace{0.2 cm}

        \begin{twocolentry}{
            2002
        }
            \textbf{Custom Operating System}\end{twocolentry}

        \vspace{0.10 cm}
        \begin{onecolentry}
            \begin{highlights}
                \item Built a UNIX-style OS with a scheduler, file system, text editor, and calculator
                \item Tools Used: C
            \end{highlights}
        \end{onecolentry}



    
    \section{Technologies}



        
        \begin{onecolentry}
            \textbf{Languages:} C++, C, Java, Objective-C, C\#, SQL, JavaScript
        \end{onecolentry}

        \vspace{0.2 cm}

        \begin{onecolentry}
            \textbf{Technologies:} .NET, Microsoft SQL Server, XCode, Interface Builder
        \end{onecolentry}


    

\end{document}}
```
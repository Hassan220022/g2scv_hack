import os
import sys
import json
import time
import argparse
import requests

# Add the shared directory to the path for utils
sys.path.append('/Users/mikawi/Developer/hackathon/g2scv_n/shared')
import utils
from pathlib import Path
from typing import Dict, Optional, Union, Any


def scrape_github_readmes(username: str) -> dict:
    """
    Call the GitHub README scraper service to fetch README files from user repositories.
    
    Args:
        username: GitHub username
        
    Returns:
        Dictionary with repository data including READMEs
    """
    print(f"Scraping GitHub READMEs for user: {username}")
    
    try:
        # Use importlib to load the module directly
        import importlib.util
        
        spec = importlib.util.spec_from_file_location(
            "github_scraper", 
            "/Users/mikawi/Developer/hackathon/g2scv_n/services/github_readme_scraper/main.py"
        )
        github_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(github_module)
        
        # Call the actual GitHub scraper function
        return github_module.scrape_github_readmes(username)
    except Exception as e:
        print(f"Error calling GitHub README scraper: {e}")
        # Fallback to mock data if the service is unavailable
        return {"repo1": {"name": "Mock Repo", "readme": "Error occurred while scraping GitHub READMEs."}}

def call_cv_ocr_api(cv_file_path: str, session_dir: str = None) -> dict:
    """
    Call the CV OCR parser service to extract information from a CV file.
    
    Args:
        cv_file_path: Path to the CV file
        session_dir: Session directory for saving results (optional)
        
    Returns:
        Dictionary with extracted data from the CV
    """
    print(f"Processing CV file: {cv_file_path}")
    
    try:
        # Check if the CV file exists
        if not os.path.exists(cv_file_path):
            print(f"Error: CV file not found at {cv_file_path}")
            return {"error": f"CV file not found at {cv_file_path}"}
        
        # Use importlib to load the module directly
        import importlib.util
        
        # Load the document_parser module
        spec = importlib.util.spec_from_file_location(
            "document_parser", 
            "/Users/mikawi/Developer/hackathon/g2scv_n/services/cv_ocr_parser/document_parser.py"
        )
        document_parser_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(document_parser_module)
        
        # Define bucket directory for direct saving
        bucket_dir = "/Users/mikawi/Developer/hackathon/g2scv_n/bucket"
        
        # Generate a filename from the CV file
        cv_filename = os.path.basename(cv_file_path)
        cv_name = os.path.splitext(cv_filename)[0]
        
        # Parse the CV with document_parser
        # First save to main bucket directory
        result = document_parser_module.parse_document(
            cv_file_path, 
            bucket_dir=bucket_dir,
            output_path=os.path.join(bucket_dir, f"{cv_name}_parsed.json")
        )
        
        # If session directory is provided, also save there
        if session_dir and os.path.exists(session_dir):
            session_result = document_parser_module.parse_document(
                cv_file_path,
                bucket_dir=session_dir,
                output_path=os.path.join(session_dir, "cv_ocr_data.json")
            )
            print(f"CV OCR data also saved to session: {os.path.join(session_dir, 'cv_ocr_data.json')}")
        
        return result
    except Exception as e:
        print(f"Error calling CV OCR parser: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to mock data if the service is unavailable
        return {"name": "CV Parse Error", "text": f"Error occurred while parsing CV: {str(e)}", "error": str(e)}

def call_rag_api(linkedin_json_path: str, github_json_path: str, cv_ocr_json_path: str) -> str:
    """
    Call the RAG API service to generate LaTeX CV from the collected data.
    
    Args:
        linkedin_json_path: Path to the LinkedIn profile data JSON file
        github_json_path: Path to the GitHub README data JSON file
        cv_ocr_json_path: Path to the CV OCR data JSON file
        
    Returns:
        LaTeX content for the generated CV
    """
    print(f"Calling RAG API with:\n- LinkedIn data: {linkedin_json_path}\n- GitHub data: {github_json_path}\n- CV OCR data: {cv_ocr_json_path}")
    
    try:
        # Import the RAG API module if available
        sys.path.append('/Users/mikawi/Developer/hackathon/g2scv_n/services/rag_module')
        try:
            from services.rag_module.rag_api import generate_cv
            
            # Load the data from JSON files
            with open(linkedin_json_path, 'r') as f:
                linkedin_data = json.load(f)
            
            with open(github_json_path, 'r') as f:
                github_data = json.load(f)
                
            with open(cv_ocr_json_path, 'r') as f:
                cv_ocr_data = json.load(f)
                
            # Call the actual RAG API function
            return generate_cv(linkedin_data, github_data, cv_ocr_data)
        except ImportError:
            # If the module is not available, use the rag_api API endpoint if it's running as a service
            rag_api_url = "http://localhost:8005/generate-cv"  # Adjust port if needed
            try:
                response = requests.post(
                    rag_api_url,
                    json={
                        "linkedin_json_path": linkedin_json_path,
                        "github_json_path": github_json_path,
                        "cv_ocr_json_path": cv_ocr_json_path
                    }
                )
                response.raise_for_status()
                return response.json().get("latex_content")
            except requests.exceptions.RequestException as e:
                print(f"Error calling RAG API service: {e}")
                # Fallback to mock data
                return r"\documentclass{article}\begin{document}\title{Generated CV}\author{Generated from LinkedIn, GitHub, and CV data}\maketitle\section{Error}Unable to generate complete CV due to RAG API service error.\end{document}"
    except Exception as e:
        print(f"Error in RAG processing: {e}")
        # Fallback to mock data if anything fails
        return r"\documentclass{article}\begin{document}\title{Generated CV}\author{Generated from LinkedIn, GitHub, and CV data}\maketitle\section{Error}Unable to generate complete CV due to an error.\end{document}"

def convert_latex_to_pdf(latex_content: str, output_dir: str, filename_base: str = "generated_cv") -> str:
    """
    Call the LaTeX to PDF service to convert LaTeX content to a PDF file.
    
    Args:
        latex_content: LaTeX content as a string
        output_dir: Directory to save the PDF file
        filename_base: Base name for the output files
        
    Returns:
        Path to the generated PDF file
    """
    print(f"Converting LaTeX to PDF and saving to {output_dir}/{filename_base}.pdf")
    
    try:
        # First save the LaTeX content to a file
        latex_file_path = os.path.join(output_dir, f"{filename_base}.tex")
        with open(latex_file_path, 'w') as f:
            f.write(latex_content)
            
        # Then call the LaTeX to PDF service using importlib
        try:
            # Use importlib to load the module directly
            import importlib.util
            
            # Load the latex_to_pdf module
            spec = importlib.util.spec_from_file_location(
                "latex_to_pdf", 
                "/Users/mikawi/Developer/hackathon/g2scv_n/services/latex_to_pdf/main.py"
            )
            latex_pdf_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(latex_pdf_module)
            
            return latex_pdf_module.process_latex_file(latex_file_path) or os.path.join(output_dir, f"{filename_base}.pdf")
        except Exception as e:
            print(f"Error importing LaTeX to PDF module: {e}")
            # Fallback to direct subprocess call if module import fails
            import subprocess
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', latex_file_path],
                cwd=output_dir,
                check=False
            )
            pdf_path = os.path.join(output_dir, f"{filename_base}.pdf")
            if os.path.exists(pdf_path):
                return pdf_path
            else:
                print(f"Error: PDF generation failed, file not found at {pdf_path}")
                return None
    except Exception as e:
        print(f"Error converting LaTeX to PDF: {e}")
        # Create a fallback text file with the LaTeX content
        fallback_path = os.path.join(output_dir, f"{filename_base}_text.txt")
        with open(fallback_path, 'w') as f:
            f.write(f"LaTeX conversion failed. Original LaTeX content:\n\n{latex_content}")
        print(f"LaTeX content saved as text file: {fallback_path}")
        return fallback_path


def main_orchestrator(linkedin_url: str, github_username: str, cv_file_path: str, output_dir: Optional[str] = None):
    print("Starting CV generation process...\n")

    # 1. Create new dir in /bucket with a random id.
    # This is the single source of truth for the session's storage location.
    session_dir = utils.create_session_dir() # e.g., bucket/some-uuid/

    linkedin_json_path = None
    github_json_path = None
    cv_ocr_json_path = None
    generated_cv_path = None

    try:
        # 2. Call LinkedIn API, get its data, and save it in the session_dir
        print("\n--- Calling LinkedIn API ---")
        linkedin_api_service_url = "http://localhost:8004" # Base URL for the LinkedIn service
        try:
            response = requests.post(f"{linkedin_api_service_url}/scrape-linkedin", json={"url": linkedin_url})
            response.raise_for_status()
            linkedin_api_response_data = response.json() # This is LinkedInProfileDataResponse

            if linkedin_api_response_data.get("success"):
                linkedin_profile_data = linkedin_api_response_data.get("profile_data")
                apify_run_id = linkedin_api_response_data.get("run_id")
                apify_dataset_id = linkedin_api_response_data.get("dataset_id")

                if linkedin_profile_data:
                    linkedin_filename = "linkedin_profile.json"
                    linkedin_json_path = utils.save_json_to_file(
                        data=linkedin_profile_data,
                        dir_path=session_dir, # Orchestrator controls save location
                        filename=linkedin_filename
                    )
                    print(f"LinkedIn data received from API and saved to: {linkedin_json_path}")

                    # Now that main.py has saved the data, tell LinkedIn API to clean up Apify
                    if apify_run_id and apify_dataset_id:
                        print(f"Confirming data receipt with LinkedIn API to delete Apify data (run: {apify_run_id})...")
                        try:
                            confirm_response = requests.post(
                                f"{linkedin_api_service_url}/confirm-data-receipt",
                                json={"run_id": apify_run_id, "dataset_id": apify_dataset_id}
                            )
                            if confirm_response.status_code == 200:
                                print(f"Apify data deletion initiated via LinkedIn API: {confirm_response.json().get('message')}")
                            else:
                                print(f"Warning: Failed to confirm data receipt with LinkedIn API. Status: {confirm_response.status_code} - {confirm_response.text}")
                        except requests.exceptions.RequestException as confirm_exc:
                             print(f"Error calling /confirm-data-receipt on LinkedIn API: {confirm_exc}")
                else:
                    print("LinkedIn API call successful but no 'profile_data' in response.")
            else:
                print(f"LinkedIn API call failed: {linkedin_api_response_data.get('message', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            print(f"Error calling LinkedIn API service: {e}")
        print("--- LinkedIn API Call Complete ---")


        # 3. Call GitHub function and save its returned json in the SAME session_dir
        print("\n--- Calling GitHub Scraper ---")
        try:
            # Call the GitHub README scraper service
            github_data = scrape_github_readmes(github_username)
            if github_data:
                github_filename = f"github_data_{github_username}.json"
                # Save GitHub data directly to the main bucket directory
                bucket_dir = "/Users/mikawi/Developer/hackathon/g2scv_n/bucket"
                github_json_path = utils.save_json_to_file(
                    data=github_data,
                    dir_path=bucket_dir, # Save directly to main bucket directory
                    filename=github_filename
                )
                # Also save to session directory for consistency with other services
                session_github_path = utils.save_json_to_file(
                    data=github_data,
                    dir_path=session_dir,
                    filename=github_filename
                )
                print(f"GitHub data saved to bucket: {github_json_path}")
                print(f"GitHub data also saved to session: {session_github_path}")
            else:
                print(f"No data returned from GitHub scraper for user {github_username}.")
        except Exception as e:
            print(f"Error calling GitHub scraper: {e}")
        print("--- GitHub Scraper Call Complete ---")


        # 4. Call the CV OCR API to extract info and store result in the SAME session_dir
        print("\n--- Calling CV OCR API ---")
        if not os.path.exists(cv_file_path):
            print(f"Error: CV file for OCR not found at {cv_file_path}. Skipping OCR.")
        else:
            try:
                # Call the CV OCR parser service with the session directory
                cv_ocr_data = call_cv_ocr_api(cv_file_path, session_dir=session_dir)
                if cv_ocr_data and not cv_ocr_data.get("error"): # Check for actual data / no error
                    # Data is now saved directly by the parser in both locations
                    # The session path is used in the orchestrator
                    cv_ocr_json_path = os.path.join(session_dir, "cv_ocr_data.json")
                    # Also save to main bucket with specific name derived from CV file
                    cv_filename = os.path.basename(cv_file_path)
                    cv_name = os.path.splitext(cv_filename)[0]
                    bucket_path = f"/Users/mikawi/Developer/hackathon/g2scv_n/bucket/{cv_name}_parsed.json"
                    print(f"CV OCR data saved to: {cv_ocr_json_path}")
                    print(f"CV OCR data also saved to bucket: {bucket_path}")
                else:
                    print(f"CV OCR API returned no data or an error for {cv_file_path}.")
            except Exception as e:
                print(f"Error calling CV OCR API: {e}")
        print("--- CV OCR API Call Complete ---")


        # 5. Call RAG API -> giving it the paths to the JSON files within session_dir
        print("\n--- Calling RAG API ---")
        if all([linkedin_json_path, github_json_path, cv_ocr_json_path]):
            try:
                latex_output = call_rag_api(linkedin_json_path, github_json_path, cv_ocr_json_path)
                if latex_output:
                    # 6. Send LaTeX to service for PDF conversion, save in session_dir
                    print("\n--- Calling LaTeX to PDF Service ---")
                    generated_cv_path = convert_latex_to_pdf(latex_output, session_dir, "generated_cv")
                    print("--- LaTeX to PDF Service Call Complete ---")
                else:
                    print("RAG API did not return LaTeX content.")
            except Exception as e:
                print(f"Error in RAG API or LaTeX conversion: {e}")
        else:
            missing_files = [name for name, path in [("LinkedIn", linkedin_json_path), ("GitHub", github_json_path), ("CV OCR", cv_ocr_json_path)] if not path]
            print(f"Skipping RAG API and LaTeX conversion due to missing data from: {', '.join(missing_files)}")


        # 7. Return path for new CV and ask for confirmation
        print("\n--- Process Complete ---")
        if generated_cv_path and os.path.exists(generated_cv_path):
            print(f"Successfully generated CV! You can find it at: {generated_cv_path}")
            user_acceptance = input("Is the generated CV accepted? (yes/no/edit): ").strip().lower()
            # ... (handle user_acceptance) ...
        else:
            print("CV generation failed or was skipped. Please check logs and session directory.")
        print(f"All session files are located in: {session_dir}")

    except Exception as e:
        print(f"An unexpected error occurred during orchestration: {e}")
        if session_dir: # Should always be defined if create_session_dir succeeded
            print(f"Session files might be incomplete. Check directory: {session_dir}")

def parse_arguments():
    """
    Parse command line arguments for the orchestrator.
    """
    parser = argparse.ArgumentParser(description="G2S CV Generator Orchestrator")
    parser.add_argument("--linkedin", "-l", type=str, help="LinkedIn profile URL")
    parser.add_argument("--github", "-g", type=str, help="GitHub username")
    parser.add_argument("--cv", "-c", type=str, help="Path to the CV file for OCR")
    parser.add_argument("--output", "-o", type=str, help="Output directory for generated files (default: session directory in bucket)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode, prompting for missing information")
    parser.add_argument("--cv-only", action="store_true", help="Run only the CV OCR parsing functionality (skips LinkedIn and GitHub)")
    
    return parser.parse_args()

def interactive_mode():
    """
    Run the orchestrator in interactive mode, prompting for information.
    """
    print("=== G2S CV Generator - Interactive Mode ===\n")
    
    # Get LinkedIn URL
    linkedin_url = input("Enter LinkedIn profile URL (or press Enter to skip): ").strip()
    
    # Get GitHub username
    github_username = input("Enter GitHub username (or press Enter to skip): ").strip()
    
    # Get CV file path
    cv_file_path = input("Enter path to CV file (or press Enter to use a dummy CV): ").strip()
    if not cv_file_path:
        # Create a dummy CV if none provided
        dummy_cv_path = "dummy_cv.pdf"
        if not os.path.exists(dummy_cv_path):
            with open(dummy_cv_path, "w") as f:
                f.write("Dummy CV content.")
            print(f"Created dummy CV: {dummy_cv_path}")
        cv_file_path = dummy_cv_path
    elif not os.path.exists(cv_file_path):
        print(f"Warning: CV file not found at {cv_file_path}. Creating a dummy CV instead.")
        with open("dummy_cv.pdf", "w") as f:
            f.write("Dummy CV content.")
        cv_file_path = "dummy_cv.pdf"
    
    # Get output directory
    output_dir = input("Enter output directory (or press Enter for default): ").strip()
    
    # Ensure LinkedIn API is running
    print("\nEnsure the LinkedIn API service (linkedin_api.py) is running on http://localhost:8004")
    input("Press Enter to start the orchestration process once the LinkedIn API is ready...")
    
    # Run the orchestrator
    main_orchestrator(
        linkedin_url=linkedin_url,
        github_username=github_username,
        cv_file_path=cv_file_path,
        output_dir=output_dir if output_dir else None
    )

def cv_only_processor(cv_file_path: str, output_dir: str = None):
    """
    Process only the CV OCR functionality, skipping LinkedIn and GitHub steps.
    This function is used when the --cv-only flag is specified.
    
    Args:
        cv_file_path: Path to the CV file for OCR
        output_dir: Optional output directory
    """
    print("Starting CV OCR processing...")    
    # Validate CV file
    if not cv_file_path or not os.path.exists(cv_file_path):
        print(f"Error: CV file not found at {cv_file_path}")
        return
    
    # Create a session directory for output if no output_dir specified
    session_dir = output_dir if output_dir else utils.create_session_dir()
    print(f"\nCreated session directory: {session_dir}")
    
    try:
        # Call the CV OCR parser directly
        print("\n--- Running CV OCR Parser ---")
        cv_ocr_data = call_cv_ocr_api(cv_file_path, session_dir=session_dir)
        
        if cv_ocr_data and not cv_ocr_data.get("error"):
            # Get paths for reference
            cv_ocr_json_path = os.path.join(session_dir, "cv_ocr_data.json")
            cv_filename = os.path.basename(cv_file_path)
            cv_name = os.path.splitext(cv_filename)[0]
            bucket_path = f"/Users/mikawi/Developer/hackathon/g2scv_n/bucket/{cv_name}_parsed.json"
            
            # Print summary of CV data
            print("\n--- CV OCR Parsing Results Summary ---")
            if cv_ocr_data.get("metadata"):
                print(f"Document Type: {cv_ocr_data['metadata'].get('Producer', 'Unknown')}")
            
            if cv_ocr_data.get("content"):
                content_preview = cv_ocr_data["content"][:150] + "..." if len(cv_ocr_data["content"]) > 150 else cv_ocr_data["content"]
                print(f"Content Preview: {content_preview}")
            
            if cv_ocr_data.get("entities"):
                print("Extracted Entities:")
                for entity_type, entities in cv_ocr_data["entities"].items():
                    if entities:
                        print(f"  {entity_type}: {len(entities)} items")
                        print(f"    Sample: {', '.join(entities[:5])}{'...' if len(entities) > 5 else ''}")
            
            if cv_ocr_data.get("cv_sections"):
                print("CV Sections Found:")
                for section in cv_ocr_data["cv_sections"]:
                    print(f"  {section}")
                    
            print(f"\nFull CV parsing results saved to:\n- Session: {cv_ocr_json_path}\n- Bucket: {bucket_path}")
            print("\n--- CV OCR Processing Complete ---")
        else:
            print(f"Error: CV OCR parsing failed. {cv_ocr_data.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"An unexpected error occurred during CV OCR processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Check if CV-only mode is specified
    if args.cv_only:
        if not args.cv:
            print("Error: --cv-only requires a CV file path to be specified with --cv")
        else:
            cv_only_processor(args.cv, args.output)
    # If interactive mode is enabled or no arguments are provided, use interactive mode
    elif args.interactive or not (args.linkedin or args.github or args.cv):
        interactive_mode()
    else:
        # Use command line arguments
        linkedin_url = args.linkedin or "https://www.linkedin.com/in/williamhgates/"  # Default if not provided
        github_username = args.github or "torvalds"  # Default if not provided
        
        # Check if CV file exists, create dummy if not provided or not found
        if not args.cv:
            dummy_cv_path = "dummy_cv.pdf"
            if not os.path.exists(dummy_cv_path):
                with open(dummy_cv_path, "w") as f:
                    f.write("Dummy CV content.")
                print(f"Created dummy CV: {dummy_cv_path}")
            cv_file_path = dummy_cv_path
        else:
            cv_file_path = args.cv
            if not os.path.exists(cv_file_path):
                print(f"Warning: CV file not found at {cv_file_path}. Creating a dummy CV instead.")
                with open("dummy_cv.pdf", "w") as f:
                    f.write("Dummy CV content.")
                cv_file_path = "dummy_cv.pdf"
        
        print("Ensure the LinkedIn API service (linkedin_api.py) is running on http://localhost:8004")
        input("Press Enter to start the orchestration process once the LinkedIn API is ready...")
        
        # Run the orchestrator
        main_orchestrator(
            linkedin_url=linkedin_url,
            github_username=github_username,
            cv_file_path=cv_file_path,
            output_dir=args.output
        )
import os
import sys
import json
import time
import argparse
import requests
import concurrent.futures # Added for parallelism

# Add the shared directory to the path for utils
sys.path.append('/Users/mikawi/Developer/hackathon/g2scv_n/shared')
import utils
from pathlib import Path
from typing import Dict, Optional, Union, Any


# Helper function to encapsulate LinkedIn API call for parallel execution
def process_linkedin_data(linkedin_url: str, session_dir: str) -> Optional[str]:
    """
    Calls the LinkedIn API, gets its data, and saves it in the session_dir.

    Args:
        linkedin_url: The URL of the LinkedIn profile.
        session_dir: The directory to save the LinkedIn data.

    Returns:
        Path to the saved LinkedIn JSON file or None if an error occurs.
    """
    print("\n--- Calling LinkedIn API ---")
    linkedin_api_service_url = "http://localhost:8004" # Base URL for the LinkedIn service
    linkedin_json_path = None
    try:
        response = requests.post(f"{linkedin_api_service_url}/scrape-linkedin", json={"url": linkedin_url})
        response.raise_for_status()
        linkedin_api_response_data = response.json()

        if linkedin_api_response_data.get("success"):
            linkedin_profile_data = linkedin_api_response_data.get("profile_data")
            apify_run_id = linkedin_api_response_data.get("run_id")
            apify_dataset_id = linkedin_api_response_data.get("dataset_id")

            if linkedin_profile_data:
                linkedin_filename = "linkedin_profile.json"
                linkedin_json_path = utils.save_json_to_file(
                    data=linkedin_profile_data,
                    dir_path=session_dir,
                    filename=linkedin_filename
                )
                print(f"LinkedIn data received from API and saved to: {linkedin_json_path}")

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
    return linkedin_json_path

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

        return result # Return the result from the primary save location
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
    session_dir = utils.create_session_dir() # e.g., bucket/some-uuid/
    print(f"Session directory created: {session_dir}")


    linkedin_json_path = None
    github_data = None # Store raw data first
    cv_ocr_data = None # Store raw data first
    generated_cv_path = None

    # Paths for JSON files after saving
    saved_github_json_path = None
    saved_cv_ocr_json_path = None

    try:
        # --- Execute these tasks in parallel ---
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit LinkedIn task
            future_linkedin = executor.submit(process_linkedin_data, linkedin_url, session_dir)

            # Submit GitHub task
            future_github = executor.submit(scrape_github_readmes, github_username)

            # Submit CV OCR task
            # Ensure cv_file_path is valid before submitting
            if not os.path.exists(cv_file_path):
                print(f"Error: CV file for OCR not found at {cv_file_path}. Skipping OCR for parallel execution.")
                future_cv_ocr = executor.submit(lambda: {"error": f"CV file not found at {cv_file_path}"}) # Submit a dummy task that returns an error
            else:
                future_cv_ocr = executor.submit(call_cv_ocr_api, cv_file_path, session_dir) # session_dir is passed for saving

            # Retrieve results
            print("\n--- Waiting for parallel tasks (LinkedIn, GitHub, CV OCR) to complete ---")
            linkedin_json_path = future_linkedin.result() # This is already the path or None
            github_data = future_github.result()
            cv_ocr_data_result = future_cv_ocr.result() # This is the raw data from call_cv_ocr_api or an error dict
        print("--- Parallel tasks completed ---")


        # --- Process results from parallel tasks (Saving data) ---

        # 2. Process and Save GitHub Data (already retrieved as github_data)
        print("\n--- Processing GitHub Scraper Data ---")
        if github_data and not github_data.get("error"): # Check if data is valid
            github_filename = f"github_data_{github_username}.json"
            bucket_dir = "/Users/mikawi/Developer/hackathon/g2scv_n/bucket" # Main bucket
            # Save to main bucket
            utils.save_json_to_file(
                data=github_data,
                dir_path=bucket_dir,
                filename=github_filename
            )
            # Save to session directory and get path for RAG
            saved_github_json_path = utils.save_json_to_file(
                data=github_data,
                dir_path=session_dir,
                filename=github_filename
            )
            print(f"GitHub data saved to bucket: {os.path.join(bucket_dir, github_filename)}")
            print(f"GitHub data also saved to session: {saved_github_json_path}")
        elif github_data and github_data.get("error"):
             print(f"GitHub scraping resulted in an error: {github_data.get('readme', 'Unknown GitHub error')}")
        else:
            print(f"No data returned or error from GitHub scraper for user {github_username}.")
        print("--- GitHub Data Processing Complete ---")


        # 3. Process and Save CV OCR Data (already retrieved as cv_ocr_data_result)
        print("\n--- Processing CV OCR API Data ---")
        if 'error' not in cv_ocr_data_result: # call_cv_ocr_api now handles saving to session_dir if successful
            # The file cv_ocr_data.json should already be in session_dir if call_cv_ocr_api was successful
            saved_cv_ocr_json_path = os.path.join(session_dir, "cv_ocr_data.json")
            if not os.path.exists(saved_cv_ocr_json_path):
                 # This case might happen if call_cv_ocr_api had an internal issue not returning "error" but failed to save
                 print(f"Warning: CV OCR data was expected in {saved_cv_ocr_json_path} but not found. Saving manually.")
                 if cv_ocr_data_result: # If there's some data to save
                    utils.save_json_to_file(cv_ocr_data_result, session_dir, "cv_ocr_data.json")
                    print(f"CV OCR data manually saved to: {saved_cv_ocr_json_path}")
                 else:
                    saved_cv_ocr_json_path = None # Ensure it's None if truly no data
                    print("No CV OCR data to save.")
            else:
                print(f"CV OCR data was processed and saved by call_cv_ocr_api to: {saved_cv_ocr_json_path}")
                # Main bucket saving is handled within call_cv_ocr_api
                cv_filename = os.path.basename(cv_file_path)
                cv_name = os.path.splitext(cv_filename)[0]
                bucket_cv_path = f"/Users/mikawi/Developer/hackathon/g2scv_n/bucket/{cv_name}_parsed.json"
                print(f"CV OCR data also saved by call_cv_ocr_api to bucket: {bucket_cv_path}")

        elif cv_ocr_data_result and cv_ocr_data_result.get("error"):
            print(f"CV OCR API returned an error: {cv_ocr_data_result['error']}")
        else: # Should not happen if cv_file_path was invalid initially and skipped.
             print(f"CV OCR API returned no data or an unexpected result for {cv_file_path}.")
        print("--- CV OCR API Data Processing Complete ---")


        # --- Sequential Tasks ---

        # 4. Call RAG API
        print("\n--- Calling RAG API ---")
        # Ensure all required JSON paths are valid before calling RAG
        # linkedin_json_path is already set from future_linkedin.result()
        if linkedin_json_path and saved_github_json_path and saved_cv_ocr_json_path:
            if os.path.exists(linkedin_json_path) and \
               os.path.exists(saved_github_json_path) and \
               os.path.exists(saved_cv_ocr_json_path):
                try:
                    latex_output = call_rag_api(linkedin_json_path, saved_github_json_path, saved_cv_ocr_json_path)
                    if latex_output:
                        # 5. Convert LaTeX to PDF
                        print("\n--- Calling LaTeX to PDF Service ---")
                        generated_cv_path = convert_latex_to_pdf(latex_output, session_dir, "generated_cv")
                        print("--- LaTeX to PDF Service Call Complete ---")
                    else:
                        print("RAG API did not return LaTeX content.")
                except Exception as e:
                    print(f"Error in RAG API or LaTeX conversion: {e}")
            else:
                missing_for_rag = []
                if not os.path.exists(linkedin_json_path): missing_for_rag.append(f"LinkedIn data ({linkedin_json_path})")
                if not os.path.exists(saved_github_json_path): missing_for_rag.append(f"GitHub data ({saved_github_json_path})")
                if not os.path.exists(saved_cv_ocr_json_path): missing_for_rag.append(f"CV OCR data ({saved_cv_ocr_json_path})")
                print(f"Skipping RAG API: One or more input JSON files do not exist: {', '.join(missing_for_rag)}")
        else:
            missing_files = []
            if not linkedin_json_path: missing_files.append("LinkedIn data path")
            if not saved_github_json_path: missing_files.append("GitHub data path")
            if not saved_cv_ocr_json_path: missing_files.append("CV OCR data path")
            print(f"Skipping RAG API and LaTeX conversion due to missing data paths from: {', '.join(missing_files)}")


        # 6. Return path for new CV and ask for confirmation
        print("\n--- Process Complete ---")
        if generated_cv_path and os.path.exists(generated_cv_path):
            print(f"Successfully generated CV! You can find it at: {generated_cv_path}")
            # For non-interactive execution, we might not want this input
            # user_acceptance = input("Is the generated CV accepted? (yes/no/edit): ").strip().lower()
            # ... (handle user_acceptance) ...
        else:
            print("CV generation failed or was skipped. Please check logs and session directory.")
        print(f"All session files are located in: {session_dir}")

    except Exception as e:
        print(f"An unexpected error occurred during orchestration: {e}")
        import traceback
        traceback.print_exc()
        if session_dir:
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

    linkedin_url = input("Enter LinkedIn profile URL (or press Enter to skip): ").strip()
    if not linkedin_url: # Provide a default if skipped in interactive for testing
        linkedin_url = "https://www.linkedin.com/in/williamhgates/" # Example
        print(f"Using default LinkedIn URL: {linkedin_url}")


    github_username = input("Enter GitHub username (or press Enter to skip): ").strip()
    if not github_username: # Provide a default if skipped
        github_username = "torvalds" # Example
        print(f"Using default GitHub username: {github_username}")


    cv_file_path = input("Enter path to CV file (or press Enter to use a dummy CV): ").strip()
    if not cv_file_path:
        dummy_cv_path = "dummy_cv.pdf"
        if not os.path.exists(dummy_cv_path):
            try:
                with open(dummy_cv_path, "w") as f:
                    f.write("Dummy CV content for testing.")
                print(f"Created dummy CV: {dummy_cv_path}")
            except IOError as e:
                print(f"Error creating dummy CV {dummy_cv_path}: {e}")
                return # Cannot proceed without a CV or dummy
        cv_file_path = dummy_cv_path
    elif not os.path.exists(cv_file_path):
        print(f"Warning: CV file not found at {cv_file_path}. Attempting to create a dummy CV.")
        dummy_cv_path = os.path.join(os.getcwd(), "dummy_cv_interactive.pdf") # Ensure it's a full path or in CWD
        try:
            with open(dummy_cv_path, "w") as f:
                f.write("Dummy CV content created because original was not found.")
            cv_file_path = dummy_cv_path
            print(f"Using dummy CV: {cv_file_path}")
        except IOError as e:
            print(f"Error creating dummy CV {dummy_cv_path}: {e}")
            print("Please provide a valid CV path or ensure write permissions for dummy CV creation.")
            return


    output_dir_input = input("Enter output directory (or press Enter for default session directory): ").strip()
    output_dir = output_dir_input if output_dir_input else None


    print("\nEnsure the LinkedIn API service (linkedin_api.py) is running on http://localhost:8004")
    # input("Press Enter to start the orchestration process once the LinkedIn API is ready...") # Commenting out for faster testing

    main_orchestrator(
        linkedin_url=linkedin_url,
        github_username=github_username,
        cv_file_path=cv_file_path,
        output_dir=output_dir
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
    if not cv_file_path or not os.path.exists(cv_file_path):
        print(f"Error: CV file not found at {cv_file_path}")
        return

    session_dir = output_dir if output_dir else utils.create_session_dir()
    print(f"\nSession directory: {session_dir}") # Corrected from "Created session directory" to "Session directory"

    try:
        print("\n--- Running CV OCR Parser ---")
        # In cv_only_mode, call_cv_ocr_api will save to session_dir
        cv_ocr_data_result = call_cv_ocr_api(cv_file_path, session_dir=session_dir)

        if cv_ocr_data_result and not cv_ocr_data_result.get("error"):
            cv_ocr_json_path = os.path.join(session_dir, "cv_ocr_data.json") # Path where it should be saved
            # Main bucket path is constructed based on the cv_file_path
            cv_filename = os.path.basename(cv_file_path)
            cv_name = os.path.splitext(cv_filename)[0]
            bucket_path = f"/Users/mikawi/Developer/hackathon/g2scv_n/bucket/{cv_name}_parsed.json"


            print("\n--- CV OCR Parsing Results Summary ---")
            # Check if the actual data (not just paths) is available in cv_ocr_data_result for summary
            if cv_ocr_data_result.get("metadata"):
                print(f"Document Type: {cv_ocr_data_result['metadata'].get('Producer', 'Unknown')}")

            if cv_ocr_data_result.get("content"):
                content_preview = cv_ocr_data_result["content"][:150] + "..." if len(cv_ocr_data_result["content"]) > 150 else cv_ocr_data_result["content"]
                print(f"Content Preview: {content_preview}")

            if cv_ocr_data_result.get("entities"):
                print("Extracted Entities:")
                for entity_type, entities in cv_ocr_data_result["entities"].items():
                    if entities:
                        print(f"  {entity_type}: {len(entities)} items")
                        print(f"    Sample: {', '.join(str(e) for e in entities[:5])}{'...' if len(entities) > 5 else ''}") # Ensure entities are strings for join

            if cv_ocr_data_result.get("cv_sections"):
                print("CV Sections Found:")
                for section in cv_ocr_data_result["cv_sections"]:
                    print(f"  {section}")

            print(f"\nFull CV parsing results saved to:\n- Session: {cv_ocr_json_path}\n- Bucket: {bucket_path}")
            print("\n--- CV OCR Processing Complete ---")
        else:
            print(f"Error: CV OCR parsing failed. {cv_ocr_data_result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"An unexpected error occurred during CV OCR processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    args = parse_arguments()

    if args.cv_only:
        if not args.cv:
            print("Error: --cv-only requires a CV file path to be specified with --cv")
        else:
            cv_only_processor(args.cv, args.output)
    elif args.interactive or not (args.linkedin or args.github or args.cv):
        interactive_mode()
    else:
        linkedin_url = args.linkedin or "https://www.linkedin.com/in/williamhgates/"
        github_username = args.github or "torvalds"

        if not args.cv:
            dummy_cv_path = "dummy_cv_main.pdf" # Different name to avoid conflict with interactive
            if not os.path.exists(dummy_cv_path):
                try:
                    with open(dummy_cv_path, "w") as f:
                        f.write("Dummy CV content for main execution.")
                    print(f"Created dummy CV: {dummy_cv_path}")
                except IOError as e:
                    print(f"Error creating dummy CV {dummy_cv_path}: {e}")
                    sys.exit(1) # Exit if dummy CV cannot be created
            cv_file_path = dummy_cv_path
        else:
            cv_file_path = args.cv
            if not os.path.exists(cv_file_path):
                print(f"Warning: CV file not found at {cv_file_path}. Attempting to create a dummy CV.")
                dummy_cv_path_fallback = "dummy_cv_main_fallback.pdf"
                try:
                    with open(dummy_cv_path_fallback, "w") as f:
                        f.write("Dummy CV content, original CV not found.")
                    print(f"Using dummy CV: {dummy_cv_path_fallback}")
                    cv_file_path = dummy_cv_path_fallback
                except IOError as e:
                    print(f"Error creating dummy CV {dummy_cv_path_fallback}: {e}")
                    print("Please provide a valid CV path.")
                    sys.exit(1)


        print("Ensure the LinkedIn API service (linkedin_api.py) is running on http://localhost:8004")
        # input("Press Enter to start the orchestration process once the LinkedIn API is ready...") # Commented out for faster testing

        main_orchestrator(
            linkedin_url=linkedin_url,
            github_username=github_username,
            cv_file_path=cv_file_path,
            output_dir=args.output
        )
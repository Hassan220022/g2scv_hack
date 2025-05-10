import os
import requests # For calling the LinkedIn FastAPI service
import time # For potential delays or retries
import utils


def scrape_github_readmes_mock(username: str) -> dict:
    print(f"MOCK: Scraping GitHub READMEs for user: {username}")
    return {"repo1": {"name": "Mock Repo", "readme": "Mock Readme Content"}}

def call_cv_ocr_api_mock(cv_file_path: str) -> dict:
    print(f"MOCK: Processing CV file: {cv_file_path}")
    return {"name": "John Doe CV", "text": "CV text"}

def call_rag_api_mock(linkedin_json_path: str, github_json_path: str, cv_ocr_json_path: str) -> str: # Keep mock
    print(f"MOCK: RAG API called with {linkedin_json_path}, {github_json_path}, {cv_ocr_json_path}")
    return "\\documentclass{article}\\begin{document}Mock CV\\end{document}"

def convert_latex_to_pdf_mock(latex_content: str, output_dir: str, filename_base: str = "generated_cv") -> str: # Keep mock
    pdf_path = os.path.join(output_dir, f"{filename_base}.pdf")
    with open(pdf_path, 'w') as f: f.write("Mock PDF")
    print(f"MOCK: PDF saved to {pdf_path}")
    return pdf_path


def main_orchestrator(linkedin_url: str, github_username: str, cv_file_path: str):
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
            # Assuming scrape_github_readmes (or its mock) returns the data directly
            github_data = scrape_github_readmes_mock(github_username) # Replace with actual import and call
            if github_data:
                github_filename = "github_data.json"
                github_json_path = utils.save_json_to_file(
                    data=github_data,
                    dir_path=session_dir, # Orchestrator controls save location
                    filename=github_filename
                )
                print(f"GitHub data saved to: {github_json_path}")
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
                # Assuming call_cv_ocr_api (or its mock) returns data directly
                cv_ocr_data = call_cv_ocr_api_mock(cv_file_path)
                if cv_ocr_data and not cv_ocr_data.get("error"): # Check for actual data / no error
                    cv_ocr_filename = "cv_ocr_data.json"
                    cv_ocr_json_path = utils.save_json_to_file(
                        data=cv_ocr_data,
                        dir_path=session_dir, # Orchestrator controls save location
                        filename=cv_ocr_filename
                    )
                    print(f"CV OCR data saved to: {cv_ocr_json_path}")
                else:
                    print(f"CV OCR API returned no data or an error for {cv_file_path}.")
            except Exception as e:
                print(f"Error calling CV OCR API: {e}")
        print("--- CV OCR API Call Complete ---")


        # 5. Call RAG API -> giving it the paths to the JSON files within session_dir
        print("\n--- Calling RAG API ---")
        if all([linkedin_json_path, github_json_path, cv_ocr_json_path]):
            try:
                latex_output = call_rag_api_mock(linkedin_json_path, github_json_path, cv_ocr_json_path)
                if latex_output:
                    # 6. Send LaTeX to service for PDF conversion, save in session_dir
                    print("\n--- Calling LaTeX to PDF Service ---")
                    generated_cv_path = convert_latex_to_pdf_mock(latex_output, session_dir, "generated_cv")
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

if __name__ == "__main__":
    linkedin_profile_url = "https://www.linkedin.com/in/williamhgates/" # Example
    github_user = "torvalds" # Example
    dummy_cv_path = "dummy_cv.pdf"
    if not os.path.exists(dummy_cv_path):
        with open(dummy_cv_path, "w") as f: f.write("Dummy CV content.")
        print(f"Created dummy CV: {dummy_cv_path}")
    cv_document_path = dummy_cv_path

    print("Ensure the LinkedIn API service (linkedin_api.py) is running on http://localhost:8004")
    input("Press Enter to start the orchestration process once the LinkedIn API is ready...")

    main_orchestrator(
        linkedin_url=linkedin_profile_url,
        github_username=github_user,
        cv_file_path=cv_document_path
    )
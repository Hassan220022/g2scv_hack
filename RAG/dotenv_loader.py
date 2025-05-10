"""
Utility module for loading environment variables from .env file
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def load_env_vars():
    """
    Load environment variables from .env file
    """
    # Get the directory of the current file
    current_dir = Path(__file__).parent.absolute()
    
    # Path to .env file
    env_path = current_dir / '.env'
    
    # Load environment variables from .env file
    load_dotenv(dotenv_path=env_path)
    
    # Check if OPENAI_API_KEY is set
    check_openai_api_key()

def check_openai_api_key():
    """
    Check if OPENAI_API_KEY is set in environment variables
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("WARNING: OPENAI_API_KEY environment variable is not set.")
        print("Please set it in the .env file or in your environment variables.")
        print("You can create an API key at https://platform.openai.com/account/api-keys")
        return False
    
    if api_key == "your_openai_api_key_here":
        print("WARNING: You are using the default API key.")
        print("Please replace it with your actual OpenAI API key in the .env file.")
        return False
    
    return True

if __name__ == "__main__":
    # Example usage
    load_env_vars()
    if check_openai_api_key():
        print("OpenAI API key is set and ready to use.")
    else:
        print("Please provide your OpenAI API key before running the application.") 
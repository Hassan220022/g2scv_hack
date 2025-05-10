import os
import json
import uuid

BUCKET_BASE_DIR = "../bucket"

def create_session_dir(base_dir: str = BUCKET_BASE_DIR) -> str:
    """
    Creates a new directory with a random UUID name within the specified base directory.

    Args:
        base_dir: The base directory where the new session directory will be created.

    Returns:
        The path to the newly created session directory.
    """
    session_id = str(uuid.uuid4())
    session_dir_path = os.path.join(base_dir, session_id)
    os.makedirs(session_dir_path, exist_ok=True)
    print(f"Created session directory: {session_dir_path}")
    return session_dir_path

def save_json_to_file(data: any, dir_path: str, filename: str) -> str:
    """
    Saves dictionary data as a JSON file in the specified directory.

    Args:
        data: The dictionary data to save.
        dir_path: The directory where the file will be saved.
        filename: The name of the JSON file (e.g., "linkedin_data.json").

    Returns:
        The full path to the saved JSON file.
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path} as it did not exist.")

    file_path = os.path.join(dir_path, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data successfully saved to {file_path}")
    return file_path

def read_json_from_file(file_path: str) -> dict:
    """
    Reads JSON data from a file.

    Args:
        file_path: The path to the JSON file.

    Returns:
        The loaded JSON data as a dictionary.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return {}
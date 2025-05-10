"""
Test script for GitHub README search functionality from the RAG module.
This script directly tests the search_github_readmes function.
"""

import os
import json
from pathlib import Path
from services.rag_module.rag_api import load_github_data, search_github_readmes

def main():
    # Load GitHub data
    try:
        github_data = load_github_data()
        print(f"Loaded GitHub data with {len(github_data)} repositories")
        
        # Sample query to test
        query = "arithmetic logic unit ALU implementation"
        top_k = 2
        
        print(f"\nSearching for: '{query}'")
        print(f"Top {top_k} results:")
        
        # Search for GitHub READMEs
        results = search_github_readmes(query, github_data, top_k)
        
        # Display results
        for i, result in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(f"Repository: {result.repo_name}")
            print(f"Description: {result.repo_info.get('description', 'N/A')}")
            print(f"Languages: {', '.join(result.repo_info.get('languages', []))}")
            print(f"Stars: {result.repo_info.get('stars', 0)}")
            print(f"Similarity Score: {result.similarity_score:.4f}")
            
            # Display a snippet of the README
            readme_snippet = result.readme_content[:200] + "..." if len(result.readme_content) > 200 else result.readme_content
            print(f"\nREADME Snippet:\n{readme_snippet}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

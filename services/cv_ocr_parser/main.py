#!/usr/bin/env python3
"""
Test script for CV parser service.
This script demonstrates how to use the CV parser to extract information from a CV file.
"""

import os
import sys
import json
from document_parser import parse_document

def main():
    # Location of the sample CV
    sample_cv_path = os.path.join(os.path.dirname(__file__), "mikawi_CV.pdf")
    
    # Bucket directory for output
    bucket_dir = "/Users/mikawi/Developer/hackathon/g2scv_n/bucket"
    
    # Ensure bucket directory exists
    os.makedirs(bucket_dir, exist_ok=True)
    
    print(f"Parsing CV: {sample_cv_path}")
    
    # Parse the CV and save result to bucket
    parse_document(sample_cv_path, bucket_dir=bucket_dir)

if __name__ == "__main__":
    main()

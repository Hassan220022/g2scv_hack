#!/usr/bin/env python3
"""
CLI utility for document parsing.
Extract text, metadata, and hyperlinks from various file formats.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Optional

from document_parser import parse_document

def batch_process(
    files: List[str], 
    output_dir: Optional[str] = None, 
    verbose: bool = False
):
    """Process multiple files."""
    results = []
    
    # Create output directory if needed
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    for file_path in files:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
        
        print(f"Processing: {file_path}")
        
        # Determine output path
        output_path = None
        if output_dir:
            output_path = Path(output_dir) / f"{file_path.stem}.json"
        
        # Parse the document
        try:
            result = parse_document(file_path, output_path)
            
            # Print summary
            if verbose:
                print(f"  Type: {result.get('type', 'unknown')}")
                print(f"  Size: {result.get('file_info', {}).get('size_bytes', 0)} bytes")
                print(f"  Content Length: {len(result.get('content', ''))}")
                print(f"  Hyperlinks: {len(result.get('hyperlinks', []))}")
                print(f"  Emails: {len(result.get('emails', []))}")
                if output_path:
                    print(f"  Output: {output_path}")
                print()
            
            results.append({
                "file": str(file_path),
                "success": True,
                "output": str(output_path) if output_path else None
            })
            
        except Exception as e:
            print(f"  Error: {str(e)}")
            results.append({
                "file": str(file_path),
                "success": False,
                "error": str(e)
            })
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Extract text, metadata, and hyperlinks from documents"
    )
    parser.add_argument(
        "files", 
        nargs="+", 
        help="Paths to files to process"
    )
    parser.add_argument(
        "-o", "--output-dir", 
        help="Directory to save output JSON files"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Print detailed information"
    )
    parser.add_argument(
        "-s", "--summary-file", 
        help="Save processing summary to JSON file"
    )
    
    args = parser.parse_args()
    
    # Process files
    results = batch_process(args.files, args.output_dir, args.verbose)
    
    # Save summary if requested
    if args.summary_file:
        with open(args.summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Summary saved to {args.summary_file}")
    
    # Print final summary
    successful = sum(1 for r in results if r["success"])
    print(f"\nProcessed {len(results)} files: {successful} successful, {len(results) - successful} failed")
    
    return 0 if all(r["success"] for r in results) else 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
FastAPI server for document parsing.
Provides an API endpoint to upload files and extract text, metadata, and hyperlinks.
"""

import os
import uuid
import shutil
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from document_parser import parse_document

# Create output directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title="Document Parser API",
    description="Extract text, metadata, and hyperlinks from various document formats",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse", response_model=Dict[str, Any])
async def parse_document_api(
    file: UploadFile = File(...),
    save_output: bool = True,
):
    """
    Parse a document to extract text, metadata, and hyperlinks.
    
    Args:
        file: The file to parse
        save_output: Whether to save the output as a JSON file
        
    Returns:
        Dictionary with extracted data
    """
    # Check file size (10MB limit)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 10MB)")
    
    # Create temporary file
    temp_file = None
    try:
        # Save uploaded file to a temporary file
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp_file = temp.name
            shutil.copyfileobj(file.file, temp)

        # Generate output path if needed
        output_path = None
        if save_output:
            output_filename = f"{uuid.uuid4()}.json"
            output_path = OUTPUT_DIR / output_filename
        
        # Parse the document
        result = parse_document(temp_file, output_path if save_output else None)
        
        # Add the output file path to the result
        if save_output:
            result["output_file"] = str(output_path)
        
        return result
    
    except Exception as e:
        raise HTTPException(500, f"Error processing file: {str(e)}")
    
    finally:
        # Clean up the temporary file
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)


@app.get("/", response_class=JSONResponse)
async def root():
    """API status endpoint."""
    return {"status": "ok", "message": "Document Parser API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

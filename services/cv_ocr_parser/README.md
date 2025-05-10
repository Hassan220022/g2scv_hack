# Document Parser & OCR for CV Extraction

A powerful tool for extracting text, metadata, and hyperlinks from various document formats including CVs, resumes, PDFs, images, and Word documents.

## Features

- Supports multiple file formats:
  - PDF documents
  - Images (JPG, PNG, TIFF)
  - Word documents (DOCX)
- Extracts:
  - Full text content with OCR for images
  - Document metadata
  - Hyperlinks and URLs
  - Email addresses
  - File information
- Provides both:
  - Command-line interface
  - REST API (FastAPI)
- Outputs results in JSON format

## Requirements

- Python 3.8+
- Tesseract OCR engine (for image processing)
- ExifTool (for advanced metadata extraction)

## Installation

1. Install system dependencies:

```bash
# macOS
brew install tesseract
brew install exiftool

# Linux
sudo apt-get install tesseract-ocr
sudo apt-get install exiftool
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

Process a single file:

```bash
python cli.py /path/to/document.pdf -o output/
```

Process multiple files:

```bash
python cli.py /path/to/file1.pdf /path/to/file2.docx /path/to/file3.jpg -o output/ -v
```

Options:
- `-o, --output-dir`: Directory to save JSON output files
- `-v, --verbose`: Print detailed information
- `-s, --summary-file`: Save processing summary to JSON file

### API Server

Start the API server:

```bash
python api.py
```

The server will be available at http://localhost:8000

API Endpoints:
- `POST /parse`: Upload and parse a document
- `GET /`: Check API status

Example API request with curl:

```bash
curl -X POST http://localhost:8000/parse \
  -F "file=@/path/to/document.pdf" \
  -F "save_output=true"
```

## Output Format

The parser generates structured JSON output with the following information:

```json
{
  "type": "pdf",
  "content": "Full text content...",
  "metadata": {
    "author": "Jane Doe",
    "created": "2023-01-01",
    "title": "Professional Resume"
  },
  "hyperlinks": [
    "https://linkedin.com/in/janedoe",
    "https://github.com/janedoe"
  ],
  "emails": [
    "jane.doe@example.com"
  ],
  "file_info": {
    "filename": "resume.pdf",
    "path": "/path/to/resume.pdf",
    "size_bytes": 123456,
    "mime_type": "application/pdf",
    "last_modified": "2023-04-28T19:53:21"
  }
}
```

## Python Module Usage

You can also use the document parser as a Python module:

```python
from document_parser import parse_document

# Parse a document and get the result
result = parse_document("/path/to/document.pdf")

# Parse and save to JSON
result = parse_document("/path/to/document.pdf", output_path="output/result.json")
```

## License

MIT

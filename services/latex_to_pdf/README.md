# LaTeX to PDF Converter Service

A microservice that finds LaTeX files in the bucket directory, converts them to PDF format, and saves the PDFs back to the bucket with timestamped filenames.

## Overview

This service scans for `.tex` files in the bucket directory, converts them to PDF format using `pdflatex`, and renames the resulting PDFs with timestamped filenames in the same bucket directory. All auxiliary files created during the process are cleaned up, keeping the bucket directory clean.

## Prerequisites

- Python 3.6 or higher
- LaTeX distribution with `pdflatex` command available:
  - **macOS**: Install [MacTeX](https://www.tug.org/mactex/)
  - **Linux**: `sudo apt-get install texlive-latex-base`
  - **Windows**: Install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)

## Setup

1. Ensure your LaTeX distribution is properly installed and the `pdflatex` command is available
2. No additional Python packages are required beyond the standard library

## Usage

### Basic Usage

1. Place your LaTeX (`.tex`) files in the bucket directory (`/g2scv_n/bucket/`)
2. Run the service:

```bash
cd /path/to/g2scv_n/services/latex_to_pdf
python main.py
```

3. The service will:
   - Find all `.tex` files in the bucket directory
   - Convert them to PDF using `pdflatex`
   - Rename the PDFs with timestamped filenames (e.g., `filename_YYYYMMDD_HHMMSS.pdf`)
   - Clean up all temporary files created during the conversion process

### Output

- Converted PDFs will be saved to `/g2scv_n/bucket/` with filenames in the format:
  - `original_filename_YYYYMMDD_HHMMSS.pdf`
- Log messages will be displayed in the console showing the progress

## How It Works

1. The service scans for all `.tex` files in the bucket directory
2. For each LaTeX file:
   - Runs `pdflatex` (twice to resolve all references)
   - Renames the generated PDF with a timestamp in the filename
   - Cleans up all temporary files (`.aux`, `.log`, etc.)
   - Logs the process with information about success or failure

## Troubleshooting

### No PDF Generated

- Verify that `pdflatex` is properly installed and available in your PATH
- Check the LaTeX file for compilation errors
- Examine the logs for specific error messages

### Permission Issues

- Ensure you have write permissions to both the service directory and the bucket directory

## Integrating with Other Services

This service is designed to work with other microservices in the system:

1. Other services can place `.tex` files directly in the bucket directory
2. Run this service to process all LaTeX files in the bucket
3. The PDFs will be available in the same bucket directory with timestamped filenames
4. Other services can then use these generated PDFs as needed

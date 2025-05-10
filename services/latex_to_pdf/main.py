import os
import subprocess
import logging
import time
import shutil
import glob
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('latex_to_pdf')

BUCKET_DIR = "/Users/mikawi/Developer/hackathon/g2scv_n/bucket"

# This is where we'll look for LaTeX files to convert
SOURCE_DIR = BUCKET_DIR

def ensure_dir_exists(directory):
    """Ensure the given directory exists."""
    os.makedirs(directory, exist_ok=True)

def convert_latex_to_pdf(latex_file_path):
    """
    Convert a LaTeX file to PDF using pdflatex.
    
    Args:
        latex_file_path (str): Path to the LaTeX file
        
    Returns:
        str: Path to the generated PDF file or None if conversion failed
    """
    if not os.path.exists(latex_file_path):
        logger.error(f"LaTeX file not found: {latex_file_path}")
        return None
    
    # Get the directory and filename
    file_dir = os.path.dirname(latex_file_path)
    file_name = os.path.basename(latex_file_path)
    file_base = os.path.splitext(file_name)[0]
    
    # Construct the output PDF path
    output_pdf_path = os.path.join(file_dir, f"{file_base}.pdf")
    
    # Run pdflatex twice to ensure all references are resolved
    for _ in range(2):
        try:
            logger.info(f"Running pdflatex on {latex_file_path}")
            process = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', latex_file_path],
                cwd=file_dir,
                capture_output=True,
                text=True,
                check=False
            )
            
            if process.returncode != 0:
                logger.error(f"pdflatex failed: {process.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error running pdflatex: {e}")
            return None
    
    # Check if PDF was generated
    if not os.path.exists(output_pdf_path):
        logger.error(f"PDF file not generated: {output_pdf_path}")
        return None
    
    return output_pdf_path

def save_pdf_to_bucket(pdf_path):
    """
    Rename the PDF file with a timestamp in the bucket directory.
    Since we're already working in the bucket directory, this just renames the file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Path to the saved PDF in the bucket with timestamp
    """
    ensure_dir_exists(BUCKET_DIR)
    
    # Generate a timestamped filename
    file_name = os.path.basename(pdf_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bucket_filename = f"{os.path.splitext(file_name)[0]}_{timestamp}.pdf"
    bucket_path = os.path.join(BUCKET_DIR, bucket_filename)
    
    # Since we're already working in the bucket, just rename the file
    try:
        # If the files are on different filesystems, copy then delete
        if os.path.dirname(pdf_path) != BUCKET_DIR:
            shutil.copy2(pdf_path, bucket_path)
        else:
            # Otherwise just rename
            os.rename(pdf_path, bucket_path)
            
        logger.info(f"PDF saved with timestamp: {bucket_path}")
        return bucket_path
    except Exception as e:
        logger.error(f"Error saving PDF with timestamp: {e}")
        return None

def cleanup_auxiliary_files(latex_file_path, remove_pdf=False):
    """
    Clean up all auxiliary files created during LaTeX compilation.
    
    Args:
        latex_file_path (str): Path to the LaTeX file
        remove_pdf (bool): Whether to also remove the generated PDF file
    """
    file_dir = os.path.dirname(latex_file_path)
    file_base = os.path.splitext(os.path.basename(latex_file_path))[0]
    
    # List of common LaTeX auxiliary file extensions to remove
    extensions_to_remove = [
        '.aux', '.log', '.out', '.toc', '.lof', '.lot', '.bbl', '.blg',
        '.fls', '.fdb_latexmk', '.synctex.gz', '.dvi', '.nav', '.snm',
        '.vrb', '.bcf', '.run.xml', '.idx', '.ilg', '.ind', '.ist'
    ]
    
    # Also remove PDF if requested
    if remove_pdf:
        extensions_to_remove.append('.pdf')
    
    # Remove all auxiliary files
    for ext in extensions_to_remove:
        aux_files = glob.glob(os.path.join(file_dir, f"*{ext}"))
        for aux_file in aux_files:
            try:
                os.remove(aux_file)
                if ext == '.pdf':
                    logger.info(f"Removed PDF file: {aux_file}")
                else:
                    logger.debug(f"Removed auxiliary file: {aux_file}")
            except Exception as e:
                logger.warning(f"Failed to remove {aux_file}: {e}")

def process_latex_file(latex_file_path):
    """
    Process a LaTeX file: convert to PDF and save to bucket.
    
    Args:
        latex_file_path (str): Path to the LaTeX file
        
    Returns:
        str: Path to the PDF in the bucket or None if processing failed
    """
    logger.info(f"Processing LaTeX file: {latex_file_path}")
    
    # Convert LaTeX to PDF
    pdf_path = convert_latex_to_pdf(latex_file_path)
    if not pdf_path:
        return None
    
    # Save PDF to bucket
    bucket_path = save_pdf_to_bucket(pdf_path)
    
    # Clean up auxiliary files including the PDF file
    cleanup_auxiliary_files(latex_file_path, remove_pdf=False)
    
    return bucket_path

def main():
    """Main function to process all LaTeX files in the bucket directory."""
    
    # Ensure bucket directory exists
    ensure_dir_exists(BUCKET_DIR)
    
    # Process all .tex files in the bucket directory
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith('.tex'):
            latex_file_path = os.path.join(SOURCE_DIR, filename)
            bucket_path = process_latex_file(latex_file_path)
            
            if bucket_path:
                logger.info(f"Successfully processed {filename} to {bucket_path}")
            else:
                logger.error(f"Failed to process {filename}")

if __name__ == "__main__":
    main()

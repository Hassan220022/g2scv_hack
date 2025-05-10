#!/usr/bin/env python3
"""
Document Parser - Extract text, metadata, and hyperlinks from various file formats.
Supports PDF, Word Documents, Images, and more.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime

# PDF processing
import PyPDF2
import pdfplumber

# Image processing
from PIL import Image, ExifTags
import pytesseract

# Word document processing
from docx import Document as DocxDocument

# File type detection
import magic

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
URL_PATTERN = r'\b(?:https?://|www\.)\S+\b'
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class DocumentParser:
    """Main document parser class that handles different file types."""
    
    def __init__(self, file_path: str):
        """Initialize with file path."""
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.mime_type = self._get_mime_type()
        self.parser_func = self._get_parser_function()
        
    def _get_mime_type(self) -> str:
        """Determine MIME type of the file."""
        mime = magic.Magic(mime=True)
        return mime.from_file(str(self.file_path))
    
    def _get_parser_function(self):
        """Get the appropriate parser function based on MIME type."""
        mime_mapping = {
            'application/pdf': self._parse_pdf,
            'image/jpeg': self._parse_image,
            'image/png': self._parse_image,
            'image/tiff': self._parse_image,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': self._parse_docx,
        }
        
        # Check by extension as fallback
        ext_mapping = {
            '.pdf': self._parse_pdf,
            '.jpg': self._parse_image,
            '.jpeg': self._parse_image,
            '.png': self._parse_image,
            '.tiff': self._parse_image,
            '.tif': self._parse_image,
            '.docx': self._parse_docx,
        }
        
        parser = mime_mapping.get(self.mime_type)
        if not parser:
            # Fallback to extension
            parser = ext_mapping.get(self.file_path.suffix.lower())
            
        if not parser:
            raise ValueError(f"Unsupported file type: {self.mime_type} with extension {self.file_path.suffix}")
            
        return parser
    
    def parse(self) -> Dict[str, Any]:
        """Parse the document and return structured data."""
        try:
            result = self.parser_func()
            # Add common metadata
            result["file_info"] = {
                "filename": self.file_path.name,
                "path": str(self.file_path),
                "size_bytes": self.file_path.stat().st_size,
                "mime_type": self.mime_type,
                "last_modified": datetime.fromtimestamp(self.file_path.stat().st_mtime).isoformat(),
            }
            return result
        except Exception as e:
            logger.error(f"Error parsing document: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "file_info": {
                    "filename": self.file_path.name,
                    "path": str(self.file_path),
                }
            }
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text."""
        if not text:
            return []
        return list(set(re.findall(URL_PATTERN, text)))
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text."""
        if not text:
            return []
        return list(set(re.findall(EMAIL_PATTERN, text)))
    
    def _get_exif_metadata(self) -> Dict[str, Any]:
        """Extract EXIF metadata using Pillow."""
        try:
            if self.file_path.suffix.lower() not in ['.jpg', '.jpeg', '.tiff', '.tif']:
                return {}
                
            with Image.open(self.file_path) as img:
                if not hasattr(img, '_getexif') or img._getexif() is None:
                    return {}
                    
                exif_data = {}
                for tag, value in img._getexif().items():
                    if tag in ExifTags.TAGS:
                        tag_name = ExifTags.TAGS[tag]
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8')
                            except UnicodeDecodeError:
                                value = str(value)
                        exif_data[tag_name] = value
                return exif_data
        except Exception as e:
            logger.warning(f"Error extracting EXIF metadata: {str(e)}")
            return {}
    
    def _parse_pdf(self) -> Dict[str, Any]:
        """Parse PDF files."""
        result = {
            "type": "pdf",
            "content": "",
            "metadata": {},
            "pages": [],
            "hyperlinks": [],
        }
        
        # Extract text and links with pdfplumber
        try:
            with pdfplumber.open(self.file_path) as pdf:
                # Get document metadata
                if hasattr(pdf, 'metadata') and pdf.metadata:
                    result["metadata"] = {k: v for k, v in pdf.metadata.items() if v}
                
                # Process each page
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text() or ""
                    page_data = {
                        "page_number": i + 1,
                        "content": page_text,
                        "links": [],
                    }
                    
                    # Extract links from annotations
                    if hasattr(page, 'hyperlinks') and page.hyperlinks:
                        for link in page.hyperlinks:
                            if 'uri' in link:
                                link_data = {
                                    "url": link['uri'],
                                    "page": i + 1,
                                }
                                if 'rect' in link:
                                    link_data["coordinates"] = link['rect']
                                
                                page_data["links"].append(link_data)
                                result["hyperlinks"].append(link['uri'])
                    
                    # Also find URLs in text
                    for url in self._extract_urls(page_text):
                        if url not in result["hyperlinks"]:
                            result["hyperlinks"].append(url)
                    
                    result["pages"].append(page_data)
                    result["content"] += page_text + "\n\n"
        except Exception as e:
            logger.warning(f"Error with pdfplumber: {str(e)}")
            
            # Fallback to PyPDF2
            try:
                with open(self.file_path, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    if pdf.metadata:
                        result["metadata"] = {k.strip('/'): v for k, v in pdf.metadata.items() if v}
                    
                    for i, page in enumerate(pdf.pages):
                        page_text = page.extract_text() or ""
                        result["pages"].append({
                            "page_number": i + 1,
                            "content": page_text,
                            "links": [],
                        })
                        result["content"] += page_text + "\n\n"
                        
                        # Find URLs in text
                        for url in self._extract_urls(page_text):
                            if url not in result["hyperlinks"]:
                                result["hyperlinks"].append(url)
            except Exception as e2:
                logger.error(f"Error with PyPDF2 fallback: {str(e2)}")
                
        # Clean up content
        result["content"] = result["content"].strip()
        result["emails"] = self._extract_emails(result["content"])
        
        return result
    
    def _parse_image(self) -> Dict[str, Any]:
        """Parse image files using OCR."""
        result = {
            "type": "image",
            "content": "",
            "metadata": self._get_exif_metadata(),
            "hyperlinks": [],
        }
        
        try:
            # Perform OCR
            img = Image.open(self.file_path)
            result["image_info"] = {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
            }
            
            # Extract text via OCR
            text = pytesseract.image_to_string(img)
            result["content"] = text
            
            # Extract URLs and emails
            result["hyperlinks"] = self._extract_urls(text)
            result["emails"] = self._extract_emails(text)
            
        except Exception as e:
            logger.error(f"Error parsing image: {str(e)}")
            result["error"] = str(e)
            
        return result
    
    def _parse_docx(self) -> Dict[str, Any]:
        """Parse Word documents (.docx)."""
        result = {
            "type": "docx",
            "content": "",
            "metadata": {},
            "hyperlinks": [],
        }
        
        try:
            doc = DocxDocument(self.file_path)
            
            # Extract core properties
            if hasattr(doc, 'core_properties'):
                props = doc.core_properties
                metadata = {}
                for prop in ['author', 'category', 'comments', 'content_status', 
                            'created', 'identifier', 'keywords', 'language', 
                            'last_modified_by', 'last_printed', 'modified', 
                            'revision', 'subject', 'title', 'version']:
                    if hasattr(props, prop):
                        value = getattr(props, prop)
                        if value:
                            if isinstance(value, datetime):
                                metadata[prop] = value.isoformat()
                            else:
                                metadata[prop] = str(value)
                result["metadata"] = metadata
            
            # Extract text content
            paragraphs = []
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
            result["content"] = "\n".join(paragraphs)
            
            # Extract hyperlinks from relationships
            rels = doc.part.rels
            for rel in rels.values():
                if rel.is_external:
                    target = rel.target_ref
                    if target.startswith('http'):
                        result["hyperlinks"].append(target)
            
            # Find URLs in text
            for url in self._extract_urls(result["content"]):
                if url not in result["hyperlinks"]:
                    result["hyperlinks"].append(url)
                    
            # Extract emails
            result["emails"] = self._extract_emails(result["content"])
            
        except Exception as e:
            logger.error(f"Error parsing docx: {str(e)}")
            result["error"] = str(e)
            
        return result


def parse_document(file_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse document and optionally save to JSON file.
    
    Args:
        file_path: Path to the document file
        output_path: Optional path to save JSON output
        
    Returns:
        Dictionary with extracted data
    """
    parser = DocumentParser(file_path)
    result = parser.parse()
    
    if output_path:
        output_file = Path(output_path)
        if output_file.suffix != '.json':
            output_file = output_file.with_suffix('.json')
            
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            logger.info(f"Output saved to {output_file}")
    
    return result


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Parse documents and extract text, metadata, and links")
    parser.add_argument("file_path", help="Path to the document file")
    parser.add_argument("-o", "--output", help="Path to save JSON output")
    args = parser.parse_args()
    
    result = parse_document(args.file_path, args.output)
    
    if not args.output:
        # Print to console if no output file specified
        print(json.dumps(result, indent=2, ensure_ascii=False))

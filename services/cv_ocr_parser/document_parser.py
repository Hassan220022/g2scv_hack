#!/usr/bin/env python3
"""
CV Document Parser - Extract structured information, text, metadata, and hyperlinks from various CV formats.
Supports PDF, Word Documents (docx), Images (using OCR), and more.
Extracted data is saved in a structured JSON format in the specified bucket directory.
"""

import os
import re
import json
import uuid
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

# NLP for entity extraction
import spacy
try:
    nlp = spacy.load('en_core_web_sm')
except:
    # Fallback for when spaCy model isn't available
    nlp = None
    logging.warning("spaCy model not available. Entity extraction will be limited.")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
URL_PATTERN = r'\b(?:https?://|www\.)\S+\b'
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PHONE_PATTERN = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
LINKEDIN_PATTERN = r'(?:linkedin\.com/(?:in|company)/[\w-]+)'
GITHUB_PATTERN = r'(?:github\.com/[\w-]+)'

# CV sections - common section titles in resumes/CVs
CV_SECTIONS = [
    'education', 'experience', 'work experience', 'employment', 'skills', 
    'technical skills', 'projects', 'certifications', 'achievements',
    'languages', 'summary', 'objective', 'professional summary', 'profile',
    'publications', 'references', 'volunteer', 'interests', 'awards'
]


class DocumentParser:
    """Main document parser class that handles different CV file types and extracts structured information."""
    
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
            'text/plain': self._parse_text,
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
            '.txt': self._parse_text,
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
    
    def _extract_phones(self, text: str) -> List[str]:
        """Extract phone numbers from text."""
        if not text:
            return []
        return list(set(re.findall(PHONE_PATTERN, text)))
    
    def _extract_linkedin(self, text: str) -> List[str]:
        """Extract LinkedIn profiles from text."""
        if not text:
            return []
        profiles = re.findall(LINKEDIN_PATTERN, text)
        # Also check in the URLs
        urls = self._extract_urls(text)
        for url in urls:
            if 'linkedin.com/' in url:
                profiles.append(url)
        return list(set(profiles))
    
    def _extract_github(self, text: str) -> List[str]:
        """Extract GitHub profiles from text."""
        if not text:
            return []
        profiles = re.findall(GITHUB_PATTERN, text)
        # Also check in the URLs
        urls = self._extract_urls(text)
        for url in urls:
            if 'github.com/' in url:
                profiles.append(url)
        return list(set(profiles))
    
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
    
    def _parse_text(self) -> Dict[str, Any]:
        """Parse plain text files."""
        result = {
            "type": "text",
            "content": "",
            "metadata": {
                "filename": self.file_path.name,
                "extension": self.file_path.suffix,
                "size": self.file_path.stat().st_size
            },
            "paragraphs": [],
            "hyperlinks": [],
        }
        
        try:
            # Read the text file
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            result["content"] = content
            
            # Split into paragraphs (separated by blank lines)
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            result["paragraphs"] = paragraphs
            
            # Extract URLs
            result["hyperlinks"] = self._extract_urls(content)
            
            return result
        except Exception as e:
            logger.error(f"Error parsing text file: {str(e)}")
            result["error"] = str(e)
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


    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text using spaCy if available."""
        entities = {
            "PERSON": [],
            "ORG": [],
            "GPE": [],  # Geo-Political Entity (cities, countries)
            "DATE": [],
            "DEGREE": []
        }
        
        if not text or not nlp:
            return entities
            
        doc = nlp(text)
        
        # Extract standard named entities
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
                
        # Look for educational degrees with pattern matching
        degree_patterns = [
            r'\b(?:Bachelor|Master|Doctor|PhD|BSc|BA|MS|MSc|MBA|MD|B\.S|M\.S|Ph\.D)\b[\s\w]*(?:degree|of Science|of Arts|of Business|in [\w\s]+)'
        ]
        
        for pattern in degree_patterns:
            degrees = re.findall(pattern, text, re.IGNORECASE)
            if degrees:
                entities["DEGREE"].extend(degrees)
                
        # Deduplicate
        for key in entities:
            entities[key] = list(set(entities[key]))
            
        return entities
    
    def _extract_cv_sections(self, text: str) -> Dict[str, str]:
        """Attempt to extract common CV sections based on headings."""
        sections = {}
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line looks like a section heading
            is_heading = False
            line_lower = line.lower()
            
            for section_name in CV_SECTIONS:
                if section_name in line_lower and len(line) < 50:  # Avoid matching long lines
                    # Found a new section
                    if current_section:
                        sections[current_section] = '\n'.join(section_content)
                    current_section = line
                    section_content = []
                    is_heading = True
                    break
            
            if not is_heading and current_section:
                section_content.append(line)
        
        # Add the last section
        if current_section:
            sections[current_section] = '\n'.join(section_content)
            
        return sections


def parse_document(file_path: str, output_path: Optional[str] = None, bucket_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse CV document and save to JSON file in the specified bucket directory.
    
    Args:
        file_path: Path to the CV document file
        output_path: Optional explicit path to save JSON output
        bucket_dir: Optional bucket directory path to save output
        
    Returns:
        Dictionary with extracted structured CV data
    """
    parser = DocumentParser(file_path)
    result = parser.parse()
    
    # Extract additional CV-specific information
    text_content = result.get("content", "")
    
    # Add contact information
    result["contact_info"] = {
        "emails": parser._extract_emails(text_content),
        "phones": parser._extract_phones(text_content),
        "linkedin": parser._extract_linkedin(text_content),
        "github": parser._extract_github(text_content)
    }
    
    # Add named entities
    result["entities"] = parser._extract_entities(text_content)
    
    # Add structured sections
    result["cv_sections"] = parser._extract_cv_sections(text_content)
    
    # Generate a timestamp-based filename if not provided
    if not output_path and bucket_dir:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cv_parsed_{os.path.basename(file_path).split('.')[0]}_{timestamp}.json"
        output_path = os.path.join(bucket_dir, filename)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # Add the output path to the result
        result["output_file"] = output_path
            
    return result


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CV Parser: Extract structured information from CVs/Resumes")
    parser.add_argument("file", help="Path to the CV document file")
    parser.add_argument("-o", "--output", help="Path to save JSON output")
    parser.add_argument("-b", "--bucket", default="/Users/mikawi/Developer/hackathon/g2scv_n/bucket", 
                        help="Path to bucket directory for storing results")
    
    args = parser.parse_args()
    
    # Ensure bucket directory exists
    os.makedirs(args.bucket, exist_ok=True)
    
    # Parse document and save to bucket
    result = parse_document(args.file, args.output, args.bucket)
    print(f"Parsed CV: {args.file}")
    
    output_location = args.output if args.output else result.get("output_file")
    if output_location:
        print(f"Saved output to: {output_location}")
        
    # Print a summary of what was extracted
    print("\nExtracted Information Summary:")
    if "contact_info" in result:
        emails = result["contact_info"].get("emails", [])
        if emails:
            print(f"Emails: {', '.join(emails)}")
            
        phones = result["contact_info"].get("phones", [])
        if phones:
            print(f"Phone Numbers: {', '.join(phones)}")
            
        linkedin = result["contact_info"].get("linkedin", [])
        if linkedin:
            print(f"LinkedIn: {', '.join(linkedin)}")
            
    if "cv_sections" in result:
        print(f"Identified {len(result['cv_sections'])} CV sections")

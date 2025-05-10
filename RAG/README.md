# Advanced RAG System

A powerful Retrieval Augmented Generation (RAG) system for processing multiple file types and providing intelligent responses based on their content.

## Overview

This project implements a comprehensive RAG system using LangChain and OpenAI models. It processes various file types by:

1. Discovering files recursively in directories and subdirectories
2. Processing different file formats (Markdown, JSON, text, and other document types)
3. Splitting content intelligently based on file type (headers for Markdown, chunks for other formats)
4. Creating embeddings using OpenAI's text-embedding-3-small model
5. Storing the vectors in a FAISS index for efficient retrieval
6. Identifying project names from file contents and metadata
7. Retrieving relevant content based on user queries
8. Generating detailed responses with automatic summarization

## Features

- **Multi-format Support**: Processes Markdown, JSON, and other document types
- **Recursive Directory Scanning**: Finds all relevant files in nested directories
- **Intelligent Text Processing**: Uses appropriate splitters for different document types
- **Project Identification**: Automatically extracts project names from files
- **Enhanced Retrieval**: Retrieves more context for comprehensive answers
- **Automatic Summarization**: Includes a concise summary with every response
- **Interactive Mode**: Ask questions directly and get instant answers

## Setup

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone this repository or navigate to the project directory
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # On Unix/Mac
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Install additional dependencies for document processing:
   ```bash
   pip install unstructured python-docx pdf2image pytesseract
   ```
6. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Place your files in a directory (default is `SuzyAdel/`)
2. Run the script:
   ```bash
   python md_rag.py
   ```
3. The script will:
   - Process all files in the specified directory and subdirectories
   - Create or load a vector database
   - Run a sample query to test the system
   - Enter interactive mode where you can ask questions

### Example Queries

- "What projects are described in these files?"
- "List all the projects found in the documents"
- "Tell me about project X"
- "What technologies were used in these projects?"

## Configuration

You can configure the RAG system by modifying parameters in the `main()` function:

- `md_files_dir`: Directory containing files to process (default: "SuzyAdel")
- `model_name`: OpenAI model to use (default: "gpt-4.1-mini")
- `embedding_model`: Embedding model to use (default: "text-embedding-3-small")
- `use_fake_components`: Use fake embeddings and LLM for testing (default: False)

## How It Works

1. **File Discovery**: The system recursively scans for files in the specified directory.
2. **Content Processing**:
   - Markdown files are split by headers and then into chunks
   - JSON files are parsed and converted to structured text
   - Other documents are processed using appropriate loaders
3. **Project Identification**:
   - Extracts project names from README files
   - Identifies project names from headings in content
   - Creates a special project index document
4. **Vector Database Creation**:
   - Creates embeddings for all document chunks
   - Stores them in a FAISS vector database
5. **Querying**:
   - Retrieves the most relevant chunks for a query
   - Provides context to the LLM
   - Generates comprehensive responses with summaries

## Extensions

The system can be extended to handle additional file types or to integrate with other data sources. The modular design allows for easy customization and enhancement.

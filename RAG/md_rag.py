import os
import glob
import json
from typing import List, Dict, Any

from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredFileLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
# Replace OpenAI embeddings with mock
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS
# Replace OpenAI LLM with fake
from langchain_community.llms.fake import FakeListLLM
# Actual OpenAI components (imported at top level to satisfy linters if package is installed)
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Import the dotenv loader
from dotenv_loader import load_env_vars, check_openai_api_key

class MarkdownRAG:
    """
    Retrieval Augmented Generation system for files.
    This class loads various file types, processes them, creates embeddings,
    and provides a query interface for retrieving relevant content.
    """
    
    def __init__(
        self,
        md_files_dir: str = "files",
        model_name: str = "gpt-4.1-mini",
        embedding_model: str = "text-embedding-3-small",
        vector_db_path: str = "faiss_index",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        use_fake_components: bool = True  # Added parameter for testing
    ):
        """
        Initialize the RAG system.
        
        Args:
            md_files_dir: Directory containing files to process
            model_name: OpenAI model to use for generation
            embedding_model: OpenAI embedding model to use
            vector_db_path: Path to save the vector database
            chunk_size: Size of chunks for text splitting
            chunk_overlap: Overlap between chunks for text splitting
            use_fake_components: Whether to use fake embeddings and LLM for testing
        """
        self.md_files_dir = md_files_dir
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.vector_db_path = vector_db_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.use_fake_components = use_fake_components
        
        self.vector_db = None
        self.llm = None
        self.retrieval_chain = None
        
    def load_and_process_files(self) -> List[Document]:
        """
        Load and process all files from the specified directory and all subdirectories.
        
        Returns:
            List of processed document chunks
        """
        # Check if the directory exists
        if not os.path.exists(self.md_files_dir):
            print(f"Directory {self.md_files_dir} does not exist. Creating it.")
            os.makedirs(self.md_files_dir)
            return []
        
        # Get all files in the directory and all subdirectories
        all_files = []
        for root, dirs, files in os.walk(self.md_files_dir):
            for file in files:
                all_files.append(os.path.join(root, file))
        
        print(f"Found {len(all_files)} files in {self.md_files_dir} and its subdirectories")
        
        # Add the main README.md file to the list of files to process
        main_readme_path = os.path.join(os.path.dirname(__file__), "README.md")
        if os.path.exists(main_readme_path):
            print(f"Including main README: {main_readme_path}")
            all_files.append(main_readme_path)
            
        if not all_files:
            print(f"No files found in {self.md_files_dir} or project root")
            return []

        print(f"Processing {len(all_files)} files in total")
        
        # Define headers to split on for markdown files
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 5"),
            ("######", "Header 6"),
        ]
        
        # Create the markdown splitter
        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=False
        )
        
        # Create a recursive character splitter for further chunking if needed
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        all_docs = []
        project_names = set()  # To collect project names during processing
        
        # Process each file
        for file_path in all_files:
            try:
                file_extension = os.path.splitext(file_path)[1].lower()
                file_name = os.path.basename(file_path)
                
                # Try to identify project name from README filenames
                if file_name.endswith('_README.md') or file_name == 'README.md':
                    project_name = file_name.replace('_README.md', '').replace('README.md', '')
                    if project_name:
                        project_names.add(project_name)
                
                # Process based on file type
                if file_extension == '.md':
                    # Process markdown files
                    with open(file_path, 'r', encoding='utf-8') as f:
                        md_content = f.read()
                    
                    # First split by headers
                    md_header_splits = md_splitter.split_text(md_content)
                    
                    # Further split the header-based chunks if they're too large
                    chunks = text_splitter.split_documents(md_header_splits)
                    
                    # Add project identification metadata to each chunk
                    for chunk in chunks:
                        # Extract potential project names from headers
                        content = chunk.page_content
                        if '# ' in content or '## ' in content:
                            lines = content.split('\n')
                            for line in lines:
                                if line.startswith('# ') or line.startswith('## '):
                                    potential_project = line.replace('# ', '').replace('## ', '').strip()
                                    if len(potential_project) > 3 and len(potential_project) < 50:
                                        project_names.add(potential_project)
                                        chunk.metadata["project"] = potential_project
                        
                        chunk.metadata["source"] = os.path.basename(file_path)
                    
                elif file_extension == '.json':
                    # Process JSON files
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_content = json.load(f)
                    
                    # Convert JSON to string for processing
                    json_str = json.dumps(json_content, indent=2)
                    
                    # Create document from JSON string
                    doc = Document(page_content=json_str, metadata={"source": file_path})
                    
                    # Split into chunks
                    chunks = text_splitter.split_documents([doc])
                    
                    # Check if this is a repositories json file
                    if 'repositories' in file_name.lower() or 'projects' in file_name.lower():
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                json_content = json.load(f)
                                
                                # Try to extract project names from the JSON
                                if isinstance(json_content, list):
                                    for item in json_content:
                                        if isinstance(item, dict):
                                            if 'name' in item:
                                                project_names.add(item['name'])
                                            if 'project' in item:
                                                project_names.add(item['project'])
                        except Exception as e:
                            print(f"Error extracting project names from JSON {file_path}: {e}")
                    
                    for chunk in chunks:
                        chunk.metadata["source"] = os.path.basename(file_path)
                    
                else:
                    # For other file types, use the UnstructuredFileLoader
                    try:
                        loader = UnstructuredFileLoader(file_path)
                        docs = loader.load()
                        
                        # Split into chunks
                        chunks = text_splitter.split_documents(docs)
                    except Exception as e:
                        print(f"Error loading {file_path} with UnstructuredFileLoader: {e}")
                        # Fallback to treating as plain text
                        try:
                            loader = TextLoader(file_path, encoding='utf-8')
                            docs = loader.load()
                            chunks = text_splitter.split_documents(docs)
                        except Exception as e2:
                            print(f"Error loading {file_path} as text: {e2}")
                            continue
                
                all_docs.extend(chunks)
                
                print(f"Processed {file_path} into {len(chunks)} chunks")
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Create a special document that lists all project names
        if project_names:
            project_list = "# All Identified Projects\n\n"
            for i, name in enumerate(sorted(project_names), 1):
                project_list += f"{i}. {name}\n"
            
            project_doc = Document(
                page_content=project_list,
                metadata={"source": "project_index", "special": "project_list"}
            )
            all_docs.append(project_doc)
            print(f"Created project index with {len(project_names)} identified projects")
        
        return all_docs
    
    def create_vector_db(self, docs: List[Document]) -> None:
        """
        Create a vector database from the processed documents.
        
        Args:
            docs: List of document chunks to embed
        """
        if not docs:
            print("No documents to create embeddings from")
            return
        
        print(f"Creating embeddings for {len(docs)} documents")
        
        # Create embeddings
        if self.use_fake_components:
            # Use fake embeddings for testing (no API key needed)
            embeddings = FakeEmbeddings(size=1536)  # Same size as OpenAI embeddings
            print("Using fake embeddings for testing")
        else:
            # Use OpenAI embeddings
            embeddings = OpenAIEmbeddings(model=self.embedding_model)
        
        # Create vector store
        self.vector_db = FAISS.from_documents(docs, embeddings)
        
        # Save the vector store
        self.vector_db.save_local(self.vector_db_path)
        
        print(f"Vector database created and saved to {self.vector_db_path}")
    
    def load_vector_db(self) -> bool:
        """
        Load the vector database from disk if it exists.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        if not os.path.exists(self.vector_db_path):
            print(f"Vector database at {self.vector_db_path} does not exist")
            return False
        
        try:
            if self.use_fake_components:
                # Use fake embeddings for testing (no API key needed)
                embeddings = FakeEmbeddings(size=1536)
                print("Using fake embeddings for testing")
            else:
                # Use OpenAI embeddings
                embeddings = OpenAIEmbeddings(model=self.embedding_model)
                
            self.vector_db = FAISS.load_local(
                self.vector_db_path, 
                embeddings, 
                allow_dangerous_deserialization=True  # Add this parameter to allow loading the pickled database
            )
            print(f"Vector database loaded from {self.vector_db_path}")
            return True
        except Exception as e:
            print(f"Error loading vector database: {e}")
            return False
    
    def setup_retrieval_chain(self) -> None:
        """
        Set up the retrieval chain for querying.
        """
        if not self.vector_db:
            print("Vector database not initialized. Please create or load it first.")
            return
        
        # Initialize the language model
        if self.use_fake_components:
            # Use fake LLM for testing (no API key needed)
            responses = [
                "This is a test response based on the documents retrieved. "
                "I'm a fake LLM being used for testing purposes without needing an API key. "
                "In real usage, this would be a response generated by GPT based on the retrieved documents."
            ]
            self.llm = FakeListLLM(responses=responses)
            print("Using fake LLM for testing")
        else:
            # Use OpenAI LLM
            self.llm = ChatOpenAI(model_name=self.model_name)
        
        # Create a retriever from the vector database
        retriever = self.vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10}  # Increase from 5 to 10 chunks for more comprehensive retrieval
        )
        
        # Define the prompt template with enhanced instructions for thorough responses
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful assistant that generates detailed responses based on the provided content.
        
        When asked about projects, repositories, or work items, be extremely thorough and list ALL instances found in the context, 
        even if they seem minor. Never say you don't know if there's any relevant information in the context.
        If you're asked to list all projects, make an exhaustive effort to identify every project name, repository, 
        or significant work mentioned in the context.
        
        Use the following context to answer the user's question. If the information truly isn't 
        in the context provided, say you don't know.
        
        Context:
        {context}
        
        Question:
        {input}
        
        Your response MUST follow this format:
        1. Detailed answer with all relevant information
        2. End with a section titled "SUMMARY:" that provides a concise 2-3 sentence overview of your response
        
        Answer (be comprehensive and detailed):
        """)
        
        # Create the document chain
        document_chain = create_stuff_documents_chain(self.llm, prompt)
        
        # Create the retrieval chain
        self.retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        print("Retrieval chain set up successfully")
    
    def query(self, query_text: str) -> Dict[str, Any]:
        """
        Query the RAG system with a question.
        
        Args:
            query_text: The question to ask
            
        Returns:
            The response from the system
        """
        if not self.retrieval_chain:
            self.setup_retrieval_chain()
        
        if not self.retrieval_chain:
            return {"answer": "System not initialized properly", "context": []}
        
        # Check if the query is about projects or listings
        project_related_keywords = ["projects", "repositories", "list", "name all", "enumerate", "repositories"]
        is_project_query = any(keyword in query_text.lower() for keyword in project_related_keywords)
        
        # Use the enhanced prompt for project listings
        response = self.retrieval_chain.invoke({"input": query_text})
        
        answer = response.get("answer", "No answer found")
        
        # Ensure there's a summary if not already present
        if "SUMMARY:" not in answer:
            answer += "\n\nSUMMARY: This response addresses the query about " + query_text[:30] + "... Please refer to the details above for complete information."
        
        # Extract and format the source documents for context
        context_docs = []
        if "context" in response:
            for doc in response["context"]:
                context_docs.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
        
        return {
            "answer": answer,
            "context": context_docs
        }
    
    def process_and_initialize(self) -> None:
        """
        Process files and initialize the RAG system.
        If the vector database already exists, it will be loaded instead.
        """
        # Try to load existing vector database
        if self.load_vector_db():
            # Vector DB loaded, set up the retrieval chain
            self.setup_retrieval_chain()
        else:
            # Vector DB not found, process files and create it
            docs = self.load_and_process_files()
            if docs:
                self.create_vector_db(docs)
                self.setup_retrieval_chain()


def main():
    # Load environment variables
    load_env_vars()
    
    # Check if OpenAI API key is set
    has_valid_api_key = check_openai_api_key()
    
    # Initialize the RAG system
    # If no valid API key, use fake components for testing
    rag = MarkdownRAG(
        md_files_dir="SuzyAdel",
        model_name="gpt-4.1-mini",
        embedding_model="text-embedding-3-small",
        use_fake_components=False  # Use real OpenAI components
    )
    
    # Process files and initialize the system
    rag.process_and_initialize()
    
    # Sample query to test the system
    if rag.retrieval_chain:
        query = "What projects are described in these files?"
        print(f"\nTesting with query: '{query}'")
        response = rag.query(query)
        print("\nResponse:")
        print(response["answer"])
        
        print("\nSources:")
        for i, doc in enumerate(response["context"][:3], 1):  # Show first 3 sources
            print(f"{i}. {doc['metadata']['source']}")
    
    # Interactive mode
    print("\nEnter 'q' to quit")
    while True:
        user_query = input("\nEnter your query: ")
        if user_query.lower() == 'q':
            break
        
        response = rag.query(user_query)
        print("\nResponse:")
        print(response["answer"])
        
        print("\nSources:")
        for i, doc in enumerate(response["context"][:3], 1):  # Show first 3 sources
            print(f"{i}. {doc['metadata']['source']}")


if __name__ == "__main__":
    main() 
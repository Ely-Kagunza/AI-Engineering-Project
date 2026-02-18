#!/usr/bin/env python3
"""
Document ingestion pipeline for RAG system.
Processes documents, creates chunks, generates embeddings, and stores in Chroma.
"""

import os
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any
import hashlib

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import markdown
from bs4 import BeautifulSoup
import PyPDF2
from docx import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Handles document parsing and text extraction."""
    
    def __init__(self):
        self.supported_extensions = {'.md', '.txt', '.pdf', '.docx', '.html'}
    
    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single file and extract text content."""
        try:
            if file_path.suffix.lower() == '.md':
                return self._process_markdown(file_path)
            elif file_path.suffix.lower() == '.txt':
                return self._process_text(file_path)
            elif file_path.suffix.lower() == '.pdf':
                return self._process_pdf(file_path)
            elif file_path.suffix.lower() == '.docx':
                return self._process_docx(file_path)
            elif file_path.suffix.lower() == '.html':
                return self._process_html(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_path}")
                return None
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None
    
    def _process_markdown(self, file_path: Path) -> Dict[str, Any]:
        """Process markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert markdown to HTML then extract text
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        return {
            'source_id': str(file_path),
            'title': file_path.stem.replace('-', ' ').title(),
            'content': text,
            'file_type': 'markdown'
        }
    
    def _process_text(self, file_path: Path) -> Dict[str, Any]:
        """Process plain text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'source_id': str(file_path),
            'title': file_path.stem.replace('-', ' ').title(),
            'content': content,
            'file_type': 'text'
        }
    
    def _process_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Process PDF file."""
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        return {
            'source_id': str(file_path),
            'title': file_path.stem.replace('-', ' ').title(),
            'content': text,
            'file_type': 'pdf'
        }
    
    def _process_docx(self, file_path: Path) -> Dict[str, Any]:
        """Process Word document."""
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        return {
            'source_id': str(file_path),
            'title': file_path.stem.replace('-', ' ').title(),
            'content': text,
            'file_type': 'docx'
        }
    
    def _process_html(self, file_path: Path) -> Dict[str, Any]:
        """Process HTML file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        
        return {
            'source_id': str(file_path),
            'title': file_path.stem.replace('-', ' ').title(),
            'content': text,
            'file_type': 'html'
        }


class TextChunker:
    """Handles text chunking with overlap."""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Split document into overlapping chunks."""
        text = document['content']
        chunks = []
        
        # Simple sentence-aware chunking
        sentences = text.split('. ')
        current_chunk = ""
        chunk_id = 0
        
        for sentence in sentences:
            # Add sentence to current chunk
            test_chunk = current_chunk + sentence + ". "
            
            if len(test_chunk) > self.chunk_size and current_chunk:
                # Save current chunk
                chunks.append(self._create_chunk(
                    document, current_chunk.strip(), chunk_id
                ))
                chunk_id += 1
                
                # Start new chunk with overlap
                overlap_text = self._get_overlap_text(current_chunk)
                current_chunk = overlap_text + sentence + ". "
            else:
                current_chunk = test_chunk
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(self._create_chunk(
                document, current_chunk.strip(), chunk_id
            ))
        
        return chunks
    
    def _create_chunk(self, document: Dict[str, Any], text: str, chunk_id: int) -> Dict[str, Any]:
        """Create a chunk with metadata."""
        chunk_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        
        return {
            'id': f"{document['source_id']}_{chunk_id}_{chunk_hash}",
            'text': text,
            'source_id': document['source_id'],
            'title': document['title'],
            'chunk_id': chunk_id,
            'file_type': document['file_type']
        }
    
    def _get_overlap_text(self, text: str) -> str:
        """Get overlap text from end of current chunk."""
        if len(text) <= self.overlap:
            return text
        return text[-self.overlap:]


class EmbeddingGenerator:
    """Generates embeddings using sentence transformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()


class ChromaDBManager:
    """Manages Chroma vector database operations."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection_name = "company_policies"
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Using existing collection: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Company policies and procedures"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
    
    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Add chunks and embeddings to the collection."""
        ids = [chunk['id'] for chunk in chunks]
        documents = [chunk['text'] for chunk in chunks]
        metadatas = [{
            'source_id': chunk['source_id'],
            'title': chunk['title'],
            'chunk_id': chunk['chunk_id'],
            'file_type': chunk['file_type']
        } for chunk in chunks]
        
        logger.info(f"Adding {len(chunks)} chunks to collection")
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        count = self.collection.count()
        return {
            'total_chunks': count,
            'collection_name': self.collection_name
        }


def main():
    """Main ingestion pipeline."""
    parser = argparse.ArgumentParser(description='Ingest documents for RAG system')
    parser.add_argument('--corpus', required=True, help='Path to corpus directory')
    parser.add_argument('--chunk-size', type=int, default=1000, help='Chunk size in characters')
    parser.add_argument('--overlap', type=int, default=200, help='Overlap size in characters')
    parser.add_argument('--embedding-model', default='all-MiniLM-L6-v2', help='Embedding model name')
    parser.add_argument('--persist-dir', default='./chroma_db', help='Chroma persistence directory')
    
    args = parser.parse_args()
    
    # Initialize components
    processor = DocumentProcessor()
    chunker = TextChunker(chunk_size=args.chunk_size, overlap=args.overlap)
    embedder = EmbeddingGenerator(model_name=args.embedding_model)
    db_manager = ChromaDBManager(persist_directory=args.persist_dir)
    
    # Process documents
    corpus_path = Path(args.corpus)
    if not corpus_path.exists():
        logger.error(f"Corpus directory not found: {corpus_path}")
        return
    
    all_chunks = []
    processed_files = 0
    
    for file_path in corpus_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in processor.supported_extensions:
            logger.info(f"Processing: {file_path}")
            document = processor.process_file(file_path)
            
            if document:
                chunks = chunker.chunk_document(document)
                all_chunks.extend(chunks)
                processed_files += 1
                logger.info(f"Created {len(chunks)} chunks from {file_path}")
    
    if not all_chunks:
        logger.error("No chunks created. Check your corpus directory and file formats.")
        return
    
    # Generate embeddings
    texts = [chunk['text'] for chunk in all_chunks]
    embeddings = embedder.generate_embeddings(texts)
    
    # Store in Chroma
    db_manager.add_chunks(all_chunks, embeddings)
    
    # Print statistics
    stats = db_manager.get_collection_stats()
    logger.info(f"Ingestion complete!")
    logger.info(f"Processed files: {processed_files}")
    logger.info(f"Total chunks: {stats['total_chunks']}")
    logger.info(f"Collection: {stats['collection_name']}")


if __name__ == "__main__":
    main()
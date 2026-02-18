#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) implementation for company policies.
Handles query processing, retrieval, and response generation with citations.
Uses OpenRouter for free LLM access.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import json
import requests

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGSystem:
    """Main RAG system for company policy Q&A."""
    
    def __init__(
        self,
        chroma_persist_dir: str = "./chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "liquid/lfm-2.5-1.2b-instruct:free",
        top_k: int = 5
    ):
        self.top_k = top_k
        self.llm_model = llm_model
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedder = SentenceTransformer(embedding_model)
        
        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=chroma_persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        
        try:
            self.collection = self.client.get_collection("company_policies")
            logger.info("Connected to existing Chroma collection")
        except Exception as e:
            logger.error(f"Failed to connect to Chroma collection: {e}")
            raise
        
        # Initialize OpenRouter client
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.openrouter_api_key:
            logger.error("OPENROUTER_API_KEY not found in environment variables")
            raise ValueError("OpenRouter API key required")
        
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # System prompt for the LLM
        self.system_prompt = """You are a helpful assistant that answers questions about company policies and procedures.

IMPORTANT GUIDELINES:
1. You can ONLY answer questions about the company policies provided in the context below.
2. If a question is not related to company policies, respond with: "I can only answer questions about company policies and procedures. Please ask about topics like PTO, remote work, expenses, security, or employee handbook policies."
3. Always base your answers on the provided context documents.
4. Always include citations in your response using the format [Source: filename].
5. If you cannot find relevant information in the provided context, say "I don't have information about that specific topic in the company policies."
6. Keep responses concise but comprehensive.
7. Use a professional, helpful tone.

Context Documents:
{context}

Question: {question}

Please provide a helpful answer with proper citations."""
    
    def query(self, question: str) -> Dict[str, Any]:
        """Process a user question and return answer with citations."""
        try:
            # Step 1: Retrieve relevant documents
            retrieved_docs = self._retrieve_documents(question)
            
            if not retrieved_docs:
                return {
                    "answer": "I don't have information about that specific topic in the company policies.",
                    "citations": [],
                    "sources": [],
                    "retrieved_chunks": 0
                }
            
            # Step 2: Generate response using LLM
            response = self._generate_response(question, retrieved_docs)
            
            # Step 3: Extract citations and sources
            citations = self._extract_citations(retrieved_docs)
            sources = self._extract_sources(retrieved_docs)
            
            return {
                "answer": response,
                "citations": citations,
                "sources": sources,
                "retrieved_chunks": len(retrieved_docs)
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "answer": "I'm sorry, I encountered an error processing your question. Please try again.",
                "citations": [],
                "sources": [],
                "retrieved_chunks": 0
            }
    
    def _retrieve_documents(self, question: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documents using semantic search."""
        try:
            # Generate query embedding
            query_embedding = self.embedder.encode([question]).tolist()[0]
            
            # Search in Chroma
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=self.top_k,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format results
            retrieved_docs = []
            for i in range(len(results['documents'][0])):
                doc = {
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                }
                retrieved_docs.append(doc)
            
            logger.info(f"Retrieved {len(retrieved_docs)} documents for query")
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def _generate_response(self, question: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Generate response using OpenRouter LLM with retrieved context."""
        try:
            # Format context from retrieved documents
            context_parts = []
            for i, doc in enumerate(retrieved_docs):
                source_info = f"Source: {doc['metadata']['title']} (from {doc['metadata']['source_id']})"
                context_parts.append(f"Document {i+1}:\n{source_info}\n{doc['text']}\n")
            
            context = "\n".join(context_parts)
            
            # Create the prompt
            prompt = self.system_prompt.format(context=context, question=question)
            
            # Prepare request for OpenRouter
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",  # Required by OpenRouter
                "X-Title": "Company Policies RAG"  # Optional, for tracking
            }
            
            data = {
                "model": self.llm_model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant for company policy questions."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.1
            }
            
            # Call OpenRouter API
            response = requests.post(
                self.openrouter_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return "I'm sorry, I encountered an error generating a response. Please try again."
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error generating a response. Please try again."
    
    def _extract_citations(self, retrieved_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract citation information from retrieved documents."""
        citations = []
        for doc in retrieved_docs:
            # Extract filename from source_id path
            source_path = doc['metadata']['source_id']
            filename = source_path.split('/')[-1].split('\\')[-1]  # Handle both / and \
            
            citation = {
                'title': doc['metadata']['title'],
                'source_id': doc['metadata']['source_id'],
                'filename': filename,
                'url': f'/policy/{filename}',
                'chunk_id': doc['metadata']['chunk_id'],
                'snippet': doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text']
            }
            citations.append(citation)
        return citations
    
    def _extract_sources(self, retrieved_docs: List[Dict[str, Any]]) -> List[str]:
        """Extract unique source files from retrieved documents."""
        sources = set()
        for doc in retrieved_docs:
            sources.add(doc['metadata']['source_id'])
        return list(sources)
    
    def health_check(self) -> Dict[str, Any]:
        """Check system health and return status."""
        try:
            # Check Chroma connection
            collection_count = self.collection.count()
            
            # Check OpenRouter API (simple test)
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000"
            }
            
            test_data = {
                "model": self.llm_model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5
            }
            
            test_response = requests.post(
                self.openrouter_url,
                headers=headers,
                json=test_data,
                timeout=10
            )
            
            api_status = "connected" if test_response.status_code == 200 else "error"
            
            return {
                "status": "healthy",
                "chroma_documents": collection_count,
                "llm_model": self.llm_model,
                "embedding_model": "all-MiniLM-L6-v2",
                "openrouter_api": api_status
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }


class QueryValidator:
    """Validates and preprocesses user queries."""
    
    @staticmethod
    def is_policy_related(question: str) -> bool:
        """Check if question is related to company policies."""
        policy_keywords = [
            'policy', 'procedure', 'pto', 'vacation', 'sick leave', 'remote work',
            'expense', 'reimbursement', 'security', 'password', 'employee',
            'handbook', 'benefits', 'holiday', 'time off', 'work from home',
            'travel', 'meal', 'allowance', 'dress code', 'conduct', 'harassment',
            'discrimination', 'termination', 'probation', 'training'
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in policy_keywords)
    
    @staticmethod
    def preprocess_question(question: str) -> str:
        """Clean and preprocess the question."""
        # Remove extra whitespace
        question = ' '.join(question.split())
        
        # Ensure question ends with punctuation
        if not question.endswith(('?', '.', '!')):
            question += '?'
        
        return question


def main():
    """Test the RAG system with sample queries."""
    # Initialize RAG system
    rag = RAGSystem()
    
    # Test queries
    test_queries = [
        "What is the PTO policy?",
        "How many vacation days do I get?",
        "Can I work remotely?",
        "What are the expense reimbursement limits?",
        "What is the password policy?",
        "Tell me about the weather"  # Should be rejected
    ]
    
    print("Testing RAG System")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = rag.query(query)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {len(result['sources'])} documents")
        print(f"Retrieved chunks: {result['retrieved_chunks']}")
        print("-" * 30)


if __name__ == "__main__":
    main()
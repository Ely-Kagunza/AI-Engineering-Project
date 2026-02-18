#!/usr/bin/env python3
"""Test the full RAG system end-to-end."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag import RAGSystem

print("Testing Full RAG System")
print("=" * 50)

try:
    # Initialize RAG system
    print("\n1. Initializing RAG system...")
    rag = RAGSystem()
    print("   ✓ RAG system initialized")
    
    # Test query
    print("\n2. Testing query: 'How many vacation days do I get?'")
    result = rag.query("How many vacation days do I get?")
    
    print(f"\n3. Results:")
    print(f"   Answer: {result['answer'][:200]}...")
    print(f"   Sources: {len(result['sources'])} documents")
    print(f"   Citations: {len(result['citations'])} citations")
    print(f"   Retrieved chunks: {result['retrieved_chunks']}")
    
    if result['answer'] and "error" not in result['answer'].lower():
        print("\n✓ SUCCESS! The system is working correctly!")
        print("\nYou can now start the web application:")
        print("  python app.py")
    else:
        print("\n✗ The system returned an error.")
        print(f"   Error: {result['answer']}")
        sys.exit(1)
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

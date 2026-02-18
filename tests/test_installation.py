#!/usr/bin/env python3
"""Test script to verify installation."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Testing RAG System Installation...")
print("=" * 50)

# Test 1: Import core packages
print("\n1. Testing core package imports...")
try:
    import flask
    import chromadb
    import sentence_transformers
    import requests
    import pandas
    import numpy
    print("   ✓ All core packages imported successfully!")
except ImportError as e:
    print(f"   ✗ Import error: {e}")
    exit(1)

# Test 2: Import project modules
print("\n2. Testing project module imports...")
try:
    from src.ingest import DocumentProcessor, TextChunker
    # Import module but don't instantiate RAGSystem (requires model download)
    import src.rag
    print("   ✓ All project modules imported successfully!")
except ImportError as e:
    print(f"   ✗ Import error: {e}")
    exit(1)

# Test 3: Test document processing
print("\n3. Testing document processing...")
try:
    from pathlib import Path
    processor = DocumentProcessor()
    doc = processor.process_file(Path('policies/employee-handbook.md'))
    print(f"   ✓ Document processed: {doc['title']}")
    print(f"   ✓ Content length: {len(doc['content'])} characters")
except Exception as e:
    print(f"   ✗ Processing error: {e}")
    exit(1)

# Test 4: Test chunking
print("\n4. Testing text chunking...")
try:
    chunker = TextChunker(chunk_size=1000, overlap=200)
    chunks = chunker.chunk_document(doc)
    print(f"   ✓ Created {len(chunks)} chunks")
    print(f"   ✓ First chunk length: {len(chunks[0]['text'])} characters")
except Exception as e:
    print(f"   ✗ Chunking error: {e}")
    exit(1)

# Test 5: Check environment file
print("\n5. Checking environment configuration...")
try:
    from pathlib import Path
    if Path('.env').exists():
        print("   ✓ .env file exists")
        from dotenv import load_dotenv
        import os
        load_dotenv()
        if os.getenv('OPENROUTER_API_KEY'):
            print("   ✓ OPENROUTER_API_KEY is configured")
        else:
            print("   ⚠ OPENROUTER_API_KEY not set in .env file")
            print("   → Copy .env.example to .env and add your API key")
    else:
        print("   ⚠ .env file not found")
        print("   → Copy .env.example to .env and add your API key")
except Exception as e:
    print(f"   ✗ Environment check error: {e}")

# Test 6: Check if Chroma DB exists
print("\n6. Checking Chroma database...")
try:
    from pathlib import Path
    if Path('chroma_db').exists():
        print("   ✓ Chroma database directory exists")
        print("   → Ready to use existing database")
    else:
        print("   ⚠ Chroma database not found")
        print("   → Run: python src/ingest.py --corpus policies/")
except Exception as e:
    print(f"   ✗ Database check error: {e}")

print("\n" + "=" * 50)
print("Installation test complete!")
print("\nNext steps:")
print("1. Get free API key from https://openrouter.ai")
print("2. Copy .env.example to .env and add your API key")
print("3. Run: python src/ingest.py --corpus policies/")
print("4. Run: python app.py")
print("5. Open http://localhost:5000 in your browser")

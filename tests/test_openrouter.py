#!/usr/bin/env python3
"""Test OpenRouter API connection."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL", "microsoft/phi-3-mini-128k-instruct:free")

print(f"Testing OpenRouter API...")
print(f"Model: {model}")
print(f"API Key: {api_key[:10]}..." if api_key else "No API key found")
print()

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:5000",
    "X-Title": "Company Policies RAG Test"
}

data = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Say 'Hello, I am working!' in one sentence."}
    ],
    "max_tokens": 50,
    "temperature": 0.1
}

try:
    print("Sending test request to OpenRouter...")
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    
    if response.status_code == 200:
        result = response.json()
        answer = result['choices'][0]['message']['content']
        print(f"\n✓ Success! Response: {answer}")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(f"Details: {response.text}")
        
except Exception as e:
    print(f"\n✗ Exception: {e}")

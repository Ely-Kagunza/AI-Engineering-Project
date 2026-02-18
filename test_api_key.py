#!/usr/bin/env python3
"""Test OpenRouter API key and diagnose issues."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENROUTER_API_KEY')

if not api_key:
    print("❌ No API key found in .env file")
    exit(1)

print(f"✓ API key found (length: {len(api_key)})")
print(f"✓ Key starts with: {api_key[:10]}...")

# Test 1: Check API key format
if not api_key.startswith('sk-or-v1-'):
    print("⚠️  Warning: API key doesn't start with 'sk-or-v1-'")
    print("   OpenRouter keys should start with 'sk-or-v1-'")

# Test 2: Try to call OpenRouter API
print("\nTesting API connection...")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:5000",
    "X-Title": "API Key Test"
}

# Try a minimal request
data = {
    "model": "liquid/lfm-2.5-1.2b-instruct:free",
    "messages": [
        {"role": "user", "content": "Say 'test' if you can read this."}
    ],
    "max_tokens": 10
}

try:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=10
    )
    
    print(f"\nResponse Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ API key is working!")
        result = response.json()
        print(f"Response: {result['choices'][0]['message']['content']}")
    elif response.status_code == 401:
        print("❌ 401 Unauthorized - API key is invalid or expired")
        print(f"Error: {response.json()}")
        print("\nPossible fixes:")
        print("1. Generate a new API key at https://openrouter.ai/keys")
        print("2. Check if your account needs verification")
        print("3. Ensure you copied the full key without spaces")
    elif response.status_code == 429:
        print("⚠️  429 Rate Limited - You've exceeded the free tier limits")
        print(f"Error: {response.json()}")
        print("\nPossible fixes:")
        print("1. Wait a few minutes and try again")
        print("2. Check your usage at https://openrouter.ai/activity")
        print("3. Consider upgrading or adding credits")
    else:
        print(f"❌ Unexpected error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Connection error: {e}")
    print("\nPossible fixes:")
    print("1. Check your internet connection")
    print("2. Verify OpenRouter.ai is accessible")

print("\n" + "="*50)
print("DIAGNOSIS COMPLETE")
print("="*50)

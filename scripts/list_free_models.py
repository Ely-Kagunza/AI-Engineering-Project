#!/usr/bin/env python3
"""List available free models on OpenRouter."""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

print("Fetching available models from OpenRouter...")
print()

try:
    response = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10
    )
    
    if response.status_code == 200:
        models = response.json()['data']
        
        # Filter for free models
        free_models = [m for m in models if m.get('pricing', {}).get('prompt', '0') == '0']
        
        print(f"Found {len(free_models)} free models:\n")
        
        for model in free_models[:15]:  # Show first 15
            model_id = model['id']
            name = model.get('name', 'Unknown')
            context = model.get('context_length', 'Unknown')
            print(f"  {model_id}")
            print(f"    Name: {name}")
            print(f"    Context: {context}")
            print()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Exception: {e}")

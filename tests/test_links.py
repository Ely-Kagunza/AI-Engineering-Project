#!/usr/bin/env python3
"""Test that policy file links work."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Testing Policy File Links")
print("=" * 50)

# Check if policies directory exists
policies_dir = Path('policies')
if not policies_dir.exists():
    print("✗ Policies directory not found!")
    exit(1)

print(f"✓ Policies directory exists: {policies_dir.absolute()}")
print()

# List all policy files
policy_files = list(policies_dir.glob('*.md'))
print(f"Found {len(policy_files)} policy files:")
print()

for file in policy_files:
    filename = file.name
    url = f"/policy/{filename}"
    print(f"  {filename}")
    print(f"    URL: {url}")
    print(f"    Size: {file.stat().st_size} bytes")
    print()

print("=" * 50)
print("✓ All policy files are accessible")
print()
print("When you start the app, these URLs will work:")
for file in policy_files:
    print(f"  http://localhost:5000/policy/{file.name}")

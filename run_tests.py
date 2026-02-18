#!/usr/bin/env python3
"""
Convenience script to run all tests from the root directory.
"""

import sys
import subprocess
from pathlib import Path

def run_test(test_file):
    """Run a test file and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {test_file}")
    print('='*60)
    
    result = subprocess.run(
        [sys.executable, f"tests/{test_file}"],
        capture_output=False
    )
    
    return result.returncode == 0

def main():
    """Run all tests."""
    print("RAG System Test Suite")
    print("="*60)
    
    tests = [
        "test_installation.py",
        "test_openrouter.py",
        "test_links.py",
        "test_full_system.py"
    ]
    
    results = {}
    for test in tests:
        results[test] = run_test(test)
    
    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print('='*60)
    
    for test, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print(f"\n{'='*60}")
        print("✓ All tests passed!")
        print('='*60)
        return 0
    else:
        print(f"\n{'='*60}")
        print("✗ Some tests failed")
        print('='*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())

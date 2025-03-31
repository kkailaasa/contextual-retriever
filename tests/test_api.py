#!/usr/bin/env python3
"""
API Tester
-----------
Test script for validating the RAG Content Retriever API functionality.
"""

import os
import sys
import time
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
HEADERS = {"X-API-Key": API_KEY} if API_KEY else {}

def print_result(endpoint, response):
    """Print test result"""
    print(f"\n===== {endpoint} =====")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text[:200] + "..." if len(response.text) > 200 else response.text)
    print("-" * 50)

def test_endpoint(method, endpoint, payload=None, expected_status=200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"Testing {method} {endpoint}...")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method.upper() == "POST":
            response = requests.post(url, headers=HEADERS, json=payload)
        else:
            print(f"Unsupported method: {method}")
            return False
            
        print_result(endpoint, response)
        
        if response.status_code == expected_status:
            print(f"✅ Success: {endpoint}")
            return response.json() if response.status_code == 200 else None
        else:
            print(f"❌ Failed: Expected status {expected_status}, got {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def main():
    """Run all API tests"""
    print(f"Testing API at {BASE_URL}")
    print(f"Using API Key: {'Yes' if API_KEY else 'No'}")
    
    # Test the health endpoint (doesn't require API key)
    test_endpoint("GET", "/health")
    
    # Test the readiness endpoint (doesn't require API key)
    test_endpoint("GET", "/readiness")
    
    # Test the liveness endpoint (doesn't require API key)
    test_endpoint("GET", "/liveness")
    
    # The following endpoints require API key
    if not API_KEY:
        print("⚠️ Warning: No API Key provided. Skipping protected endpoints.")
        return
    
    # Test the root endpoint
    test_endpoint("GET", "/")
    
    # Test search endpoint
    payload = {
        "query": "test query",
        "limit": 5,
        "use_optimized_retrieval": True
    }
    results = test_endpoint("POST", "/search", payload)
    
    # Test stats endpoint
    test_endpoint("GET", "/stats")
    
    # Test dashboard endpoint
    test_endpoint("GET", "/dashboard")

    print("\nAPI Test completed.")

if __name__ == "__main__":
    main()

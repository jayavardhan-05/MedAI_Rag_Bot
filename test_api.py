#!/usr/bin/env python3
"""
MED AI API Test Script
Tests the backend API functionality
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_ask_endpoint():
    """Test the ask endpoint with a sample question"""
    print("🔍 Testing ask endpoint...")
    
    test_question = "What are the symptoms of hypertension?"
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/ask",
            json={"question": test_question},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Ask endpoint working!")
            print(f"📝 Question: {test_question}")
            print(f"🤖 Answer: {data.get('answer', 'No answer')[:100]}...")
            print(f"📚 Sources found: {len(data.get('sources', []))}")
            return True
        else:
            print(f"❌ Ask endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing ask endpoint: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 MED AI API Test Suite")
    print("="*40)
    print("🔌 Testing backend API functionality...")
    print("="*40)
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("\n❌ Backend is not running or not healthy.")
        print("   Please start the backend first with:")
        print("   cd backend && python run_server.py")
        return
    
    print("\n" + "-"*40)
    
    # Test ask endpoint
    ask_ok = test_ask_endpoint()
    
    print("\n" + "="*40)
    if health_ok and ask_ok:
        print("🎉 All tests passed! MED AI backend is working correctly.")
        print("🚀 You can now start the frontend and use the application.")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
    
    print("="*40)

if __name__ == "__main__":
    main()
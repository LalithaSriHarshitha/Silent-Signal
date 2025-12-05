"""
Test script for Silent Signal AI API
Run this to verify your server is working correctly
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check Passed")
            print(f"   Status: {data['status']}")
            print(f"   App: {data['app']}")
            print(f"   Environment: {data['environment']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_status():
    """Test status endpoint"""
    print("\n🔍 Testing Status Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status Check Passed")
            print(f"   API: {data['api']}")
            print(f"   Database: {data['database']}")
            print(f"   Services: {len(data['services'])} configured")
            return True
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("\n🔍 Testing Root Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print(f"✅ Root endpoint accessible")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_docs():
    """Test API documentation"""
    print("\n🔍 Testing API Documentation...")
    try:
        response = requests.get(f"{BASE_URL}/api/docs")
        if response.status_code == 200:
            print(f"✅ API Docs accessible at {BASE_URL}/api/docs")
            return True
        else:
            print(f"❌ API docs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Silent Signal AI - API Test Suite")
    print("=" * 60)
    print(f"Testing server at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Status Check", test_status()))
    results.append(("Root Endpoint", test_root()))
    results.append(("API Documentation", test_docs()))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your server is working correctly.")
        print(f"\n📖 Next steps:")
        print(f"   1. Visit {BASE_URL}/api/docs for interactive API documentation")
        print(f"   2. Visit {BASE_URL}/ to see the landing page")
        print(f"   3. Add API keys to .env for full functionality")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

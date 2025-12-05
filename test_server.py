"""Test if server routes are working"""
import requests

BASE_URL = "http://localhost:8000"

tests = [
    ("/", "Landing Page"),
    ("/demo", "Demo Mode"),
    ("/test", "Test Dashboard"),
    ("/setup", "Setup Guide"),
    ("/pricing", "Pricing Page"),
    ("/api/health", "Health Check"),
]

print("=" * 60)
print("TESTING SERVER ROUTES")
print("=" * 60)

for path, name in tests:
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url, timeout=5)
        status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
        print(f"{status:10} {name:20} {url}")
        if response.status_code != 200:
            print(f"           Response: {response.text[:100]}")
    except Exception as e:
        print(f"❌ ERROR  {name:20} {url}")
        print(f"           Error: {str(e)[:100]}")

print("=" * 60)

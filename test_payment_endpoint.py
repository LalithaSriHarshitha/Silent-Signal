"""Test payment endpoint"""
import requests
import json

# Test the endpoint
url = "http://localhost:8000/api/payments/create-checkout-session"
data = {"tier": "premium"}

print(f"Testing: {url}")
print(f"Data: {data}")
print("-" * 50)

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except requests.exceptions.ConnectionError:
    print("❌ Server is not running!")
    print("Start the server with: START_SERVER_HERE.bat")
except Exception as e:
    print(f"❌ Error: {e}")

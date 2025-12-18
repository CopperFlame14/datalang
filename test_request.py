import requests
import json

url = "http://127.0.0.1:8000/extract-intent"
payload = {"text": "Remind me to submit the report urgent next Tuesday"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

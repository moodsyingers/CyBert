"""
Direct test to see raw API response
"""
import requests
import json

text = "The ransomware Conti targeted healthcare using Microsoft Exchange vulnerabilities"

response = requests.post(
    "http://localhost:5001/api/ner/analyze",
    json={"text": text},
    headers={"Content-Type": "application/json"}
)

print(f"Status: {response.status_code}")
print(f"\nFull Response:")
print(json.dumps(response.json(), indent=2))

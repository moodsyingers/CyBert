"""
Test the enhanced NER API
"""
import requests
import json

API_URL = "http://localhost:5001"

def test_text(text, description):
    print("\n" + "="*70)
    print(f"TEST: {description}")
    print("="*70)
    print(f"Input: {text}\n")
    
    response = requests.post(
        f"{API_URL}/api/ner/analyze",
        json={"text": text},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        entities = data.get('entities', [])
        
        print(f"Detected {len(entities)} entities:")
        for ent in entities:
            print(f"  - {ent['word']:<30} -> {ent['entity_type']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING ENHANCED NER API")
    print("="*70)
    
    # Test 1: The problematic text
    test_text(
        "The ransomware Conti targeted healthcare using Microsoft Exchange vulnerabilities",
        "Problematic text with Conti ransomware"
    )
    
    # Test 2: APT example
    test_text(
        "APT28 exploited CVE-2023-12345 in a phishing campaign",
        "APT28 with CVE and phishing"
    )
    
    # Test 3: Multiple entities
    test_text(
        "Fancy Bear used Cobalt Strike for lateral movement and deployed Emotet malware",
        "Multiple threat actor and tools"
    )
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70 + "\n")

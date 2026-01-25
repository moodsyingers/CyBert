"""
Simple NVD Data Collection Script
Fetches CVE data from NVD API (limited to 10,000 CVEs)
"""

import json
import requests
import time
import os


def fetch_nvd_cves(max_cves=10000, output_dir="datasets/nvd"):
    """Fetch CVE data from NVD API"""
    
    # Create output directory in project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, output_dir)
    os.makedirs(output_path, exist_ok=True)
    
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    print(f"Fetching up to {max_cves} CVEs from NVD API...")
    print(f"Output directory: {output_path}")
    print()
    
    all_cves = []
    start_index = 0
    
    while len(all_cves) < max_cves:
        print(f"Fetching CVEs starting at index {start_index}...", end=" ")
        
        params = {
            'resultsPerPage': min(2000, max_cves - len(all_cves)),
            'startIndex': start_index
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                vulnerabilities = data.get('vulnerabilities', [])
                
                if not vulnerabilities:
                    print("No more data")
                    break
                
                for vuln in vulnerabilities:
                    cve = vuln.get('cve', {})
                    
                    # Get description
                    descriptions = cve.get('descriptions', [])
                    desc_text = next(
                        (d['value'] for d in descriptions if d.get('lang') == 'en'),
                        ''
                    )
                    
                    if desc_text:
                        # Extract year from CVE ID (e.g., CVE-2023-12345)
                        cve_id = cve.get('id', '')
                        year = cve_id.split('-')[1] if '-' in cve_id else 'unknown'
                        
                        record = {
                            'cve_id': cve_id,
                            'description': desc_text,
                            'published': cve.get('published', ''),
                            'year': year
                        }
                        all_cves.append(record)
                        
                        # Stop if we reached max
                        if len(all_cves) >= max_cves:
                            break
                
                print(f"Got {len(vulnerabilities)} CVEs (total collected: {len(all_cves)})")
                
                # Stop if we reached max
                if len(all_cves) >= max_cves:
                    print(f"Reached target of {max_cves} CVEs")
                    break
                
                start_index += len(vulnerabilities)
                
                # Wait to respect rate limits (5 requests per 30 seconds)
                time.sleep(6)
                
            else:
                print(f"Error {response.status_code}")
                print(f"Response: {response.text[:200]}")
                break
                
        except Exception as e:
            print(f"Error: {str(e)}")
            break
    
    # Save all data
    output_file = os.path.join(output_path, 'nvd_cves.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_cves, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"Collection complete!")
    print(f"Total CVEs collected: {len(all_cves)}")
    print(f"Saved to: {output_file}")
    print(f"File size: {os.path.getsize(output_file):,} bytes")
    
    return all_cves


if __name__ == "__main__":
    cves = fetch_nvd_cves(max_cves=10000)
    print(f"\nDone! Collected {len(cves)} CVE descriptions")

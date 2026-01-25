"""
Simple MLM Data Cleaning Script
Processes NVD JSON file and creates corpus.txt
"""

import json
import os
import re


def clean_text(text):
    """Clean a single text description"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    # Strip
    text = text.strip()
    return text


def process_nvd_data():
    """Process NVD JSON file and create corpus"""
    
    # Get paths relative to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    input_file = os.path.join(project_root, "datasets/nvd/nvd_cves.json")
    output_dir = os.path.join(project_root, "datasets/cyber")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loading NVD data from: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        print("Please run 01_mlm_data_collection.py first")
        return
    
    # Load JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} CVE records")
    
    # Extract descriptions
    all_descriptions = []
    for record in data:
        desc = record.get('description', '').strip()
        if desc and len(desc) > 20:  # Filter short/empty
            all_descriptions.append(desc)
    
    print(f"Valid descriptions: {len(all_descriptions)}")
    
    # Clean descriptions
    print("Cleaning text...")
    cleaned = [clean_text(desc) for desc in all_descriptions]
    
    # Remove duplicates
    print("Removing duplicates...")
    unique = list(set(cleaned))
    
    print(f"Unique descriptions: {len(unique)}")
    removed = len(all_descriptions) - len(unique)
    print(f"Duplicates removed: {removed}")
    
    # Save corpus
    corpus_file = os.path.join(output_dir, 'corpus.txt')
    with open(corpus_file, 'w', encoding='utf-8') as f:
        for desc in unique:
            f.write(desc + '\n')
    
    file_size = os.path.getsize(corpus_file)
    
    print()
    print(f"Saved to: {corpus_file}")
    print(f"Lines: {len(unique)}")
    print(f"Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    # Save report
    report = {
        'input_file': input_file,
        'total_loaded': len(data),
        'valid_descriptions': len(all_descriptions),
        'unique_descriptions': len(unique),
        'duplicates_removed': removed,
        'output_file': corpus_file
    }
    
    report_file = os.path.join(output_dir, 'cleaning_report.json')
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report: {report_file}")


if __name__ == "__main__":
    process_nvd_data()
    print("\nDone!")

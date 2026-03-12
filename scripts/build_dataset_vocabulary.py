"""
Build Entity Vocabulary from CyberNER Dataset
Extracts all cybersecurity entities from cyberner_clean.csv and creates a JSON lookup file.
This vocabulary is used as a fallback in the NER API to catch entities the model might miss.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict, Counter

def extract_entity_vocabulary(csv_path, output_path):
    """
    Extract entity vocabulary from the CyberNER dataset.
    Creates a mapping of words to their entity types.
    """
    print(f"Reading dataset from: {csv_path}")
    
    # Track word -> entity type mappings
    word_to_entities = defaultdict(Counter)
    multi_word_entities = defaultdict(Counter)
    
    # Statistics
    total_rows = 0
    entity_rows = 0
    
    # Read CSV and extract entities
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        current_sentence = None
        current_entity_tokens = []
        current_entity_type = None
        
        for row in reader:
            total_rows += 1
            
            word = row['Word']
            tag = row['Tag']
            sentence_id = row['Sentence_ID']
            
            # Skip non-entity tokens
            if tag == 'O':
                # Save any ongoing multi-word entity
                if current_entity_tokens:
                    entity_text = ' '.join(current_entity_tokens).lower()
                    multi_word_entities[entity_text][current_entity_type] += 1
                    current_entity_tokens = []
                    current_entity_type = None
                continue
            
            entity_rows += 1
            
            # Extract entity type (B-MALWARE -> MALWARE)
            if '-' in tag:
                prefix, entity_type = tag.split('-', 1)
            else:
                prefix = 'B'
                entity_type = tag
            
            # Handle multi-word entities
            if prefix == 'B':  # Beginning of entity
                # Save previous entity if exists
                if current_entity_tokens:
                    entity_text = ' '.join(current_entity_tokens).lower()
                    multi_word_entities[entity_text][current_entity_type] += 1
                
                # Start new entity
                current_entity_tokens = [word]
                current_entity_type = entity_type
                
                # Also store as single word
                word_lower = word.lower()
                if len(word_lower) > 1:  # Skip single characters
                    word_to_entities[word_lower][entity_type] += 1
                    
            elif prefix == 'I':  # Inside/continuation of entity
                if current_entity_type == entity_type:
                    current_entity_tokens.append(word)
                    # Also store as single word
                    word_lower = word.lower()
                    if len(word_lower) > 1:
                        word_to_entities[word_lower][entity_type] += 1
                else:
                    # Mismatch - start new entity
                    if current_entity_tokens:
                        entity_text = ' '.join(current_entity_tokens).lower()
                        multi_word_entities[entity_text][current_entity_type] += 1
                    current_entity_tokens = [word]
                    current_entity_type = entity_type
            
            # Print progress
            if total_rows % 100000 == 0:
                print(f"  Processed {total_rows:,} rows...")
    
    # Save final entity if exists
    if current_entity_tokens:
        entity_text = ' '.join(current_entity_tokens).lower()
        multi_word_entities[entity_text][current_entity_type] += 1
    
    print(f"\nDataset Statistics:")
    print(f"  Total rows: {total_rows:,}")
    print(f"  Entity rows: {entity_rows:,}")
    print(f"  Unique single words: {len(word_to_entities):,}")
    print(f"  Unique multi-word entities: {len(multi_word_entities):,}")
    
    # Build final vocabulary (choose most common entity type for each word)
    vocabulary = {
        'single_words': {},
        'multi_word': {},
        'statistics': {
            'total_rows': total_rows,
            'entity_rows': entity_rows,
            'unique_single_words': len(word_to_entities),
            'unique_multi_word_entities': len(multi_word_entities)
        }
    }
    
    # Process single words - keep only words with frequency > 1 to reduce noise
    for word, entity_counts in word_to_entities.items():
        total_count = sum(entity_counts.values())
        if total_count > 1:  # Filter out words that appear only once
            # Choose most common entity type
            most_common_type = entity_counts.most_common(1)[0][0]
            vocabulary['single_words'][word] = {
                'entity_type': most_common_type,
                'count': total_count
            }
    
    # Process multi-word entities - keep all
    for entity, entity_counts in multi_word_entities.items():
        total_count = sum(entity_counts.values())
        if total_count > 1 and len(entity.split()) > 1:  # Only multi-word
            most_common_type = entity_counts.most_common(1)[0][0]
            vocabulary['multi_word'][entity] = {
                'entity_type': most_common_type,
                'count': total_count
            }
    
    # Update statistics
    vocabulary['statistics']['filtered_single_words'] = len(vocabulary['single_words'])
    vocabulary['statistics']['filtered_multi_word'] = len(vocabulary['multi_word'])
    
    # Print entity type distribution
    entity_type_dist = Counter()
    for word_data in vocabulary['single_words'].values():
        entity_type_dist[word_data['entity_type']] += 1
    for entity_data in vocabulary['multi_word'].values():
        entity_type_dist[entity_data['entity_type']] += 1
    
    print(f"\nFiltered Vocabulary:")
    print(f"  Single words (freq > 1): {len(vocabulary['single_words']):,}")
    print(f"  Multi-word entities (freq > 1): {len(vocabulary['multi_word']):,}")
    
    print(f"\nEntity Type Distribution:")
    for entity_type, count in entity_type_dist.most_common():
        print(f"  {entity_type}: {count:,}")
    
    # Save to JSON
    print(f"\nSaving vocabulary to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vocabulary, f, indent=2, ensure_ascii=False)
    
    print("[SUCCESS] Vocabulary built successfully!")
    return vocabulary

def main():
    # Paths
    base_dir = Path(__file__).parent.parent
    csv_path = base_dir / "datasets" / "cyber" / "cyberner_clean.csv"
    output_path = base_dir / "datasets" / "cyber" / "entity_vocabulary.json"
    
    # Check if CSV exists
    if not csv_path.exists():
        print(f"Error: Dataset not found at {csv_path}")
        return
    
    # Build vocabulary
    extract_entity_vocabulary(csv_path, output_path)
    
    print(f"\nVocabulary file created: {output_path}")
    print("This file will be loaded by the NER API at startup.")

if __name__ == "__main__":
    main()

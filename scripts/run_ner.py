"""Test NER with complete word extraction"""

import os
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Get the project root directory (parent of scripts folder)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "mini_cybert_final")

def extract_entities(text):
    """Extract cybersecurity entities from text
    
    Args:
        text: Input text to analyze
    """
    print(f"\nInput: {text}")
    
    # Tokenize with offset mapping to track character positions
    inputs = tokenizer(text, return_tensors="pt", return_offsets_mapping=True)
    offset_mapping = inputs.pop('offset_mapping')[0].tolist()
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    
    # Get predictions
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1)[0].tolist()
    
    # Helper function to check if character is part of a token
    def is_token_char(char):
        """Check if character is part of a cybersecurity token"""
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.:/')
        return char in valid_chars
    
    # Step 1: Extract ALL meaningful words from the text
    words = []
    i = 0
    while i < len(text):
        if is_token_char(text[i]):
            # Found start of a word
            start = i
            while i < len(text) and is_token_char(text[i]):
                i += 1
            word_text = text[start:i]
            words.append({
                'text': word_text,
                'start': start,
                'end': i,
                'labels': []  # Will collect all labels for tokens in this word
            })
        else:
            i += 1
    
    # Step 2: Map each token prediction to its corresponding word
    for idx in range(1, len(predictions) - 1):  # Skip [CLS] and [SEP]
        pred_id = predictions[idx]
        label = model.config.id2label[pred_id]
        char_start, char_end = offset_mapping[idx]
        
        # Skip special tokens with (0, 0) offsets
        if char_start == char_end:
            continue
        
        # Find which word this token belongs to
        token_mid = (char_start + char_end) // 2
        for word in words:
            if word['start'] <= token_mid < word['end']:
                word['labels'].append(label)
                break
    
    # Step 3: Assign dominant label to each word
    all_words_with_labels = []
    for word in words:
        if not word['labels']:
            dominant_label = 'O'
        else:
            # Get most common non-O label, or O if all are O
            non_o_labels = [l for l in word['labels'] if l != 'O']
            if non_o_labels:
                # Remove B-/I- prefixes to get entity types
                entity_types = []
                for lbl in non_o_labels:
                    entity_type = lbl.split('-')[-1] if '-' in lbl else lbl
                    entity_types.append(entity_type)
                # Get most common entity type
                from collections import Counter
                dominant_label = Counter(entity_types).most_common(1)[0][0]
            else:
                dominant_label = 'O'
        
        all_words_with_labels.append({
            'word': word['text'],
            'start': word['start'],
            'end': word['end'],
            'type': dominant_label
        })
    
    # Display words with their detected labels
    detected_entities = []
    
    if all_words_with_labels:
        # Collect detected entities
        for word_info in all_words_with_labels:
            if word_info['type'] != 'O':
                detected_entities.append((word_info['word'], word_info['type']))
    
    # Display detected entities
    if detected_entities:
        print("DETECTED ENTITIES:")
        for entity, entity_type in detected_entities:
            print(f"  {entity:30s} → {entity_type}")
    else:
        print(" No entities detected")
    print()

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH)
print("Model loaded!\n")

print("="*70)
print("Interactive Cybersecurity NER System")
print("="*70)
print("This system extracts cybersecurity entities from your questions.")
print("Entity types: MALWARE, APT, TOOL, VULNERABILITY, CVE, etc.")
print("\nCommands:")
print("  /verbose - Toggle verbose mode (show all tokens)")
print("  quit, exit, q - Stop the program")
print("="*70)
print()

# Interactive loop
while True:
    try:
        # Get user input
        user_input = input("Enter your question or text: ").strip()
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit', 'q', '']:
            print("\nThank you for using the NER system. Goodbye!")
            break
        
        # Process the input
        extract_entities(user_input)
        
    except KeyboardInterrupt:
        print("\n\n Interrupted. Goodbye!")
        break
    except Exception as e:
        print(f" Error: {e}")
        print("Please try again.\n")

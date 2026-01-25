"""
Flask Backend API for Mini-CyBERT Models (NER + MLM)
Provides cybersecurity entity recognition and masked language modeling
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import (
    pipeline, 
    AutoTokenizer, 
    AutoModelForTokenClassification,
    AutoModelForMaskedLM
)
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Model paths
BASE_DIR = Path(__file__).parent.parent
NER_MODEL_PATH = BASE_DIR / "models" / "mini_cybert_final"
MLM_MODEL_PATH = BASE_DIR / "models" / "mlm_final"

# Global model variables
ner_pipeline = None
mlm_pipeline = None
ner_tokenizer = None
ner_model = None
ner_loaded = False
mlm_loaded = False


def load_models():
    """Load both NER and MLM models"""
    global ner_pipeline, mlm_pipeline, ner_loaded, mlm_loaded
    global ner_tokenizer, ner_model  # Store separately for custom processing
    
    # Load NER model - using direct model/tokenizer instead of pipeline
    try:
        print(f"Loading NER model from: {NER_MODEL_PATH}")
        ner_tokenizer = AutoTokenizer.from_pretrained(str(NER_MODEL_PATH))
        ner_model = AutoModelForTokenClassification.from_pretrained(str(NER_MODEL_PATH))
        ner_loaded = True
        print("NER model loaded successfully!")
    except Exception as e:
        print(f"Error loading NER model: {e}")
        ner_loaded = False
    
    # Load MLM model
    try:
        print(f"Loading MLM model from: {MLM_MODEL_PATH}")
        tokenizer = AutoTokenizer.from_pretrained(str(MLM_MODEL_PATH))
        model = AutoModelForMaskedLM.from_pretrained(str(MLM_MODEL_PATH))
        mlm_pipeline = pipeline(
            "fill-mask",
            model=model,
            tokenizer=tokenizer
        )
        mlm_loaded = True
        print("MLM model loaded successfully!")
    except Exception as e:
        print(f"Error loading MLM model: {e}")
        mlm_loaded = False
    
    return ner_loaded or mlm_loaded

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ner_loaded': ner_loaded,
        'mlm_loaded': mlm_loaded
    })

@app.route('/api/ner/analyze', methods=['POST'])
def analyze_ner():
    """Analyze text and extract cybersecurity entities"""
    try:
        if not ner_loaded:
            return jsonify({'error': 'NER model not loaded'}), 500
        
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Tokenize with offset mapping to track character positions
        inputs = ner_tokenizer(text, return_tensors="pt", return_offsets_mapping=True)
        offset_mapping = inputs.pop('offset_mapping')[0].tolist()
        
        # Get predictions
        outputs = ner_model(**inputs)
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
            label = ner_model.config.id2label[pred_id]
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
        from collections import Counter
        
        entities = []
        for word in words:
            if not word['labels']:
                continue
            
            # Get most common non-O label, or skip if all are O
            non_o_labels = [l for l in word['labels'] if l != 'O']
            if non_o_labels:
                # Remove B-/I- prefixes to get entity types
                entity_types = []
                for lbl in non_o_labels:
                    entity_type = lbl.split('-')[-1] if '-' in lbl else lbl
                    entity_types.append(entity_type)
                
                # Get most common entity type
                dominant_label = Counter(entity_types).most_common(1)[0][0]
                
                # Add to entities list
                entities.append({
                    'word': word['text'],
                    'entity_type': dominant_label,
                    'start': word['start'],
                    'end': word['end']
                })
        
        response = {
            'text': text,
            'entities': entities,
            'entity_count': len(entities)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/mlm/predict', methods=['POST'])
def predict_mlm():
    """Predict masked words in text"""
    try:
        if not mlm_loaded:
            return jsonify({'error': 'MLM model not loaded'}), 500
        
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if '[MASK]' not in text and '<mask>' not in text:
            return jsonify({'error': 'Text must contain [MASK] or <mask> token'}), 400
        
        # Perform fill-mask
        results = mlm_pipeline(text)
        
        # Extract top 5 predictions
        predictions = [result['token_str'].strip() for result in results[:5]]
        
        response = {
            'text': text,
            'predictions': predictions
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*70)
    print("MINI-CYBERT API SERVER (NER + MLM)")
    print("="*70)
    
    if load_models():
        print("\nStarting Flask server on http://localhost:5001")
        print("\nAPI Endpoints:")
        if ner_loaded:
            print("  NER Model:")
            print("    - POST /api/ner/analyze  - Extract entities")
        if mlm_loaded:
            print("  MLM Model:")
            print("    - POST /api/mlm/predict  - Predict masked words")
        print("  General:")
        print("    - GET  /api/health       - Health check")
        print("="*70)
        
        app.run(debug=False, host='0.0.0.0', port=5001)
    else:
        print("\nFailed to load models!")
        print("Please ensure models are placed at:")
        print(f"  NER: {NER_MODEL_PATH}")
        print(f"  MLM: {MLM_MODEL_PATH}")

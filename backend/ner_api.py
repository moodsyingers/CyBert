"""
Flask Backend API for Mini-CyBERT Models (NER + MLM)
Provides cybersecurity entity recognition and masked language modeling.
Long text is split into sentences; NER runs per sentence (sliding window if >512 tokens), then results are combined.
"""

import re
from pathlib import Path
from collections import Counter

import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForTokenClassification,
    AutoModelForMaskedLM,
)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Model paths
BASE_DIR = Path(__file__).parent.parent
NER_MODEL_PATH = BASE_DIR / "models" / "mini_cybert_final"
MLM_MODEL_PATH = BASE_DIR / "models" / "mlm_final"

# Model max length (BERT limit)
NER_MAX_LENGTH = 512
# Sliding window stride when a segment exceeds NER_MAX_LENGTH tokens
NER_WINDOW_STRIDE = 256

# Global model variables
ner_pipeline = None
mlm_pipeline = None
ner_tokenizer = None
ner_model = None
ner_loaded = False
mlm_loaded = False


def split_into_sentences(text):
    """Split text into sentences; return list of (sentence_text, start_offset_in_original)."""
    if not text or not text.strip():
        return []
    text = text.strip()
    pattern = r'(?<=[.!?])\s+'
    parts = re.split(pattern, text)
    result = []
    current = 0
    for p in parts:
        s = p.strip()
        if not s:
            continue
        idx = text.find(s, current)
        if idx == -1:
            idx = current
        result.append((s, idx))
        current = idx + len(s)
    return result


def _is_token_char(char):
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.:/')
    return char in valid_chars


def _build_words(segment_text):
    """Build list of words with character spans; each word has 'labels': []."""
    words = []
    i = 0
    while i < len(segment_text):
        if _is_token_char(segment_text[i]):
            start = i
            while i < len(segment_text) and _is_token_char(segment_text[i]):
                i += 1
            words.append({'text': segment_text[start:i], 'start': start, 'end': i, 'labels': []})
        else:
            i += 1
    return words


def _words_to_entities(words):
    """Convert words (with labels filled) to entity list; one unique entity per word (dominant type)."""
    entities = []
    for word in words:
        if not word['labels']:
            continue
        non_o_labels = [l for l in word['labels'] if l != 'O']
        if not non_o_labels:
            continue
        entity_types = [lbl.split('-')[-1] if '-' in lbl else lbl for lbl in non_o_labels]
        dominant_type = Counter(entity_types).most_common(1)[0][0]
        entities.append({
            'word': word['text'],
            'entity_type': dominant_type,
            'start': word['start'],
            'end': word['end'],
        })
    return entities


def _assign_labels_to_words(words, offset_mapping, predictions, model):
    """Assign token-level predictions to words using offset_mapping (segment-relative)."""
    for idx in range(1, len(predictions) - 1):
        pred_id = predictions[idx]
        label = model.config.id2label[pred_id]
        char_start, char_end = offset_mapping[idx]
        if char_start == char_end:
            continue
        token_mid = (char_start + char_end) // 2
        for word in words:
            if word['start'] <= token_mid < word['end']:
                word['labels'].append(label)
                break


def extract_entities_from_segment_sliding_window(segment_text, tokenizer, model):
    """Run NER on a long segment using overlapping token windows. No truncation."""
    enc = tokenizer(
        segment_text,
        return_offsets_mapping=True,
        truncation=False,
        add_special_tokens=True,
    )
    input_ids_list = enc['input_ids']
    offset_mapping = enc['offset_mapping']
    n_content = len(input_ids_list) - 2

    if n_content <= 0:
        return []

    words = _build_words(segment_text)
    if not words:
        return []

    for start in range(0, n_content, NER_WINDOW_STRIDE):
        end = min(start + NER_MAX_LENGTH, n_content)
        window_ids = (
            [input_ids_list[0]]
            + input_ids_list[1 + start : 1 + end]
            + [input_ids_list[-1]]
        )
        inputs = {
            'input_ids': torch.tensor([window_ids], dtype=torch.long),
            'attention_mask': torch.ones(1, len(window_ids), dtype=torch.long),
        }
        with torch.no_grad():
            logits = model(**inputs).logits
        preds = logits.argmax(dim=-1)[0][1:-1].tolist()

        for i in range(end - start):
            content_idx = start + i
            char_start, char_end = offset_mapping[1 + content_idx]
            if char_start == char_end:
                continue
            label = model.config.id2label[preds[i]]
            token_mid = (char_start + char_end) // 2
            for word in words:
                if word['start'] <= token_mid < word['end']:
                    word['labels'].append(label)
                    break

    return _words_to_entities(words)


def extract_entities_from_segment(segment_text, tokenizer, model):
    """Run NER on one segment. Uses sliding window if segment exceeds NER_MAX_LENGTH tokens."""
    enc = tokenizer(
        segment_text,
        return_offsets_mapping=True,
        truncation=False,
        add_special_tokens=True,
    )
    n_tokens = len(enc['input_ids'])

    if n_tokens > NER_MAX_LENGTH + 2:
        return extract_entities_from_segment_sliding_window(segment_text, tokenizer, model)

    inputs = tokenizer(
        segment_text,
        return_tensors="pt",
        return_offsets_mapping=True,
        truncation=True,
        max_length=NER_MAX_LENGTH,
    )
    offset_mapping = inputs.pop('offset_mapping')[0].tolist()
    predictions = model(**inputs).logits.argmax(dim=-1)[0].tolist()

    words = _build_words(segment_text)
    _assign_labels_to_words(words, offset_mapping, predictions, model)
    return _words_to_entities(words)


def run_ner_on_text(text, tokenizer, model):
    """
    Split text into sentences, run NER on each, combine with global offsets.
    Returns (per_sentence_list, combined_entities).
    """
    sentences_with_offsets = split_into_sentences(text)
    if not sentences_with_offsets:
        sentences_with_offsets = [(text.strip(), 0)] if text.strip() else []

    per_sentence = []
    combined = []

    seen_spans = set()  # global (start, end) to avoid duplicate entities in combined

    for sent_text, sent_start in sentences_with_offsets:
        seg_entities = extract_entities_from_segment(sent_text, tokenizer, model)
        seg_unique = []
        for e in seg_entities:
            g_start = sent_start + e['start']
            g_end = sent_start + e['end']
            key = (g_start, g_end)
            if key in seen_spans:
                continue
            seen_spans.add(key)
            seg_unique.append(e)
        for e in seg_unique:
            combined.append({
                'word': e['word'],
                'entity_type': e['entity_type'],
                'start': sent_start + e['start'],
                'end': sent_start + e['end'],
            })
        per_sentence.append({
            'sentence': sent_text,
            'start_offset': sent_start,
            'entities': [
                {'word': e['word'], 'entity_type': e['entity_type'], 'start': e['start'], 'end': e['end']}
                for e in seg_unique
            ],
        })

    return per_sentence, combined


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
    """Analyze text: split into sentences, run NER per sentence, return per-sentence + combined entities."""
    try:
        if not ner_loaded:
            return jsonify({'error': 'NER model not loaded'}), 500

        data = request.json
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        per_sentence, combined = run_ner_on_text(text, ner_tokenizer, ner_model)

        response = {
            'text': text,
            'sentences': per_sentence,
            'entities': combined,
            'entity_count': len(combined),
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
        
        # Perform fill-mask; get more candidates to filter out single-char tokens
        results = mlm_pipeline(text, top_k=20)
        
        # Keep only word-like predictions (length >= 2, has at least one letter)
        def is_word_like(s):
            t = (s or '').strip()
            return len(t) >= 2 and any(c.isalpha() for c in t)
        word_like = [r['token_str'].strip() for r in results if is_word_like(r['token_str'])]
        seen = set()
        unique = []
        for w in word_like:
            if w not in seen:
                seen.add(w)
                unique.append(w)
        predictions = unique[:5]
        if not predictions:
            predictions = [r['token_str'].strip() for r in results[:3]]
        
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

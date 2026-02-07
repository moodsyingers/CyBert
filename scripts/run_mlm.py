"""
MLM Model - Fill-Mask Script
Use this to predict masked words in cybersecurity text
"""

import os
from transformers import pipeline, AutoTokenizer, AutoModelForMaskedLM

# Get the project root directory (parent of scripts folder)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "mlm_final")

def is_word_like(token_str):
    """Filter out single chars and non-word-like tokens (e.g. 'g', 's', 'd')."""
    s = token_str.strip()
    if len(s) < 2:
        return False
    # Require at least one letter so we skip pure punctuation/numbers
    if not any(c.isalpha() for c in s):
        return False
    return True


def predict_mask(text, top_k=20, show=5):
    """Predict the [MASK] token in the given text. Shows only word-like predictions (no single chars)."""
    print(f"\nInput: {text}")
    
    # Check if mask token is in text, if not, try to replace <mask> with [MASK]
    if '[MASK]' not in text:
        if '<mask>' in text:
            text = text.replace('<mask>', '[MASK]')
        else:
            print("WARNING: No [MASK] token found in text!")
            return

    # Get more candidates so we can filter out single-token / junk predictions
    results = fill_mask(text, top_k=top_k)
    
    word_like = [r['token_str'].strip() for r in results if is_word_like(r['token_str'])]
    # Deduplicate while preserving order (same word can appear multiple times with different scores)
    seen = set()
    unique = []
    for w in word_like:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    
    print("Predictions (word-like only):")
    for i, predicted_word in enumerate(unique[:show], 1):
        print(f"   {i}. {predicted_word}")
    if not unique:
        print("   (no word-like predictions; showing raw top 3)")
        for i, result in enumerate(results[:3], 1):
            print(f"   {i}. {result['token_str'].strip()}")
    print()

# Load model once
print("="*70)
print("MLM MODEL - FILL-MASK PREDICTOR")
print("="*70)
print("\nLoading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForMaskedLM.from_pretrained(MODEL_PATH)
fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)

print("Model loaded!\n")
print("="*70)
print("USAGE: Replace any word with [MASK] to predict it")
print("="*70)

# Example predictions
print("\nEXAMPLES:\n")

examples = [
    "The attacker used a [MASK] exploit to gain access.",
    "APT28 deployed [MASK] to steal credentials.",
    "The vulnerability allows remote [MASK] execution.",
    "The firewall blocked the [MASK] attack.",
    "Hackers exploited a [MASK] in the system.",
]

for example in examples:
    predict_mask(example)

# Interactive mode
print("="*70)
print("INTERACTIVE MODE")
print("="*70)
print("Enter your text with [MASK] (or 'quit' to exit)\n")

while True:
    user_input = input("Your text: ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("\nGoodbye!")
        break
    
    if not user_input:
        continue
    
    if '[MASK]' not in user_input and '<mask>' not in user_input:
        print("WARNING: Please include [MASK] in your text\n")
        continue
    
    predict_mask(user_input)

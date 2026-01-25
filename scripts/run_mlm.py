"""
MLM Model - Fill-Mask Script
Use this to predict masked words in cybersecurity text
"""

from transformers import pipeline, AutoTokenizer, AutoModelForMaskedLM

MODEL_PATH = r"e:\project\shiley-project\models\mlm_final"

def predict_mask(text):
    """Predict the [MASK] token in the given text"""
    print(f"\nInput: {text}")
    
    # Check if mask token is in text, if not, try to replace <mask> with [MASK]
    if '[MASK]' not in text:
        if '<mask>' in text:
            text = text.replace('<mask>', '[MASK]')
        else:
            print("WARNING: No [MASK] token found in text!")
            return

    results = fill_mask(text)
    
    print("Predictions:")
    for i, result in enumerate(results[:5], 1):
        predicted_word = result['token_str'].strip()
        print(f"   {i}. {predicted_word}")
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

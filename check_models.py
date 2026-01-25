"""
Simple Model Checker Script
Verifies both MLM and NER models are working correctly
"""

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForMaskedLM,
    AutoModelForTokenClassification
)
import os

# Model paths
MLM_PATH = r"e:\project\shiley-project\models\mlm_final"
NER_PATH = r"e:\project\shiley-project\models\mini_cybert_final"

def check_mlm():
    """Check MLM Model (Fill-Mask)"""
    print("\n" + "="*70)
    print("CHECKING MLM MODEL (Fill-Mask)")
    print("="*70)
    
    try:
        print(f"Loading from: {MLM_PATH}")
        
        tokenizer = AutoTokenizer.from_pretrained(MLM_PATH)
        model = AutoModelForMaskedLM.from_pretrained(MLM_PATH)
        fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)
        
        print("MLM Model loaded successfully!\n")
        
        # Test
        test_text = "The attacker used a <mask> exploit to gain access."
        print(f"Test: {test_text}")
        
        results = fill_mask(test_text)
        print("\nTop 3 predictions:")
        for i, r in enumerate(results[:3], 1):
            print(f"   {i}. {r['token_str'].strip()}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_ner():
    """Check NER Model (Entity Recognition)"""
    print("\n" + "="*70)
    print("CHECKING NER MODEL (Entity Recognition)")
    print("="*70)
    
    try:
        print(f"Loading from: {NER_PATH}")
        
        tokenizer = AutoTokenizer.from_pretrained(NER_PATH)
        model = AutoModelForTokenClassification.from_pretrained(NER_PATH)
        ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
        
        print("NER Model loaded successfully!\n")
        
        # Test
        test_text = "APT28 exploited CVE-2023-12345 in a phishing campaign."
        print(f"Test: {test_text}")
        
        results = ner(test_text)
        
        if results:
            print("\nDetected entities:")
            for entity in results:
                print(f"   - {entity['word']:25} -> {entity['entity_group']}")
        else:
            print("   No entities detected")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("MINI-CYBERT MODEL CHECKER")
    print("="*70)
    
    # Check both models
    mlm_ok = check_mlm()
    ner_ok = check_ner()
    
    # Summary
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    if mlm_ok:
        print("MLM Model: Working")
    else:
        print("MLM Model: Failed")
    
    if ner_ok:
        print("NER Model: Working")
    else:
        print("NER Model: Failed")
    
    if mlm_ok and ner_ok:
        print("\nBoth models are working perfectly!")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

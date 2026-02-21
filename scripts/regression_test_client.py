"""
Client regression tests (plan: cyber-only NER/MLM).
- MLM: "... suggesting a [MASK] in the middle attack." -> "man" must appear in top-5.
- NER: Client SSL/man-in-the-middle sentence -> at least one cyber entity (not O).
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Add project root for imports if needed
sys.path.insert(0, PROJECT_ROOT)

MLM_PATH = os.path.join(PROJECT_ROOT, "models", "mlm_final")
NER_PATH = os.path.join(PROJECT_ROOT, "models", "mini_cybert_final")

# Client sentence (must yield at least one entity after retraining)
CLIENT_SENTENCE = (
    "The browser displayed a security warning indicating that the secure sockets layer "
    "certificate presented by the website does not match the expected issuer suggesting "
    "a man in the middle attack."
)

MLM_INPUT = "... suggesting a [MASK] in the middle attack."
EXPECTED_MLM_TOKEN = "man"
TOP_K = 20
TOP_N_WORD_LIKE = 5


def is_word_like(token_str):
    s = (token_str or "").strip()
    if len(s) < 2:
        return False
    if not any(c.isalpha() for c in s):
        return False
    return True


def run_mlm_test():
    """MLM: 'man' should be in top-5 word-like predictions for '[MASK] in the middle attack'."""
    if not os.path.isdir(MLM_PATH):
        print(f"SKIP MLM test: model not found at {MLM_PATH}")
        return None
    try:
        from transformers import pipeline, AutoTokenizer, AutoModelForMaskedLM
    except ImportError:
        print("SKIP MLM test: transformers not installed")
        return None

    tokenizer = AutoTokenizer.from_pretrained(MLM_PATH)
    model = AutoModelForMaskedLM.from_pretrained(MLM_PATH)
    pipe = pipeline("fill-mask", model=model, tokenizer=tokenizer)
    results = pipe(MLM_INPUT, top_k=TOP_K)
    word_like = [r["token_str"].strip() for r in results if is_word_like(r["token_str"])]
    seen = set()
    unique = []
    for w in word_like:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    top5 = unique[:TOP_N_WORD_LIKE]
    passed = EXPECTED_MLM_TOKEN.lower() in [t.lower() for t in top5]
    print(f"  MLM input: {MLM_INPUT!r}")
    print(f"  Top-5 word-like: {top5}")
    print(f"  Expected '{EXPECTED_MLM_TOKEN}' in top-5: {passed}")
    return passed


def run_ner_test():
    """NER: Client sentence must have at least one span tagged with a cyber type (not O)."""
    if not os.path.isdir(NER_PATH):
        print(f"SKIP NER test: model not found at {NER_PATH}")
        return None
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForTokenClassification
    except ImportError:
        print("SKIP NER test: torch/transformers not installed")
        return None

    tokenizer = AutoTokenizer.from_pretrained(NER_PATH)
    model = AutoModelForTokenClassification.from_pretrained(NER_PATH)
    model.eval()
    id2label = model.config.id2label

    words = CLIENT_SENTENCE.split()
    tokenized = tokenizer(
        words,
        is_split_into_words=True,
        return_tensors="pt",
        truncation=True,
    )
    with torch.no_grad():
        out = model(**tokenized)
    pred_ids = out.logits.argmax(-1)[0].tolist()
    # word_ids for first (and only) sequence in batch
    word_ids = tokenized.word_ids(0) if hasattr(tokenized, "word_ids") and tokenized.word_ids(0) is not None else []

    # One label per word (first subword only)
    prev = None
    word_preds = []
    for i, wid in enumerate(word_ids):
        if wid is not None and wid != prev:
            word_preds.append(id2label.get(pred_ids[i], "O"))
        prev = wid
    entity_count = sum(1 for p in word_preds if p and p != "O")
    passed = entity_count >= 1
    print(f"  NER input: (client sentence, {len(words)} words)")
    print(f"  Predicted entities (non-O): {entity_count}")
    print(f"  At least one cyber entity: {passed}")
    return passed


def main():
    print("=" * 70)
    print("CLIENT REGRESSION TESTS")
    print("=" * 70)

    mlm_ok = run_mlm_test()
    print()
    ner_ok = run_ner_test()
    print()

    print("=" * 70)
    if mlm_ok is None and ner_ok is None:
        print("No tests run (models or deps missing). Exit 0.")
        sys.exit(0)
    if mlm_ok is False:
        print("FAIL: MLM test (expected 'man' in top-5 for man-in-the-middle).")
        sys.exit(1)
    if ner_ok is False:
        print("FAIL: NER test (expected at least one entity on client sentence).")
        sys.exit(1)
    print("PASS: All run client regression tests passed.")
    print("=" * 70)
    sys.exit(0)


if __name__ == "__main__":
    main()

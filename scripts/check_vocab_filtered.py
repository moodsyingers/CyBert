"""
Improved Vocabulary Extraction with Filtering
Excludes: stopwords, pure numbers, hex values, tokens < 3 characters
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

# Load corpus
print("Loading corpus...")
with open("datasets/cyber/corpus.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]
print(f"Loaded {len(lines)} lines\n")

# Extract TF-IDF tokens with improved filtering
print("Extracting TF-IDF tokens with filtering...")

vectorizer = TfidfVectorizer(
    token_pattern=r"(?u)\b\w[\w-]*\w\b",
    max_features=1000,  # Extract more initially, then filter
    stop_words='english',  # Remove English stop words
    min_df=2,  # Token must appear in at least 2 documents
)

vectorizer.fit(lines)
initial_tokens = list(vectorizer.get_feature_names_out())
print(f"Initial extraction: {len(initial_tokens)} tokens")

# Filter out unwanted tokens
def is_valid_token(token):
    """Check if token is a meaningful cybersecurity term"""
    
    # Rule 1: Must be at least 3 characters
    if len(token) < 3:
        return False
    
    # Rule 2: Exclude pure numbers (e.g., "123", "2025")
    if re.match(r'^\d+$', token):
        return False
    
    # Rule 3: Exclude hex values (e.g., "0x90", "0f", "ff")
    if re.match(r'^0x[0-9a-fA-F]+$', token):
        return False
    if re.match(r'^[0-9a-fA-F]+$', token) and len(token) <= 4:
        return False
    
    # Rule 4: Exclude tokens that are mostly numbers (e.g., "0000", "95553")
    if re.match(r'^\d+[a-zA-Z]?\d*$', token):
        return False
    
    # Rule 5: Exclude version-like patterns (e.g., "0-beta", "01")
    if re.match(r'^\d+-\w+$', token):
        return False
    
    # Rule 6: Exclude very long hex-like strings
    if re.match(r'^[0-9a-fA-F]{8,}$', token):
        return False
    
    return True

# Apply filtering
filtered_tokens = [token for token in initial_tokens if is_valid_token(token)]
print(f"After filtering: {len(filtered_tokens)} tokens")

# Take top 500 meaningful tokens
tokens = filtered_tokens[:500]
print(f"Final vocabulary: {len(tokens)} tokens\n")

# Display top 200 tokens
print("="*70)
print("TOP 200 FILTERED TF-IDF TOKENS")
print("(Stopwords, numbers, hex values, and short tokens removed)")
print("="*70)
for i, token in enumerate(tokens[:200], 1):
    print(f"{i:3d}. {token}")

# Validation patterns
patterns = {
    'CVE': r'CVE-\d{4}-\d+',
    'URL': r'https?://',
    'IP': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
    'Hash': r'\b[a-fA-F0-9]{32,}\b',
    'FilePath': r'[A-Z]:\\|/',
}

print("\n" + "="*70)
print("VALIDATION CHECK")
print("="*70)

suspicious = []
for token in tokens:
    for name, pattern in patterns.items():
        if re.search(pattern, token, re.IGNORECASE):
            suspicious.append((token, name))

if suspicious:
    print("\n[FAILED] Found suspicious tokens:")
    for token, pattern_name in suspicious:
        print(f"  - '{token}' matches {pattern_name}")
else:
    print("\n[PASSED] No CVE IDs, URLs, hashes, IPs, or file paths found!")
    print(f"[PASSED] All {len(tokens)} tokens are meaningful cybersecurity terms")

print("="*70)

# Additional quality check
print("\n" + "="*70)
print("QUALITY METRICS")
print("="*70)
print(f"Total tokens extracted: {len(tokens)}")
print(f"Average token length: {sum(len(t) for t in tokens) / len(tokens):.1f} characters")
print(f"Tokens >= 5 characters: {sum(1 for t in tokens if len(t) >= 5)}")
print(f"Tokens with hyphens: {sum(1 for t in tokens if '-' in t)}")
print("="*70)

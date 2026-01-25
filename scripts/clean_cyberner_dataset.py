import pandas as pd

# Paths
INPUT_CSV = "datasets/cyber/cyberner.csv"
OUTPUT_CSV = "datasets/cyber/cyberner_clean.csv"

# Load raw dataset
df = pd.read_csv(INPUT_CSV)

# Fill missing tags safely
df["Tag"] = df["Tag"].fillna("O")

# Print unique tags BEFORE cleaning
print("=" * 60)
print("Unique tags BEFORE cleaning:")
print("=" * 60)
before_tags = sorted(df["Tag"].unique())
for tag in before_tags:
    print(tag)
print(f"\nCount: {len(before_tags)}")

# Comprehensive label normalization map
LABEL_NORMALIZATION = {
    # Malware normalization (MAL, Malware -> MALWARE)
    "B-MAL": "B-MALWARE",
    "I-MAL": "I-MALWARE",
    "B-Malware": "B-MALWARE",
    "I-Malware": "I-MALWARE",
    
    # Tool normalization (Tool, GENERAL_TOOL -> TOOL)
    "B-Tool": "B-TOOL",
    "I-Tool": "I-TOOL",
    "B-GENERAL_TOOL": "B-TOOL",
    "I-GENERAL_TOOL": "I-TOOL",
    "B-ATTACK_TOOL": "B-TOOL",
    "I-ATTACK_TOOL": "I-TOOL",
    
    # Vulnerability normalization (VULID, VULNAME, Vulnerability -> VULNERABILITY)
    "B-VULID": "B-VULNERABILITY",
    "I-VULID": "I-VULNERABILITY",
    "B-VULNAME": "B-VULNERABILITY",
    "I-VULNAME": "I-VULNERABILITY",
    "B-Vulnerability": "B-VULNERABILITY",
    "I-Vulnerability": "I-VULNERABILITY",
    
    # Organization normalization (Org, Organization -> ORG)
    "B-Org": "B-ORG",
    "I-Org": "I-ORG",
    "B-Organization": "B-ORG",
    "I-Organization": "I-ORG",
    "B-HackOrg": "B-ORG",
    "I-HackOrg": "I-ORG",
    
    # Identity normalization (IDTY, IDTYL, GENERAL_IDENTITY -> IDENTITY)
    "B-IDTY": "B-IDENTITY",
    "I-IDTY": "I-IDENTITY",
    "B-IDTYL": "B-IDENTITY",
    "B-GENERAL_IDENTITY": "B-IDENTITY",
    "I-GENERAL_IDENTITY": "I-IDENTITY",
    
    # Location normalization (LOC, Area -> LOCATION)
    "B-LOC": "B-LOCATION",
    "I-LOC": "I-LOCATION",
    "B-Area": "B-LOCATION",
    "I-Area": "I-LOCATION",
    
    # Time normalization (Time -> TIME)
    "B-Time": "B-TIME",
    "I-Time": "I-TIME",
    
    # Indicator normalization (Indicator -> INDICATOR)
    "B-Indicator": "B-INDICATOR",
    "I-Indicator": "I-INDICATOR",
    
    # Security Team normalization (SecTeam, S-SECTEAM -> SECTEAM)
    "B-SecTeam": "B-SECTEAM",
    "I-SecTeam": "I-SECTEAM",
    "B-S-SECTEAM": "B-SECTEAM",
    "I-S-SECTEAM": "I-SECTEAM",
    
    # System/Software normalization (System, OS -> SOFTWARE)
    "B-System": "B-SOFTWARE",
    "I-System": "I-SOFTWARE",
    "B-OS": "B-SOFTWARE",
    "I-OS": "I-SOFTWARE",
    
    # Protocol normalization
    "B-PROT": "B-PROTOCOL",
    "I-PROT": "I-PROTOCOL",
    
    # Domain normalization
    "B-DOM": "B-DOMAIN",
    "I-DOM": "I-DOMAIN",
    
    # Encryption normalization
    "B-ENCR": "B-ENCRYPTION",
    "I-ENCR": "I-ENCRYPTION",
    
    # Exploit normalization
    "B-Exp": "B-EXPLOIT",
    "I-Exp": "I-EXPLOIT",
    
    # Activity normalization
    "B-ACT": "B-ACTIVITY",
    "I-ACT": "I-ACTIVITY",
    "B-OffAct": "B-ACTIVITY",
    "I-OffAct": "I-ACTIVITY",
    
    # Purpose normalization
    "B-Purp": "B-PURPOSE",
    "I-Purp": "I-PURPOSE",
    
    # Way/Method normalization
    "B-Way": "B-METHOD",
    "I-Way": "I-METHOD",
    
    # Features normalization
    "B-Features": "B-FEATURE",
    "I-Features": "I-FEATURE",
    
    # Sample File normalization
    "B-SamFile": "B-FILE",
    "I-SamFile": "I-FILE",
    
    # Hash normalization (MD5, SHA1, SHA2 -> HASH)
    "B-MD5": "B-HASH",
    "B-SHA1": "B-HASH",
    "B-SHA2": "B-HASH",
    "I-SHA2": "I-HASH",
}

# Apply normalization
df["Tag"] = df["Tag"].apply(lambda t: LABEL_NORMALIZATION.get(t, t))

# Print unique tags AFTER cleaning
print("\n" + "=" * 60)
print("Unique tags AFTER cleaning:")
print("=" * 60)
after_tags = sorted(df["Tag"].unique())
for tag in after_tags:
    print(tag)
print(f"\nCount: {len(after_tags)}")

# Print reduction summary
print("\n" + "=" * 60)
print("SUMMARY:")
print("=" * 60)
print(f"Tags before cleaning: {len(before_tags)}")
print(f"Tags after cleaning:  {len(after_tags)}")
print(f"Tags reduced by:      {len(before_tags) - len(after_tags)}")
print(f"Reduction percentage: {((len(before_tags) - len(after_tags)) / len(before_tags) * 100):.1f}%")

# Save cleaned dataset
df.to_csv(OUTPUT_CSV, index=False)

print(f"\n✓ Cleaned dataset saved to: {OUTPUT_CSV}")
print(f"✓ Total rows: {len(df):,}")
print(f"✓ Columns: {list(df.columns)}")

# Cybersecurity NER Dataset Cleaning

## Overview

This directory contains scripts to clean and normalize the cybersecurity NER dataset (`cyberner.csv`) by consolidating inconsistent BIO tags.

## Problem

The original dataset had **118 unique tags** with many inconsistencies:

- Case differences: `B-Tool` vs `B-TOOL`
- Semantic duplicates: `B-MAL`, `B-Malware`, `B-MALWARE`
- Abbreviation variants: `B-VULID`, `B-VULNAME`, `B-VULNERABILITY`
- Multiple names for same entity: `B-Org`, `B-Organization`, `B-HackOrg`

## Solution

Created a comprehensive normalization mapping that consolidates tags while preserving the BIO format (Beginning-Inside-Outside).

## Results

- **Original tags:** 118 unique tags
- **Cleaned tags:** 75 unique tags
- **Reduction:** 43 tags (36.4% reduction)
- **Total rows:** 609,922
- **Total sentences:** 10,042

## Cleaned Tag Categories

### Entity Types (37 categories with B- and I- prefixes + O)

1. **ACTIVITY** - Cybersecurity activities
2. **APT** - Advanced Persistent Threats
3. **ATTACK_MOTIVATION** - Motivation behind attacks
4. **ATTACK_PATTERN** - Attack patterns and techniques
5. **ATTACK_RESOURCE_LEVEL** - Resource level of attacks
6. **ATTACK_SOPHISTICATION_LEVEL** - Sophistication level
7. **CAMPAIGN** - Attack campaigns
8. **COURSE_OF_ACTION** - Response actions
9. **DOMAIN** - Domain names
10. **EMAIL** - Email addresses
11. **ENCRYPTION** - Encryption methods
12. **EXPLOIT** - Exploits
13. **FEATURE** - Features
14. **FILE** - File names and paths
15. **HASH** - Hash values (MD5, SHA1, SHA2)
16. **IDENTITY** - Identities
17. **IMPACT** - Impact descriptions
18. **INDICATOR** - Indicators of compromise
19. **INFRASTRUCTURE** - Infrastructure components
20. **INTRUSION_SET** - Intrusion sets
21. **IP** - IP addresses
22. **LOCATION** - Geographic locations
23. **MALWARE** - Malware names
24. **MALWARE_ANALYSIS** - Malware analysis
25. **METHOD** - Attack methods
26. **OBSERVED_DATA** - Observed data
27. **ORG** - Organizations
28. **PROTOCOL** - Network protocols
29. **PURPOSE** - Purpose descriptions
30. **SECTEAM** - Security teams
31. **SOFTWARE** - Software/Systems/OS
32. **THREAT_ACTOR** - Threat actors
33. **TIME** - Time references
34. **TOOL** - Tools and utilities
35. **URL** - URLs
36. **VICTIM_IDENTITY** - Victim identities
37. **VULNERABILITY** - Vulnerabilities
38. **O** - Outside (no entity)

## Key Normalizations Applied

| Original Tags                         | →   | Normalized Tag  |
| ------------------------------------- | --- | --------------- |
| B-MAL, B-Malware                      | →   | B-MALWARE       |
| B-Tool, B-GENERAL_TOOL, B-ATTACK_TOOL | →   | B-TOOL          |
| B-VULID, B-VULNAME, B-Vulnerability   | →   | B-VULNERABILITY |
| B-Org, B-Organization, B-HackOrg      | →   | B-ORG           |
| B-System, B-OS                        | →   | B-SOFTWARE      |
| B-LOC, B-Area                         | →   | B-LOCATION      |
| B-IDTY, B-IDTYL, B-GENERAL_IDENTITY   | →   | B-IDENTITY      |
| B-MD5, B-SHA1, B-SHA2                 | →   | B-HASH          |
| B-SecTeam, B-S-SECTEAM                | →   | B-SECTEAM       |
| B-Time                                | →   | B-TIME          |
| B-Indicator                           | →   | B-INDICATOR     |
| B-PROT                                | →   | B-PROTOCOL      |
| B-DOM                                 | →   | B-DOMAIN        |
| B-ENCR                                | →   | B-ENCRYPTION    |
| B-Exp                                 | →   | B-EXPLOIT       |
| B-ACT, B-OffAct                       | →   | B-ACTIVITY      |
| B-Purp                                | →   | B-PURPOSE       |
| B-Way                                 | →   | B-METHOD        |
| B-Features                            | →   | B-FEATURE       |
| B-SamFile                             | →   | B-FILE          |

## Files

### Scripts

- **`clean_cyberner_dataset.py`** - Main cleaning script
- **`get_unique_tags.py`** - Extract unique tags from dataset
- **`write_summary.py`** - Generate cleaning summary report

### Data Files

- **`datasets/cyber/cyberner.csv`** - Original raw dataset (preserved)
- **`datasets/cyber/cyberner_clean.csv`** - Cleaned dataset (ready for training)

### Output Files

- **`unique_tags_output.txt`** - List of all unique tags from original dataset
- **`cleaning_summary.txt`** - Detailed cleaning summary with statistics

## Usage

### 1. Clean the Dataset

```bash
python scripts/clean_cyberner_dataset.py
```

### 2. View Unique Tags

```bash
python scripts/get_unique_tags.py
```

### 3. Generate Summary Report

```bash
python scripts/write_summary.py
```

## Dataset Format

The cleaned dataset maintains the same structure:

| Column      | Description                      |
| ----------- | -------------------------------- |
| Word        | The word/token                   |
| Tag         | BIO tag (cleaned and normalized) |
| Sentence_ID | Sentence identifier              |
| STIX_Tag    | Original STIX tag (preserved)    |
| Source      | Data source (e.g., CyNER)        |

## Tag Distribution (Top 10)

| Tag              | Count   | Percentage |
| ---------------- | ------- | ---------- |
| O                | 494,641 | 81.10%     |
| I-ATTACK_PATTERN | 8,339   | 1.37%      |
| B-ORG            | 7,642   | 1.25%      |
| B-TOOL           | 7,045   | 1.16%      |
| B-MALWARE        | 6,002   | 0.98%      |
| B-LOCATION       | 5,740   | 0.94%      |
| B-APT            | 4,521   | 0.74%      |
| B-IDENTITY       | 4,084   | 0.67%      |
| B-TIME           | 3,757   | 0.62%      |
| B-ACTIVITY       | 3,445   | 0.56%      |

## Next Steps

The cleaned dataset (`cyberner_clean.csv`) is now ready for:

1. NER model training
2. Fine-tuning pre-trained models (BERT, RoBERTa, etc.)
3. Evaluation and benchmarking
4. Integration with cybersecurity NLP pipelines

## Notes

- The original dataset (`cyberner.csv`) is **preserved** and not modified
- All cleaning is done at the CSV level before model training
- BIO format is strictly maintained (B-, I-, O prefixes)
- Sentence_ID and Word columns remain unchanged
- The STIX_Tag column is preserved for reference

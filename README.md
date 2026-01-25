# Mini-CyBERT: Cybersecurity-Aware Language Model

A lightweight, domain-adaptive transformer model for cybersecurity text processing using Hugging Face Transformers.

---

## Project Overview

Mini-CyBERT is a compact language model specifically designed for cybersecurity applications. The model addresses the unique challenges of processing cybersecurity text by extending BERT's vocabulary with domain-specific terminology and fine-tuning using Masked Language Modeling (MLM) on cybersecurity corpora.

**Key Features:**

- Domain-specific vocabulary for cybersecurity terminology
- Fine-tuned on National Vulnerability Database (NVD) data
- Named Entity Recognition (NER) for cybersecurity entities
- Web-based interface for real-time entity extraction

---

## Data Collection and Processing

The project uses data from the National Vulnerability Database (NVD), the official U.S. government repository of vulnerability information.

### Data Collection

**Script:** `scripts/01_mlm_data_collection.py`

Collects CVE (Common Vulnerabilities and Exposures) data from NVD API.

```bash
python scripts/01_mlm_data_collection.py
```

**What it does:**

- Fetches up to 10,000 recent CVE records from NVD
- Extracts vulnerability descriptions
- Saves to `datasets/nvd/nvd_cves.json`
- Respects API rate limits (6 seconds between requests)

**Data Source:** https://nvd.nist.gov/  
**API Endpoint:** https://services.nvd.nist.gov/rest/json/cves/2.0

### Data Cleaning

**Script:** `scripts/02_mlm_data_cleaning.py`

Processes the collected NVD data for model training.

```bash
python scripts/02_mlm_data_cleaning.py
```

**Processing steps:**

1. Extracts descriptions from JSON records
2. Filters invalid or empty entries
3. Normalizes text formatting
4. Removes duplicate descriptions
5. Creates clean corpus file

**Output:** `datasets/cyber/corpus.txt` - Clean text corpus for MLM training

---

## Model Architecture

**Base Model:** BERT (Bidirectional Encoder Representations from Transformers)

**Adaptations:**

1. Vocabulary extension with cybersecurity-specific terms
2. MLM fine-tuning on cybersecurity corpus
3. NER fine-tuning for entity extraction

**Recognized Entity Types:**

- Malware
- Vulnerabilities (CVE IDs)
- Software/Systems
- Organizations/Threat Actors
- Indicators of Compromise (IOCs)
- Attack Patterns

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Node.js and npm
- pip package manager

### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Required packages:

- Flask (API server)
- Flask-CORS (cross-origin requests)
- transformers (Hugging Face)
- torch (PyTorch)

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install Node.js dependencies:

```bash
npm install
```

---

## Running the Application

### Start Backend Server

From the project root directory:

```bash
python backend/ner_api.py
```

The backend will:

- Load the Mini-CyBERT NER model
- Load the MLM model
- Start Flask server on http://localhost:5001

Wait for both models to load (approximately 20-30 seconds).

### Start Frontend Interface

In a new terminal, from the project root:

```bash
cd frontend
npm run dev
```

Access the application at: http://localhost:5173

---

## Using the Application

### NER Model (Named Entity Recognition)

1. Select "NER Model" in the interface
2. Enter cybersecurity text (e.g., vulnerability descriptions, threat reports)
3. Click "Analyze Text"
4. View extracted entities with their classifications

**Example Input:**

```
APT28 exploited CVE-2023-12345 in a phishing campaign targeting Windows systems.
```

**Example Output:**

- APT28: THREAT_ACTOR
- CVE-2023-12345: VULNERABILITY
- phishing: ATTACK_VECTOR
- Windows: SOFTWARE

### MLM Model (Masked Language Modeling)

1. Select "MLM Model" in the interface
2. Enter text with [MASK] token where you want predictions
3. Click "Analyze Text"
4. View top 5 word predictions

**Example Input:**

```
The attacker used a [MASK] exploit to gain access.
```

**Example Output:**

1. zero-day
2. remote
3. buffer
4. privilege
5. sql

---

## Project Structure

```
mini-cybert/
|
|-- backend/
|   |-- ner_api.py              # Flask API server
|   |-- requirements.txt         # Python dependencies
|
|-- frontend/
|   |-- src/
|   |   |-- App.jsx             # React application
|   |   |-- App.css             # Styling
|   |-- package.json            # Node.js dependencies
|
|-- scripts/
|   |-- 01_mlm_data_collection.py   # NVD data collection
|   |-- 02_mlm_data_cleaning.py     # Data preprocessing
|   |-- run_ner.py                  # NER inference script
|
|-- datasets/
|   |-- nvd/                    # Raw NVD data
|   |   |-- nvd_cves.json
|   |-- cyber/                  # Processed data
|       |-- corpus.txt          # MLM training corpus
|       |-- cyberner.csv        # NER training data
|
|-- models/
|   |-- mini_cybert_weights/
|       |-- mlm_final/          # MLM model weights
|       |-- mini_cybert_final/  # NER model weights
|
|-- README.md                   # This file
|-- SETUP_GUIDE.txt             # Detailed setup instructions
```

---

## Model Training

The Mini-CyBERT model was trained using the following process:

1. **Data Collection:** 10,000 CVE descriptions from NVD
2. **Vocabulary Extension:** Domain-specific terms added using TF-IDF
3. **MLM Pre-training:** Masked language modeling on cybersecurity corpus
4. **NER Fine-tuning:** Entity recognition on labeled cybersecurity entities

Training data sources:

- National Vulnerability Database (NVD)
- CyNER Dataset (Hugging Face)

---

## API Endpoints

### NER Endpoint

```
POST http://localhost:5001/api/ner/analyze
Content-Type: application/json

{
  "text": "your cybersecurity text here"
}
```

### MLM Endpoint

```
POST http://localhost:5001/api/mlm/predict
Content-Type: application/json

{
  "text": "text with [MASK] token"
}
```

### Health Check

```
GET http://localhost:5001/api/health
```

---

## Evaluation and Performance

The model has been evaluated on cybersecurity NER tasks and shows improved performance over generic BERT models for:

- Vulnerability identification
- Threat actor recognition
- Attack pattern classification
- Indicator of Compromise (IOC) extraction

---

## References

1. Ranade, P., Piplai, A., Joshi, A., & Finin, T. (2021). CyBERT: Contextualized Embeddings for the Cybersecurity Domain. IEEE Big Data.
2. Devlin, J., et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.
3. National Vulnerability Database (NVD). National Institute of Standards and Technology. https://nvd.nist.gov/

---

## License

This project is developed for academic research purposes.

## Contact

For questions or issues, please refer to the project documentation or contact the development team.

---

**Developed as part of Mini-CyBERT: Building a Lightweight Cybersecurity-Aware Language Model**

import { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';

function App() {
  const [selectedModel, setSelectedModel] = useState('ner'); // 'ner' or 'mlm'
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = 'http://localhost:5001';

  useEffect(() => {
    console.log('🚀 App Component Mounted!');
    console.log('API URL:', API_URL);
  }, []);

  const handleAnalyze = async () => {
    console.log('=== ANALYZE BUTTON CLICKED ===');
    console.log('Input Text:', inputText);
    console.log('Selected Model:', selectedModel);

    if (!inputText.trim()) {
      console.log('❌ Error: Empty text');
      setError('Please enter some text');
      return;
    }

    if (selectedModel === 'mlm' && !inputText.includes('[MASK]')) {
      console.log('❌ Error: MLM requires [MASK] token');
      setError('MLM model requires [MASK] token in the text');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    console.log('🔄 Loading started...');

    try {
      let endpoint = '';
      let requestBody = {};

      if (selectedModel === 'ner') {
        endpoint = `${API_URL}/api/ner/analyze`;
        requestBody = { text: inputText };
      } else {
        endpoint = `${API_URL}/api/mlm/predict`;
        requestBody = { text: inputText };
      }

      console.log('📡 Making request to:', endpoint);
      console.log('📦 Request body:', requestBody);

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      console.log('📨 Response status:', response.status);

      if (!response.ok) {
        console.log('❌ Response not OK');
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      console.log('✅ Response data:', data);
      
      // Filter out two-letter words from NER results
      if (selectedModel === 'ner' && data.entities) {
        // First filter by length
        data.entities = data.entities.filter(entity => {
          const word = (entity.word || '').trim().replace(/[.,;:!?]/g, '');
          return word.length > 2;
        });
        
        // Remove duplicates - keep only unique word + entity_type combinations
        const seen = new Set();
        data.entities = data.entities.filter(entity => {
          const key = `${entity.word.toLowerCase().trim()}|${entity.entity_type}`;
          if (seen.has(key)) {
            console.log('🔄 Removing duplicate:', entity.word, entity.entity_type);
            return false;
          }
          seen.add(key);
          return true;
        });
        
        data.entity_count = data.entities.length;
        console.log('✅ After deduplication, entity count:', data.entity_count);
        
        // Also filter sentence entities
        if (data.sentences) {
          data.sentences = data.sentences.map(sent => ({
            ...sent,
            entities: (sent.entities || []).filter(entity => {
              const word = (entity.word || '').trim().replace(/[.,;:!?]/g, '');
              return word.length > 2;
            })
          }));
        }
      }
      
      // Filter out two-letter words and duplicates from MLM predictions
      if (selectedModel === 'mlm' && data.predictions) {
        // Filter by length
        data.predictions = data.predictions.filter(word => {
          const cleanWord = (word || '').trim().replace(/[.,;:!?]/g, '');
          return cleanWord.length > 2;
        });
        
        // Remove duplicate predictions (case-insensitive)
        const uniquePredictions = [...new Set(data.predictions.map(w => w.toLowerCase()))];
        data.predictions = uniquePredictions;
        console.log('✅ Unique MLM predictions:', data.predictions.length);
      }
      
      console.log('✅ Setting result state');
      setResult(data);
    } catch (err) {
      console.error('❌ Error occurred:', err);
      setError(err.message);
    } finally {
      setLoading(false);
      console.log('✅ Loading finished');
    }
  };

  const getEntityColor = (entityType) => {
    const colors = {
      APT: '#e03131',
      THREAT_ACTOR: '#ff6b6b',
      MALWARE: '#ee5a6f',
      VULNERABILITY: '#f06595',
      TOOL: '#845ef7',
      EXPLOIT: '#cc5de8',
      METHOD: '#7950f2',
      CAMPAIGN: '#5c7cfa',
      INDICATOR: '#339af0',
      HASH: '#228be6',
      IP: '#15aabf',
      URL: '#12b886',
      FILE: '#40c057',
      SOFTWARE: '#82c91e',
      INFRASTRUCTURE: '#fab005',
    };
    return colors[entityType] || '#868e96';
  };

  const exampleTexts = {
    ner: [
      'APT28, also known as Fancy Bear, used phishing to exploit CVE-2023-12345.',
      'The ransomware Conti targeted healthcare using Microsoft Exchange vulnerabilities.',
      'Attackers exploited CVE-2021-44228 (Log4Shell) to gain network access.',
    ],
    mlm: [
      'The attacker used a [MASK] exploit to gain access.',
      'APT28 deployed [MASK] to steal credentials.',
      'The vulnerability allows remote [MASK] execution.',
      '... suggesting a [MASK] in the middle attack.',
    ],
  };

  return (
    <div className="app">
      <Header />
      
      <div className="container">
        <div className="main-content">
          <div className="card">
            <h2>Cybersecurity Text Analysis</h2>
            <p className="subtitle">Choose a model and analyze cybersecurity text</p>

            {/* Model Selection */}
            <div className="model-selection">
              <label className="radio-label">
                <input
                  type="radio"
                  value="ner"
                  checked={selectedModel === 'ner'}
                  onChange={(e) => {
                    console.log('📝 Model changed to:', e.target.value);
                    setSelectedModel(e.target.value);
                  }}
                />
                <span className="radio-text">
                  <strong>NER Model</strong> - Extract cybersecurity entities
                </span>
              </label>

              <label className="radio-label">
                <input
                  type="radio"
                  value="mlm"
                  checked={selectedModel === 'mlm'}
                  onChange={(e) => {
                    console.log('📝 Model changed to:', e.target.value);
                    setSelectedModel(e.target.value);
                  }}
                />
                <span className="radio-text">
                  <strong>MLM Model</strong> - Predict masked words (use [MASK])
                </span>
              </label>
            </div>

            {/* Input Section */}
            <div className="input-section">
              <label>
                {selectedModel === 'ner' ? 'Enter cybersecurity text:' : 'Enter text with [MASK]:'}
              </label>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={
                  selectedModel === 'ner'
                    ? 'e.g., APT28 exploited CVE-2023-12345 in a phishing campaign'
                    : 'e.g., The attacker used a [MASK] exploit to gain access'
                }
                rows={4}
              />

              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="analyze-btn"
              >
                {loading ? 'Analyzing...' : 'Analyze Text'}
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {/* Results Section */}
            {result && (
              <div className="results-section">
                {selectedModel === 'ner' ? (
                  // NER Results - Show only combined entities
                  <>
                    <h3>Detected Entities ({result.entity_count})</h3>
                    {result.entities && result.entities.length > 0 ? (
                      <div className="entities-grid">
                        {result.entities.map((entity, index) => (
                          <div
                            key={index}
                            className="entity-card"
                            style={{ borderLeftColor: getEntityColor(entity.entity_type) }}
                          >
                            <div className="entity-word">{entity.word}</div>
                            <div
                              className="entity-type"
                              style={{ backgroundColor: getEntityColor(entity.entity_type) }}
                            >
                              {entity.entity_type}
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p>No entities detected</p>
                    )}
                  </>
                ) : (
                  // MLM Results
                  <>
                    <h3>Predictions for [MASK]</h3>
                    {result.predictions && result.predictions.length > 0 ? (
                      <div className="predictions-list">
                        {result.predictions.map((pred, index) => (
                          <div key={index} className="prediction-item">
                            <span className="prediction-rank">{index + 1}</span>
                            <span className="prediction-word">{pred}</span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p>No predictions available</p>
                    )}
                  </>
                )}
              </div>
            )}

            {/* Example Texts */}
            <div className="examples-section">
              <h4>Example Texts:</h4>
              <div className="examples-grid">
                {exampleTexts[selectedModel].map((example, index) => (
                  <button
                    key={index}
                    onClick={() => setInputText(example)}
                    className="example-btn"
                  >
                    Example {index + 1}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

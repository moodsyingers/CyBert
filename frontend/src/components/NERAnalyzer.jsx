import { useState } from 'react';
import './NERAnalyzer.css';

const NERAnalyzer = () => {
  const [text, setText] = useState('');
  const [entities, setEntities] = useState([]);
  const [sentences, setSentences] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_URL = 'http://localhost:5001';

  const analyzeText = async () => {
    if (!text.trim()) {
      setError('Please enter some text');
      return;
    }

    setLoading(true);
    setError('');
    setEntities([]);
    setSentences([]);

    try {
      const response = await fetch(`${API_URL}/api/ner/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze text');
      }

      const data = await response.json();
      setEntities(data.entities || []);
      setSentences(data.sentences || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getEntityColor = (entityType) => {
    const colors = {
      THREAT_ACTOR: '#ff6b6b',
      MALWARE: '#ee5a6f',
      VULNERABILITY: '#f06595',
      ATTACK_VECTOR: '#cc5de8',
      TOOL: '#845ef7',
      SECTOR: '#5c7cfa',
      LOCATION: '#339af0',
    };
    return colors[entityType] || '#868e96';
  };

  return (
    <div className="ner-analyzer">
      <div className="ner-container">
        <h1>Cybersecurity Entity Recognition</h1>
        <p className="subtitle">Powered by Mini-CyBERT NER Model</p>

        <div className="input-section">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter cybersecurity text to analyze... (e.g., 'APT28 exploited CVE-2023-12345 in a phishing campaign')"
            rows={6}
          />
          
          <button 
            onClick={analyzeText} 
            disabled={loading}
            className="analyze-btn"
          >
            {loading ? 'Analyzing...' : 'Analyze Text'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {(entities.length > 0 || sentences.length > 0) && (
          <div className="results-section">
            {sentences.length > 1 && (
              <div className="sentences-breakdown">
                <h3>By sentence ({sentences.length} sentences)</h3>
                {sentences.map((sent, idx) => (
                  <div key={idx} className="sentence-block">
                    <span className="sentence-label">Sentence {idx + 1}:</span>
                    <span className="sentence-text">{sent.sentence.length > 80 ? sent.sentence.slice(0, 80) + '...' : sent.sentence}</span>
                    {sent.entities && sent.entities.length > 0 ? (
                      <div className="sentence-entities">
                        {sent.entities.map((e, i) => (
                          <span key={i} className="sentence-entity-tag" style={{ backgroundColor: getEntityColor(e.entity_type) + '40' }}>
                            {e.word} ({e.entity_type})
                          </span>
                        ))}
                      </div>
                    ) : (
                      <span className="no-entities">No entities</span>
                    )}
                  </div>
                ))}
              </div>
            )}
            <h2>Combined entities ({entities.length})</h2>
            
            <div className="entities-list">
              {entities.map((entity, index) => (
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

            <div className="highlighted-text">
              <h3>Highlighted Text</h3>
              <div className="text-display">
                {text.split('').map((char, index) => {
                  const entity = entities.find(
                    (e) => index >= e.start && index < e.end
                  );
                  
                  if (entity) {
                    return (
                      <span
                        key={index}
                        className="highlighted"
                        style={{ backgroundColor: getEntityColor(entity.entity_type) + '40' }}
                      >
                        {char}
                      </span>
                    );
                  }
                  return <span key={index}>{char}</span>;
                })}
              </div>
            </div>
          </div>
        )}

        <div className="examples-section">
          <h3>Example Texts</h3>
          <div className="examples">
            <button onClick={() => setText('APT28, also known as Fancy Bear, used phishing to exploit CVE-2023-12345.')}>
              Example 1
            </button>
            <button onClick={() => setText('The ransomware Conti targeted healthcare using Microsoft Exchange vulnerabilities.')}>
              Example 2
            </button>
            <button onClick={() => setText('Attackers exploited CVE-2021-44228 (Log4Shell) to gain network access.')}>
              Example 3
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NERAnalyzer;

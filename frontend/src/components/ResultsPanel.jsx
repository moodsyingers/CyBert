import { useState, useEffect } from 'react';

// Icons
const ResultIcons = {
  Threat: () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>,
  Info: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>,
  List: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>,
  Shield: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>,
  Check: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
};

function ResultsPanel({ prediction }) {
  const [attackInfo, setAttackInfo] = useState(null);

  useEffect(() => {
    if (prediction && prediction.attackType) {
      fetch(`http://localhost:5000/api/attack-info/${prediction.attackType}`)
        .then(res => res.json())
        .then(data => setAttackInfo(data))
        .catch(err => console.error('Failed to load attack info:', err));
    }
  }, [prediction]);

  if (!prediction) {
    return null;
  }

  const getSeverityColor = (severity) => {
    if (severity === 'Critical') return '#ef4444';
    if (severity === 'High') return '#f97316';
    return '#eab308';
  };

  return (
    <div className="card">
      <div className="card-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ 
            background: '#fee2e2', 
            padding: '8px', 
            borderRadius: '6px',
            color: '#ef4444'
          }}>
            <ResultIcons.Threat />
          </div>
          <div>
            <h3 className="card-title">Threat Analysis Report</h3>
            <span style={{ fontSize: '12px', color: '#64748b' }}>ID: {Math.random().toString(36).substr(2, 9).toUpperCase()}</span>
          </div>
        </div>
      </div>

      <div className="card-body">
        <div style={{ 
          padding: '20px', 
          background: '#f8fafc', 
          border: '1px solid #e2e8f0', 
          borderRadius: '8px',
          marginBottom: '32px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div>
            <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', marginBottom: '6px', fontWeight: '600' }}>Detected Threat</div>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#0f172a' }}>{prediction.attackType}</div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', marginBottom: '6px', fontWeight: '600' }}>Confidence Score</div>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#2563eb' }}>{prediction.confidence.toFixed(1)}%</div>
          </div>
        </div>

        <div style={{ marginBottom: '32px' }}>
          <h4 className="info-title"><ResultIcons.List /> Probability Distribution</h4>
          <ul className="probability-list">
            {Object.entries(prediction.probabilities).map(([type, prob]) => (
              <li key={type} className="probability-item">
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <span style={{ fontSize: '14px', fontWeight: '600', color: '#334155' }}>{type}</span>
                  <span style={{ fontSize: '14px', color: '#64748b', fontWeight: '500' }}>{prob.toFixed(1)}%</span>
                </div>
                <div className="probability-bar">
                  <div
                    className="probability-fill"
                    style={{ 
                      width: `${prob}%`,
                      background: type === prediction.attackType ? '#0f172a' : '#cbd5e1'
                    }}
                  ></div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        {attackInfo && (
          <>
            <div className="info-section">
              <h4 className="info-title"><ResultIcons.Info /> Description</h4>
              <p className="info-content">
                {attackInfo.description}
              </p>
            </div>

            <div className="info-section">
              <h4 className="info-title"><ResultIcons.Shield /> Indicators of Compromise</h4>
              <ul className="info-list">
                {attackInfo.indicators.map((indicator, index) => (
                  <li key={index} className="info-content">{indicator}</li>
                ))}
              </ul>
            </div>

            <div className="info-section">
              <h4 className="info-title"><ResultIcons.Check /> Severity Assessment</h4>
              <div style={{ 
                display: 'inline-flex', 
                alignItems: 'center',
                padding: '6px 16px',
                background: '#fff',
                border: `1px solid ${getSeverityColor(attackInfo.severity)}`,
                color: getSeverityColor(attackInfo.severity),
                borderRadius: '6px',
                fontSize: '13px',
                fontWeight: '700',
                boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
              }}>
                <span style={{ 
                  width: '8px', 
                  height: '8px', 
                  background: getSeverityColor(attackInfo.severity), 
                  borderRadius: '50%', 
                  marginRight: '10px' 
                }}></span>
                {attackInfo.severity.toUpperCase()}
              </div>
            </div>

            <div className="info-section">
              <h4 className="info-title"><ResultIcons.Shield /> Mitigation Steps</h4>
              <ul className="info-list">
                {attackInfo.mitigation.map((step, index) => (
                  <li key={index} className="info-content">{step}</li>
                ))}
              </ul>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ResultsPanel;

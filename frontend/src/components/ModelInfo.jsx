import { useState, useEffect } from 'react';

// Icons
const Icons = {
  Chip: () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>,
  Target: () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>,
  Activity: () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>,
  Layers: () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
};

function ModelInfo() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/model-info')
      .then(res => res.json())
      .then(data => setInfo(data))
      .catch(err => console.error('Failed to load model info:', err));
  }, []);

  if (!info) {
    return (
      <div className="card" style={{ padding: '24px', textAlign: 'center', color: '#64748b' }}>
        Loading model specifications...
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ 
            background: '#f1f5f9', 
            padding: '8px', 
            borderRadius: '6px',
            color: '#475569'
          }}>
            <Icons.Chip />
          </div>
          <div>
            <h3 className="card-title">Model Specifications</h3>
            <p className="card-subtitle">Active inference engine details</p>
          </div>
        </div>
        <div style={{ 
          background: '#dcfce7', 
          color: '#166534', 
          padding: '4px 12px', 
          borderRadius: '100px', 
          fontSize: '12px', 
          fontWeight: '600',
          display: 'flex',
          alignItems: 'center',
          gap: '6px'
        }}>
          <span style={{ width: '6px', height: '6px', background: '#166534', borderRadius: '50%' }}></span>
          ACTIVE
        </div>
      </div>

      <div className="card-body">
        {/* Main Metrics Grid */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(4, 1fr)', 
          gap: '20px',
          marginBottom: '32px'
        }}>
          <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ color: '#64748b', fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', marginBottom: '8px' }}>Accuracy</div>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#0f172a' }}>{(info.accuracy * 100).toFixed(1)}%</div>
            <div style={{ width: '100%', height: '4px', background: '#e2e8f0', marginTop: '8px', borderRadius: '2px' }}>
              <div style={{ width: `${info.accuracy * 100}%`, height: '100%', background: '#10b981', borderRadius: '2px' }}></div>
            </div>
          </div>

          <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ color: '#64748b', fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', marginBottom: '8px' }}>Precision</div>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#0f172a' }}>{(info.precision * 100).toFixed(1)}%</div>
            <div style={{ width: '100%', height: '4px', background: '#e2e8f0', marginTop: '8px', borderRadius: '2px' }}>
              <div style={{ width: `${info.precision * 100}%`, height: '100%', background: '#3b82f6', borderRadius: '2px' }}></div>
            </div>
          </div>

          <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ color: '#64748b', fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', marginBottom: '8px' }}>Recall</div>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#0f172a' }}>{(info.recall * 100).toFixed(1)}%</div>
            <div style={{ width: '100%', height: '4px', background: '#e2e8f0', marginTop: '8px', borderRadius: '2px' }}>
              <div style={{ width: `${info.recall * 100}%`, height: '100%', background: '#8b5cf6', borderRadius: '2px' }}></div>
            </div>
          </div>

          <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ color: '#64748b', fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', marginBottom: '8px' }}>F1 Score</div>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#0f172a' }}>{(info.f1_score * 100).toFixed(1)}%</div>
            <div style={{ width: '100%', height: '4px', background: '#e2e8f0', marginTop: '8px', borderRadius: '2px' }}>
              <div style={{ width: `${info.f1_score * 100}%`, height: '100%', background: '#f59e0b', borderRadius: '2px' }}></div>
            </div>
          </div>
        </div>

        {/* Details Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
          
          {/* Left Column: Configuration */}
          <div>
            <h4 style={{ 
              fontSize: '13px', 
              fontWeight: '700', 
              color: '#334155', 
              textTransform: 'uppercase', 
              marginBottom: '16px',
              display: 'flex', 
              alignItems: 'center', 
              gap: '8px' 
            }}>
              <Icons.Layers /> Configuration
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f8fafc', borderRadius: '6px' }}>
                <span style={{ color: '#64748b', fontSize: '13px', fontWeight: '500' }}>Algorithm</span>
                <span style={{ color: '#0f172a', fontWeight: '600', fontSize: '13px' }}>{info.type}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f8fafc', borderRadius: '6px' }}>
                <span style={{ color: '#64748b', fontSize: '13px', fontWeight: '500' }}>Estimators</span>
                <span style={{ color: '#0f172a', fontWeight: '600', fontSize: '13px' }}>{info.n_estimators} Trees</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f8fafc', borderRadius: '6px' }}>
                <span style={{ color: '#64748b', fontSize: '13px', fontWeight: '500' }}>Input Features</span>
                <span style={{ color: '#0f172a', fontWeight: '600', fontSize: '13px' }}>22 Parameters</span>
              </div>
            </div>
          </div>

          {/* Right Column: Capabilities */}
          <div>
            <h4 style={{ 
              fontSize: '13px', 
              fontWeight: '700', 
              color: '#334155', 
              textTransform: 'uppercase', 
              marginBottom: '16px',
              display: 'flex', 
              alignItems: 'center', 
              gap: '8px' 
            }}>
              <Icons.Target /> Detection Capabilities
            </h4>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {info.classes.map((cls, index) => (
                <div key={index} style={{
                  padding: '8px 16px',
                  background: '#fff',
                  border: '1px solid #e2e8f0',
                  borderRadius: '6px',
                  fontSize: '13px',
                  fontWeight: '600',
                  color: '#475569',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
                }}>
                  <span style={{ width: '6px', height: '6px', background: '#3b82f6', borderRadius: '50%' }}></span>
                  {cls}
                </div>
              ))}
            </div>
            <div style={{ marginTop: '16px', fontSize: '13px', color: '#64748b', lineHeight: '1.6' }}>
              This model is optimized for real-time traffic analysis, capable of distinguishing between benign activities and malicious attack patterns with high confidence.
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default ModelInfo;

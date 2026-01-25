import { useState } from 'react';

// Icons
const Icons = {
  Port: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect><rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>,
  Protocol: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>,
  Traffic: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>,
  Packet: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>,
  Alert: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>,
  Search: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
};

function DetectionForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    sourcePort: 12345,
    destinationPort: 80,
    protocol: 'TCP',
    trafficType: 'HTTP',
    packetType: 'Data',
    packetLength: 500,
    anomalyScore: 50,
    severity: 'Medium',
    hasAlert: true,
    hasIoC: false,
    signaturePatternA: false,
    signaturePatternB: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="card">
      <div className="card-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ 
            background: '#eff6ff', 
            padding: '8px', 
            borderRadius: '6px',
            color: '#2563eb'
          }}>
            <Icons.Search />
          </div>
          <div>
            <h2 className="card-title">Traffic Analysis Configuration</h2>
            <p className="card-subtitle">Define network parameters for threat detection</p>
          </div>
        </div>
      </div>

      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(4, 1fr)', 
            gap: '24px',
            marginBottom: '32px'
          }}>
            <div className="form-group">
              <label className="form-label"><Icons.Port /> Source Port</label>
              <input
                type="number"
                name="sourcePort"
                className="form-input"
                value={formData.sourcePort}
                onChange={handleChange}
                min="1"
                max="65535"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label"><Icons.Port /> Dest Port</label>
              <input
                type="number"
                name="destinationPort"
                className="form-input"
                value={formData.destinationPort}
                onChange={handleChange}
                min="1"
                max="65535"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label"><Icons.Protocol /> Protocol</label>
              <select
                name="protocol"
                className="form-select"
                value={formData.protocol}
                onChange={handleChange}
              >
                <option value="TCP">TCP</option>
                <option value="UDP">UDP</option>
                <option value="ICMP">ICMP</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label"><Icons.Traffic /> Traffic Type</label>
              <select
                name="trafficType"
                className="form-select"
                value={formData.trafficType}
                onChange={handleChange}
              >
                <option value="DNS">DNS</option>
                <option value="HTTP">HTTP</option>
                <option value="FTP">FTP</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label"><Icons.Packet /> Packet Type</label>
              <select
                name="packetType"
                className="form-select"
                value={formData.packetType}
                onChange={handleChange}
              >
                <option value="Control">Control</option>
                <option value="Data">Data</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label"><Icons.Alert /> Severity</label>
              <select
                name="severity"
                className="form-select"
                value={formData.severity}
                onChange={handleChange}
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">
                Packet Length <span className="range-value">{formData.packetLength} bytes</span>
              </label>
              <input
                type="range"
                name="packetLength"
                className="form-input"
                value={formData.packetLength}
                onChange={handleChange}
                min="64"
                max="1500"
                step="1"
                style={{ marginTop: '12px' }}
              />
            </div>

            <div className="form-group">
              <label className="form-label">
                Anomaly Score <span className="range-value">{formData.anomalyScore}%</span>
              </label>
              <input
                type="range"
                name="anomalyScore"
                className="form-input"
                value={formData.anomalyScore}
                onChange={handleChange}
                min="0"
                max="100"
                step="1"
                style={{ marginTop: '12px' }}
              />
            </div>
          </div>

          <div className="form-group" style={{ 
            background: '#f8fafc', 
            padding: '20px', 
            borderRadius: '8px', 
            border: '1px solid #e2e8f0',
            position: 'relative',
            overflow: 'hidden'
          }}>
            <div style={{ 
              position: 'absolute', 
              top: 0, 
              left: 0, 
              width: '4px', 
              height: '100%', 
              background: '#3b82f6' 
            }}></div>
            <label className="form-label" style={{ marginBottom: '16px', color: '#1e293b' }}>Detection Indicators</label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="hasAlert"
                  checked={formData.hasAlert}
                  onChange={handleChange}
                />
                Alert Triggered
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="hasIoC"
                  checked={formData.hasIoC}
                  onChange={handleChange}
                />
                IoC Detected
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="signaturePatternA"
                  checked={formData.signaturePatternA}
                  onChange={handleChange}
                />
                Pattern A Match
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="signaturePatternB"
                  checked={formData.signaturePatternB}
                  onChange={handleChange}
                />
                Pattern B Match
              </label>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '32px' }}>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
              style={{ 
                minWidth: '240px', 
                height: '48px',
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '10px'
              }}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  PROCESSING...
                </>
              ) : (
                <>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                  RUN THREAT ANALYSIS
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default DetectionForm;

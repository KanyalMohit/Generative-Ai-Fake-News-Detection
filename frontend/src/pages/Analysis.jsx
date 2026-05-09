import React, { useState, useEffect } from 'react';

const safeScore = (v) => {
  const n = Number(v);
  return Number.isFinite(n) ? Math.max(0, Math.min(100, n)) : 0;
};

function ConfidenceBar({ label, score }) {
  const s = safeScore(score);
  const cls = s > 70 ? 'good' : s > 40 ? 'mid' : 'bad';
  const color = s > 70 ? '#34d399' : s > 40 ? '#fbbf24' : '#f87171';
  return (
    <div className="bar-row">
      <div className="bar-header">
        <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>{label}</span>
        <span style={{ fontSize: '0.85rem', fontWeight: 700, color }}>{s}%</span>
      </div>
      <div className="bar-track">
        <div className={`bar-fill ${cls}`} style={{ width: `${s}%` }} />
      </div>
    </div>
  );
}

function BulletList({ items, emptyText }) {
  if (!items?.length) return <p style={{ fontSize: '0.875rem', color: '#475569', fontStyle: 'italic' }}>{emptyText}</p>;
  return (
    <ul className="bullet-list">
      {items.map((item, i) => (
        <li className="bullet-item" key={i}>
          <span className="bullet-num">{i + 1}</span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}

export default function Analysis() {
  const [mode, setMode] = useState('text');
  const [inputText, setInputText] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [polling, setPolling] = useState(false);

  const changeMode = (m) => {
    setMode(m);
    setResult(null);
    setError(null);
    setJobId(null);
    setFile(null);
    setInputText('');
  };

  useEffect(() => {
    if (!polling || !jobId) return;
    const API_BASE_URL = import.meta.env.VITE_API_URL || '/_/backend';
    const iv = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/analyze/video/${jobId}`);
        const data = await res.json();
        if (data.status === 'COMPLETED') {
          setResult(JSON.parse(data.result));
          setPolling(false);
          setLoading(false);
        } else if (data.status === 'FAILED') {
          setError(data.error || 'Video analysis failed.');
          setPolling(false);
          setLoading(false);
        }
      } catch {
        setError('Error checking video status.');
        setPolling(false);
        setLoading(false);
      }
    }, 3000);
    return () => clearInterval(iv);
  }, [polling, jobId]);

  const analyze = async () => {
    const API_BASE_URL = import.meta.env.VITE_API_URL || '/_/backend';
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      let endpoint, body, headers = {};
      if (mode === 'text') {
        endpoint = `${API_BASE_URL}/analyze/text`;
        body = JSON.stringify({ content: inputText });
        headers = { 'Content-Type': 'application/json' };
      } else if (mode === 'image') {
        endpoint = `${API_BASE_URL}/analyze/image`;
        const fd = new FormData();
        fd.append('file', file);
        body = fd;
      } else {
        endpoint = `${API_BASE_URL}/analyze/video`;
        const fd = new FormData();
        fd.append('file', file);
        body = fd;
      }
      const res = await fetch(endpoint, { method: 'POST', headers, body });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Analysis failed');
      if (mode === 'video') {
        setJobId(data.job_id);
        setPolling(true);
      } else {
        setResult(data);
        setLoading(false);
      }
    } catch (e) {
      setError(e.message);
      setLoading(false);
    }
  };

  const label = result?.label;
  const isDeepfake = result?.is_deepfake;
  const toneClass = label === 'REAL' ? 'real' : (label === 'FAKE' || isDeepfake) ? 'fake' : 'uncertain';
  const verdictText = label || (isDeepfake ? 'DEEPFAKE DETECTED' : result ? 'LIKELY AUTHENTIC' : '');

  const canRun = mode === 'text' ? inputText.trim().length >= 10 : !!file;

  return (
    <div className="page">
      <div className="analyze-page fade-in">
        <h1 className="page-title">Content Analysis Lab</h1>
        <p className="page-subtitle">Paste news text or upload an image — Satya AI will verify it.</p>

        {/* Mode tabs — text, image, video */}
        <div className="mode-tabs">
          {[
            { id: 'text', label: '📝 News Text' },
            { id: 'image', label: '🖼️ Image' },
            { id: 'video', label: '📹 Video' },
          ].map(m => (
            <button
              key={m.id}
              className={`mode-tab${mode === m.id ? ' active' : ''}`}
              onClick={() => changeMode(m.id)}
            >
              {m.label}
            </button>
          ))}
        </div>

        {/* Input card */}
        <div className="input-card">
          {mode === 'text' ? (
            <div style={{ position: 'relative' }}>
              <textarea
                className="content-textarea"
                placeholder="Paste a news article, headline, or claim here… (no URLs — text content only)"
                value={inputText}
                onChange={e => setInputText(e.target.value)}
              />
              <span style={{ position: 'absolute', bottom: '1rem', right: '1.25rem', fontSize: '0.7rem', color: '#334155', fontFamily: 'monospace' }}>
                {inputText.length} chars
              </span>
            </div>
          ) : (
            <div className="dropzone">
              <input
                type="file"
                accept={mode === 'image' ? 'image/*' : 'video/*'}
                onChange={e => setFile(e.target.files?.[0] || null)}
              />
              <div className="dropzone-icon">
                {mode === 'image' ? '🖼️' : '📹'}
              </div>
              {file ? (
                <div style={{ fontWeight: 700, color: '#818cf8', marginBottom: '0.25rem' }}>{file.name}</div>
              ) : (
                <>
                  <div style={{ fontWeight: 700, color: 'white', fontSize: '1.05rem', marginBottom: '0.375rem' }}>
                    Click or drag your {mode} here
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#475569' }}>
                    {mode === 'image' ? 'JPG, PNG, WEBP' : 'MP4, MOV, MKV'} · Max 50MB
                  </div>
                </>
              )}
            </div>
          )}

          <button
            className="run-btn"
            onClick={analyze}
            disabled={loading || !canRun}
          >
            {loading ? (
              <>
                <div className="spinner" />
                {polling ? 'Deep analysis in progress…' : 'Satya AI is thinking…'}
              </>
            ) : (
              <> ⚡ Run Satya Analysis</>
            )}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="error-box">
            <span>🚨</span>
            <div>
              <div style={{ fontWeight: 700, marginBottom: '0.25rem' }}>Analysis Error</div>
              <div style={{ fontSize: '0.875rem', opacity: 0.8 }}>{error}</div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="fade-in">
            {/* Verdict banner */}
            <div className={`verdict-banner ${toneClass}`}>
              <div className={`verdict-label ${toneClass}`}>
                {toneClass === 'real' ? '✅' : toneClass === 'fake' ? '🚨' : '⚠️'} Official Verdict
              </div>
              <h2 className={`verdict-heading ${toneClass}`}>{verdictText}</h2>
              <p className="verdict-summary">
                {result.summary || result.final_reasoning || result.verdict_explanation}
              </p>
            </div>

            {/* Metrics + insights */}
            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-label">📊 Neural Metrics</div>
                <ConfidenceBar label="AI Confidence" score={result.confidence || result.confidence_score} />
                {result.credibility_analysis && (
                  <ConfidenceBar label="Source Reliability" score={result.credibility_analysis.credibility_score} />
                )}
                <div style={{ marginTop: '1rem', padding: '0.875rem', background: 'rgba(255,255,255,0.03)', borderRadius: '0.75rem', fontSize: '0.75rem', color: '#475569', lineHeight: 1.6 }}>
                  Metrics reflect semantic consistency, source signals, and evidence quality.
                </div>
              </div>

              <div className="metric-card">
                <div className="metric-label">🔬 Forensic Insights</div>
                {mode === 'video' ? (
                  <>
                    <div style={{ fontWeight: 700, color: 'white', marginBottom: '0.5rem', fontSize: '0.875rem' }}>Visual Anomalies</div>
                    <BulletList items={result.visual_anomalies} emptyText="No visual synthetic markers detected." />
                    <div style={{ height: '1px', background: 'rgba(255,255,255,0.05)', margin: '1rem 0' }} />
                    <div style={{ fontWeight: 700, color: 'white', marginBottom: '0.5rem', fontSize: '0.875rem' }}>Audio Fingerprint</div>
                    <BulletList items={result.audio_anomalies} emptyText="Audio stream consistent with original." />
                  </>
                ) : (
                  <>
                    <div style={{ fontWeight: 700, color: 'white', marginBottom: '0.5rem', fontSize: '0.875rem' }}>Source Reputation</div>
                    <p style={{ fontSize: '0.875rem', color: '#94a3b8', background: 'rgba(255,255,255,0.03)', padding: '0.875rem', borderRadius: '0.75rem', lineHeight: 1.6, marginBottom: '1rem' }}>
                      {result.credibility_analysis?.source_reputation || 'Source evaluation indicates neutral historical reliability.'}
                    </p>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                      <div style={{ padding: '0.875rem', background: 'rgba(99,102,241,0.06)', border: '1px solid rgba(99,102,241,0.1)', borderRadius: '0.875rem', textAlign: 'center' }}>
                        <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#818cf8' }}>{result.detected_claims?.length || 0}</div>
                        <div style={{ fontSize: '0.65rem', color: '#475569', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em' }}>Claims Found</div>
                      </div>
                      <div style={{ padding: '0.875rem', background: 'rgba(139,92,246,0.06)', border: '1px solid rgba(139,92,246,0.1)', borderRadius: '0.875rem', textAlign: 'center' }}>
                        <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#a78bfa' }}>{result.citations?.length || 0}</div>
                        <div style={{ fontSize: '0.65rem', color: '#475569', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em' }}>References</div>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Evidence grid */}
            {mode !== 'video' && (
              <>
                <div className="info-grid">
                  <div className="info-card">
                    <div className="info-card-title">🧠 Detected Claims</div>
                    <BulletList items={result.detected_claims} emptyText="No explicit claims extracted." />
                  </div>
                  <div className="info-card">
                    <div className="info-card-title">🗺️ Verification Strategy</div>
                    <BulletList items={result.verification_strategy} emptyText="Strategy auto-selected based on content type." />
                  </div>
                </div>

                <div className="info-grid">
                  <div className="info-card">
                    <div className="info-card-title">✅ Supporting Evidence</div>
                    <BulletList items={result.evidence_for} emptyText="No strong supporting evidence found." />
                  </div>
                  <div className="info-card">
                    <div className="info-card-title">🚫 Contradicting Evidence</div>
                    <BulletList items={result.evidence_against} emptyText="No direct contradictions found." />
                  </div>
                </div>

                {/* Reasoning */}
                <div className="reasoning-card">
                  <h3 style={{ fontWeight: 800, color: 'white', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    🧾 Deep Reasoning
                  </h3>
                  <p className="reasoning-quote">
                    "{result.final_reasoning || 'Conclusion based on weighted cross-referenced evidence.'}"
                  </p>
                  <div className="recommendation-box">
                    <div className="rec-label">⚡ System Recommendation</div>
                    <p className="rec-text">
                      {result.recommended_user_action || 'Verify through primary sources before sharing.'}
                    </p>
                  </div>
                </div>

                {/* Uncertainty notes */}
                {result.uncertainty_notes?.length > 0 && (
                  <div className="info-card" style={{ marginBottom: '1.5rem' }}>
                    <div className="info-card-title">🫥 Uncertainty Notes</div>
                    <BulletList items={result.uncertainty_notes} emptyText="" />
                  </div>
                )}
              </>
            )}

            {/* Sources */}
            {(result.citations || []).length > 0 && (
              <div className="sources-card">
                <div className="metric-label">🔗 Evidence Log</div>
                <div className="sources-grid">
                  {result.citations.map((cite, i) => {
                    const url = cite?.url || cite;
                    const snippet = cite?.snippet;
                    return (
                      <a key={i} href={url} target="_blank" rel="noopener noreferrer" className="source-item">
                        <div className="source-header">
                          <span className="source-badge">Source #{i + 1}</span>
                          <span style={{ color: '#475569', fontSize: '0.75rem' }}>↗</span>
                        </div>
                        <div className="source-url">{url}</div>
                        {snippet && <p className="source-snippet">{snippet}</p>}
                      </a>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

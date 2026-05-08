import React from 'react';
import { Link } from 'react-router-dom';

const features = [
  {
    icon: '🧠',
    title: 'LLM-Powered Reasoning',
    desc: 'Google Gemini analyzes semantic context, logical fallacies, and narrative bias in any piece of content.',
  },
  {
    icon: '🌐',
    title: 'Real-Time Web Search',
    desc: 'Perplexity AI cross-references claims against live global news databases for evidence-backed verdicts.',
  },
  {
    icon: '🎭',
    title: 'Deepfake Detection',
    desc: 'Advanced visual and audio forensics identify pixel-level anomalies in AI-generated or manipulated media.',
  },
];

const checks = [
  { title: 'Evidence-Based Reports', desc: 'Every verdict is backed by citations and direct links to primary sources.' },
  { title: 'Multi-Modal Support', desc: 'Analyze text, social media URLs, uploaded images, and video files in one place.' },
  { title: 'Explainable AI', desc: 'We surface the exact reasoning chain, not just a score, so you can judge for yourself.' },
];

export default function Home() {
  return (
    <div className="page fade-in">
      {/* ── Hero ── */}
      <section className="hero">
        <span className="hero-badge">⚡ Satya — AI Fake News Detection</span>

        <h1 className="hero-title">
          Stop Misinformation <br />
          with <span className="text-gradient">Project Satya</span>
        </h1>

        <p className="hero-subtitle">
          GenAI-powered verification for text, images, and deepfake video.
          Get confidence scores, evidence trails, and actionable recommendations in seconds.
        </p>

        <div className="hero-ctas">
          <Link to="/analyze">
            <button className="btn-primary" style={{ fontSize: '1.05rem', padding: '0.875rem 2rem' }}>
              🔬 Start Analyzing →
            </button>
          </Link>
          <Link to="/about">
            <button className="btn-ghost" style={{ fontSize: '1.05rem', padding: '0.875rem 2rem' }}>
              How it Works
            </button>
          </Link>
        </div>
      </section>

      {/* ── Features ── */}
      <section style={{ paddingBottom: '3rem' }}>
        <div className="features-grid">
          {features.map((f) => (
            <div className="feature-card" key={f.title}>
              <div className="feature-icon">{f.icon}</div>
              <h3 className="feature-title">{f.title}</h3>
              <p className="feature-desc">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Why Satya ── */}
      <section className="why-section">
        <div className="why-inner">
          <div>
            <h2 style={{ fontSize: '2rem', fontWeight: 800, color: 'white', letterSpacing: '-0.03em', marginBottom: '2rem' }}>
              Why trust <span className="text-gradient">Satya</span>?
            </h2>
            {checks.map((c) => (
              <div className="why-check" key={c.title}>
                <div className="why-check-dot">✓</div>
                <div>
                  <div style={{ fontWeight: 700, color: 'white', marginBottom: '0.25rem' }}>{c.title}</div>
                  <div style={{ fontSize: '0.9rem', color: '#64748b' }}>{c.desc}</div>
                </div>
              </div>
            ))}
          </div>
          <div style={{ position: 'relative' }}>
            <div
              className="glass"
              style={{
                borderRadius: '1.5rem',
                padding: '2rem',
                transform: 'rotate(2deg)',
              }}
            >
              {/* Mini verdict preview */}
              <div style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{ width: '0.75rem', height: '0.75rem', borderRadius: '50%', background: '#10b981' }} />
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#34d399', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Live Result Preview</span>
              </div>
              <div style={{ fontSize: '2rem', fontWeight: 900, color: '#34d399', letterSpacing: '-0.04em', marginBottom: '0.5rem' }}>REAL</div>
              <div style={{ fontSize: '0.9rem', color: '#64748b', lineHeight: 1.6, marginBottom: '1rem' }}>
                This article's core claims are consistent with verified reporting from multiple credible sources.
              </div>
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <div style={{ flex: 1, padding: '0.75rem', background: 'rgba(16,185,129,0.1)', borderRadius: '0.75rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#34d399' }}>94%</div>
                  <div style={{ fontSize: '0.65rem', color: '#475569', fontWeight: 700, textTransform: 'uppercase' }}>Confidence</div>
                </div>
                <div style={{ flex: 1, padding: '0.75rem', background: 'rgba(99,102,241,0.1)', borderRadius: '0.75rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#818cf8' }}>8</div>
                  <div style={{ fontSize: '0.65rem', color: '#475569', fontWeight: 700, textTransform: 'uppercase' }}>Citations</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="cta-strip">
        <h2 style={{ fontSize: '2.5rem', fontWeight: 900, color: 'white', letterSpacing: '-0.04em', marginBottom: '1rem' }}>
          Ready to reveal the truth?
        </h2>
        <p style={{ color: '#64748b', marginBottom: '2.5rem', fontSize: '1.05rem' }}>
          Join the fight against misinformation. Free to use, powered by cutting-edge AI.
        </p>
        <Link to="/analyze">
          <button className="btn-primary" style={{ fontSize: '1.1rem', padding: '1rem 2.5rem' }}>
            🔬 Try Satya Now
          </button>
        </Link>
      </section>
    </div>
  );
}

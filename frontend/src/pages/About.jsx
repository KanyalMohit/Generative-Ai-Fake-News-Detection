import React from 'react';
import { Link } from 'react-router-dom';

const steps = [
  { icon: '📥', title: 'Content Extraction', desc: 'Core claims are extracted from text, OCR\'d from images, or pulled from video transcripts and keyframes.' },
  { icon: '🧠', title: 'Semantic Analysis', desc: 'Gemini Pro inspects logical consistency, emotional manipulation markers, and narrative bias in the content.' },
  { icon: '🌐', title: 'Real-Time Cross-Verification', desc: 'Perplexity AI queries a live index of trusted news outlets, research papers, and official databases.' },
  { icon: '🔬', title: 'Forensic Detection', desc: 'For media, pixel-level frequency analysis and audio waveform inspection detect AI generation artifacts.' },
];

export default function About() {
  return (
    <div className="page">
      <div className="about-page fade-in">
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
          <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3rem)', fontWeight: 900, color: 'white', letterSpacing: '-0.04em', marginBottom: '1rem' }}>
            About <span className="text-gradient">Project Satya</span>
          </h1>
          <p style={{ fontSize: '1.1rem', color: '#64748b', maxWidth: '40rem', margin: '0 auto', lineHeight: 1.7 }}>
            Satya (Sanskrit: सत्य) means <strong style={{ color: '#94a3b8' }}>"Truth"</strong>. Our mission is to be the 
            last line of defence against the wave of AI-generated misinformation.
          </p>
        </div>

        {/* Mission + Tech cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginBottom: '4rem' }}>
          <div className="glass" style={{ borderRadius: '1.5rem', padding: '2rem' }}>
            <div style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>🎯</div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'white', marginBottom: '0.875rem' }}>The Mission</h2>
            <p style={{ fontSize: '0.9rem', color: '#64748b', lineHeight: 1.7 }}>
              In an era where deepfakes and AI content can reach millions in seconds, 
              manual fact-checking doesn't scale. Satya provides automated, explainable 
              verification for everyone — not just journalists.
            </p>
          </div>
          <div className="glass" style={{ borderRadius: '1.5rem', padding: '2rem' }}>
            <div style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>⚙️</div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'white', marginBottom: '0.875rem' }}>The Technology</h2>
            <p style={{ fontSize: '0.9rem', color: '#64748b', lineHeight: 1.7 }}>
              Satya combines Google Gemini's reasoning capabilities with Perplexity AI's 
              real-time retrieval system and custom computer-vision pipelines to deliver 
              comprehensive, evidence-backed verdicts.
            </p>
          </div>
        </div>

        {/* Pipeline */}
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'white', letterSpacing: '-0.03em', marginBottom: '0.5rem', textAlign: 'center' }}>
          The Verification Pipeline
        </h2>
        <p style={{ color: '#64748b', textAlign: 'center', marginBottom: '0', fontSize: '0.925rem' }}>
          Every analysis passes through four sequential intelligence layers.
        </p>

        <div className="pipeline-steps">
          {steps.map((s, i) => (
            <div className="pipeline-step" key={i}>
              <div className="step-icon">{s.icon}</div>
              <div>
                <div style={{ fontSize: '0.65rem', fontWeight: 800, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#6366f1', marginBottom: '0.25rem' }}>
                  Step {i + 1}
                </div>
                <div className="step-title">{s.title}</div>
                <div className="step-desc">{s.desc}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Open source CTA */}
        <div
          className="glass"
          style={{
            borderRadius: '1.5rem',
            padding: '3rem 2rem',
            textAlign: 'center',
            marginTop: '4rem',
            border: '1px solid rgba(99,102,241,0.15)',
            background: 'rgba(99,102,241,0.04)',
          }}
        >
          <h3 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'white', marginBottom: '0.875rem' }}>
            Open Source & Transparent
          </h3>
          <p style={{ color: '#64748b', maxWidth: '36rem', margin: '0 auto 2rem', lineHeight: 1.7, fontSize: '0.925rem' }}>
            Tools that define what is "true" must themselves be transparent. 
            Satya is built with open architectures and verifiable reasoning.
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button className="btn-ghost">View Source Code</button>
            <Link to="/analyze">
              <button className="btn-primary">🔬 Try It Now</button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

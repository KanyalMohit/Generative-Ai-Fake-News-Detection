import React from 'react';
import { Routes, Route, useLocation, Link, NavLink } from 'react-router-dom';
import Home from './pages/Home';
import Analysis from './pages/Analysis';
import About from './pages/About';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="logo">
          <div className="logo-icon">S</div>
          <span className="logo-text">Satya</span>
        </Link>

        <ul className="nav-links">
          <li>
            <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
              🏠 Home
            </NavLink>
          </li>
          <li>
            <NavLink to="/analyze" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
              🔬 Analyze
            </NavLink>
          </li>
          <li>
            <NavLink to="/about" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
              ℹ️ About
            </NavLink>
          </li>
        </ul>

        <Link to="/analyze">
          <button className="btn-primary" style={{ padding: '0.5rem 1.25rem', fontSize: '0.85rem' }}>
            Get Started →
          </button>
        </Link>
      </div>
    </nav>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="logo" style={{ textDecoration: 'none' }}>
          <div className="logo-icon" style={{ width: '1.75rem', height: '1.75rem', fontSize: '0.8rem' }}>S</div>
          <span className="logo-text" style={{ fontSize: '1.1rem' }}>Satya</span>
        </div>
        <p className="footer-copy">© {new Date().getFullYear()} Project Satya — Engineered for Digital Integrity</p>
        <div className="footer-links">
          <a href="#" className="footer-link">Docs</a>
          <a href="#" className="footer-link">Privacy</a>
          <a href="#" className="footer-link">GitHub</a>
        </div>
      </div>
    </footer>
  );
}

function App() {
  return (
    <div style={{ minHeight: '100vh', position: 'relative' }}>
      {/* Ambient blobs */}
      <div className="blob blob-tl" />
      <div className="blob blob-br" />

      <Navbar />

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analyze" element={<Analysis />} />
          <Route path="/about" element={<About />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

export default App;

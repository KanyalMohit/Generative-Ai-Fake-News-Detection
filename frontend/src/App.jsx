import React from 'react';
import Detector from './components/Detector';

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 py-12 px-4 selection:bg-indigo-100 selection:text-indigo-900">
      <div className="max-w-5xl mx-auto text-center mb-12">
        <h1 className="text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 mb-4 tracking-tight">
          Truth Lens
        </h1>
        <p className="text-xl text-slate-500 font-light max-w-2xl mx-auto">
          Advanced AI-powered verification for Text, Images, and Deepfake Video detection.
        </p>
      </div>

      <Detector />

      <div className="max-w-2xl mx-auto mt-16 text-center text-slate-400 text-sm">
        <p>© {new Date().getFullYear()} Truth Lens. Powered by Gemini Pro Vision & Perplexity Sonar.</p>
      </div>
    </div>
  );
}

export default App;

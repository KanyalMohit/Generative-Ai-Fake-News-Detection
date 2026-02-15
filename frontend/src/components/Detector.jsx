import React, { useState, useEffect } from 'react';

const Detector = () => {
    const [mode, setMode] = useState('text'); // text, image, video
    const [inputText, setInputText] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [jobId, setJobId] = useState(null);
    const [polling, setPolling] = useState(false);

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setSelectedFile(e.target.files[0]);
        }
    };

    // Polling Logic for Video
    useEffect(() => {
        let interval;
        if (polling && jobId) {
            interval = setInterval(async () => {
                try {
                    const response = await fetch(`http://localhost:8000/analyze/video/${jobId}`);
                    const data = await response.json();

                    if (data.status === 'COMPLETED') {
                        setResult(JSON.parse(data.result)); // Parse the stringified JSON result
                        setPolling(false);
                        setLoading(false);
                    } else if (data.status === 'FAILED') {
                        setError(data.error || 'Video analysis failed.');
                        setPolling(false);
                        setLoading(false);
                    }
                    // If 'QUEUED' or 'PROCESSING', continue polling
                } catch (err) {
                    console.error("Polling error", err);
                    setError("Error checking status");
                    setPolling(false);
                    setLoading(false);
                }
            }, 3000); // Check every 3 seconds
        }
        return () => clearInterval(interval);
    }, [polling, jobId]);

    const handleAnalyze = async () => {
        setLoading(true);
        setError(null);
        setResult(null);
        setJobId(null);

        try {
            let endpoint = '';
            let body;
            let headers = {};

            if (mode === 'text') {
                endpoint = 'http://localhost:8000/analyze/text';
                const isUrl = inputText.trim().startsWith('http');
                body = JSON.stringify({ content: inputText, is_url: isUrl });
                headers = { 'Content-Type': 'application/json' };
            } else if (mode === 'image') {
                endpoint = 'http://localhost:8000/analyze/image';
                const formData = new FormData();
                formData.append('file', selectedFile);
                body = formData;
            } else if (mode === 'video') {
                endpoint = 'http://localhost:8000/analyze/video';
                const formData = new FormData();
                formData.append('file', selectedFile);
                body = formData;
            }

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: headers,
                body: body
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Analysis failed');
            }

            if (mode === 'video') {
                // Video returns a Job ID
                setJobId(data.job_id);
                setPolling(true);
                // Loading stays true until polling finishes
            } else {
                setResult(data);
                setLoading(false);
            }

        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    const renderConfidenceBar = (score, label) => (
        <div className="mb-4">
            <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-slate-700">{label}</span>
                <span className="text-sm font-medium text-slate-700">{score}%</span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2.5">
                <div
                    className={`h-2.5 rounded-full ${score > 70 ? 'bg-green-600' : score > 40 ? 'bg-yellow-400' : 'bg-red-600'}`}
                    style={{ width: `${score}%` }}
                ></div>
            </div>
        </div>
    );

    return (
        <div className="max-w-4xl mx-auto p-8 bg-white rounded-2xl shadow-xl border border-slate-100">
            {/* Mode Switcher */}
            <div className="flex mb-8 p-1 bg-slate-100 rounded-xl">
                {['text', 'image', 'video'].map((m) => (
                    <button
                        key={m}
                        onClick={() => { setMode(m); setResult(null); setError(null); setJobId(null); }}
                        className={`flex-1 capitalize py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 ${mode === m
                                ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-slate-200'
                                : 'text-slate-500 hover:text-slate-700'
                            }`}
                    >
                        {m} Analysis
                    </button>
                ))}
            </div>

            {/* Input Area */}
            <div className="mb-8">
                {mode === 'text' ? (
                    <textarea
                        className="w-full p-6 bg-slate-50 border border-slate-200 rounded-xl text-slate-800 placeholder:text-slate-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all min-h-[200px] text-lg resize-y"
                        placeholder="Paste news text, a claim, or an article URL here..."
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                    />
                ) : (
                    <div className="group relative border-2 border-dashed border-slate-300 rounded-xl p-12 text-center hover:bg-slate-50 hover:border-indigo-400 transition-all cursor-pointer">
                        <input
                            type="file"
                            accept={mode === 'image' ? "image/*" : "video/*"}
                            onChange={handleFileChange}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        />
                        <div className="pointer-events-none">
                            <span className="text-4xl block mb-3 group-hover:scale-110 transition-transform">
                                {mode === 'image' ? '🖼️' : '📹'}
                            </span>
                            {selectedFile ? (
                                <div className="text-indigo-600 font-semibold bg-indigo-50 px-4 py-2 rounded-lg inline-block">
                                    {selectedFile.name}
                                </div>
                            ) : (
                                <div className="text-slate-500">
                                    <p className="font-medium text-slate-700 mb-1">Click or drag {mode} here</p>
                                    <p className="text-sm opacity-75">Supports {mode === 'image' ? 'JPG, PNG' : 'MP4, MOV'}</p>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>

            {/* Analyze Button */}
            <button
                onClick={handleAnalyze}
                disabled={loading || (mode === 'text' && !inputText) || (mode !== 'text' && !selectedFile)}
                className="w-full py-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-bold rounded-xl shadow-lg shadow-indigo-200 transition-all transform active:scale-[0.99] text-lg"
            >
                {loading ? (
                    <span className="flex items-center justify-center space-x-2">
                        <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <span>{polling ? 'Processing Video (This takes time)...' : 'Analyzing Content...'}</span>
                    </span>
                ) : 'Run Analysis'}
            </button>

            {/* Error Message */}
            {error && (
                <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-r-lg">
                    <strong className="font-bold block mb-1">Analysis Failed</strong>
                    {error}
                </div>
            )}

            {/* Results Display */}
            {result && (
                <div className="mt-12 animate-fade-in space-y-8">
                    {/* Header Card */}
                    <div className={`p-6 rounded-2xl border-l-8 shadow-sm ${result.label === 'REAL' ? 'bg-green-50 border-green-500 text-green-900' :
                            result.label === 'FAKE' || result.is_deepfake ? 'bg-red-50 border-red-500 text-red-900' :
                                'bg-yellow-50 border-yellow-500 text-yellow-900'
                        }`}>
                        <div className="flex items-center justify-between mb-2">
                            <h2 className="text-3xl font-extrabold uppercase tracking-wide">
                                {result.label || (result.is_deepfake ? "DEEPFAKE DETECTED" : "LIKELY AUTHENTIC")}
                            </h2>
                            <span className="text-4xl">
                                {result.label === 'REAL' ? '✅' :
                                    result.label === 'FAKE' || result.is_deepfake ? '🚨' : '⚠️'}
                            </span>
                        </div>
                        <p className="text-lg opacity-90 leading-relaxed font-medium">
                            {result.summary || result.verdict_explanation || result.short_explanation}
                        </p>
                    </div>

                    {/* Stats Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-slate-50 p-6 rounded-xl border border-slate-100">
                            <h3 className="text-slate-500 text-xs font-bold uppercase tracking-wider mb-4">Metrics</h3>
                            {renderConfidenceBar(result.confidence || result.confidence_score, "Confidence Score")}
                            {result.credibility_analysis && renderConfidenceBar(result.credibility_analysis.credibility_score || 0, "Source Credibility")}
                        </div>

                        {/* Credibility / Visual Anomalies */}
                        <div className="bg-slate-50 p-6 rounded-xl border border-slate-100">
                            <h3 className="text-slate-500 text-xs font-bold uppercase tracking-wider mb-4">
                                {mode === 'video' ? 'Anomalies Detected' : 'Source Reputation'}
                            </h3>
                            {mode === 'video' ? (
                                <ul className="list-disc list-inside space-y-2 text-sm text-slate-700">
                                    {(result.visual_anomalies || []).map((a, i) => <li key={i}>{a}</li>)}
                                    {(result.audio_anomalies || []).map((a, i) => <li key={i}>Sound: {a}</li>)}
                                    {!result.visual_anomalies?.length && !result.audio_anomalies?.length && (
                                        <li className="text-green-600">No significant anomalies found.</li>
                                    )}
                                </ul>
                            ) : (
                                <p className="text-slate-700 leading-relaxed">
                                    {result.credibility_analysis?.source_reputation || "No source reputation data available."}
                                </p>
                            )}
                        </div>
                    </div>

                    {/* Key Facts / Cross Verification (Text Mode Only) */}
                    {mode !== 'video' && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="bg-white p-6 rounded-xl border border-slate-100 shadow-sm">
                                <h3 className="text-indigo-600 font-bold mb-4 flex items-center">
                                    <span className="mr-2">💡</span> Key Facts
                                </h3>
                                <ul className="space-y-3">
                                    {(result.key_facts || []).map((fact, i) => (
                                        <li key={i} className="flex items-start text-slate-700 text-sm">
                                            <span className="bg-indigo-100 text-indigo-700 rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold mr-3 flex-shrink-0 mt-0.5">{i + 1}</span>
                                            {fact}
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            <div className="bg-white p-6 rounded-xl border border-slate-100 shadow-sm">
                                <h3 className="text-indigo-600 font-bold mb-4 flex items-center">
                                    <span className="mr-2">⚖️</span> Cross Verification
                                </h3>
                                <div className="space-y-4 text-sm">
                                    <div>
                                        <span className="block text-slate-500 font-semibold mb-1">Common Points:</span>
                                        <p className="text-slate-700">{result.cross_verification?.common_points || "N/A"}</p>
                                    </div>
                                    <div>
                                        <span className="block text-slate-500 font-semibold mb-1">Discrepancies:</span>
                                        <p className="text-slate-700">{result.cross_verification?.discrepancies || "N/A"}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Citations Card */}
                    {(result.citations || []).length > 0 && (
                        <div className="bg-slate-50 p-6 rounded-xl border border-slate-100">
                            <h3 className="text-slate-500 text-xs font-bold uppercase tracking-wider mb-4">Sources</h3>
                            <div className="grid gap-3">
                                {result.citations.map((cite, i) => (
                                    <a
                                        key={i}
                                        href={cite.url || cite}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center p-3 bg-white hover:bg-indigo-50 border border-slate-200 rounded-lg transition-colors group"
                                    >
                                        <span className="text-xl mr-3 group-hover:scale-110 transition-transform">🔗</span>
                                        <div className="overflow-hidden">
                                            <div className="text-sm font-semibold text-indigo-600 truncate">{cite.url || cite}</div>
                                            {cite.snippet && <div className="text-xs text-slate-500 truncate mt-0.5">{cite.snippet}</div>}
                                        </div>
                                    </a>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Detector;

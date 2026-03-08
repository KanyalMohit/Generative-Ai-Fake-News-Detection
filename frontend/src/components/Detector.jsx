import React, { useState, useEffect } from 'react';

const safeScore = (value) => {
    const num = Number(value);
    return Number.isFinite(num) ? Math.max(0, Math.min(100, num)) : 0;
};

const SectionCard = ({ title, icon, children }) => (
    <div className="bg-white p-6 rounded-xl border border-slate-100 shadow-sm">
        <h3 className="text-indigo-600 font-bold mb-4 flex items-center">
            <span className="mr-2">{icon}</span> {title}
        </h3>
        {children}
    </div>
);

const BulletList = ({ items, emptyText }) => (
    items?.length ? (
        <ul className="space-y-3">
            {items.map((item, index) => (
                <li key={index} className="flex items-start text-slate-700 text-sm">
                    <span className="bg-indigo-100 text-indigo-700 rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold mr-3 flex-shrink-0 mt-0.5">{index + 1}</span>
                    <span>{item}</span>
                </li>
            ))}
        </ul>
    ) : (
        <p className="text-sm text-slate-500">{emptyText}</p>
    )
);

const Detector = () => {
    const [mode, setMode] = useState('text');
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

    useEffect(() => {
        let interval;
        if (polling && jobId) {
            interval = setInterval(async () => {
                try {
                    const response = await fetch(`http://localhost:8000/analyze/video/${jobId}`);
                    const data = await response.json();

                    if (data.status === 'COMPLETED') {
                        setResult(JSON.parse(data.result));
                        setPolling(false);
                        setLoading(false);
                    } else if (data.status === 'FAILED') {
                        setError(data.error || 'Video analysis failed.');
                        setPolling(false);
                        setLoading(false);
                    }
                } catch (err) {
                    console.error('Polling error', err);
                    setError('Error checking status');
                    setPolling(false);
                    setLoading(false);
                }
            }, 3000);
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
                headers,
                body
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Analysis failed');
            }

            if (mode === 'video') {
                setJobId(data.job_id);
                setPolling(true);
            } else {
                setResult(data);
                setLoading(false);
            }
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    const renderConfidenceBar = (score, label) => {
        const safe = safeScore(score);
        return (
            <div className="mb-4">
                <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-slate-700">{label}</span>
                    <span className="text-sm font-medium text-slate-700">{safe}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2.5">
                    <div
                        className={`h-2.5 rounded-full ${safe > 70 ? 'bg-green-600' : safe > 40 ? 'bg-yellow-400' : 'bg-red-600'}`}
                        style={{ width: `${safe}%` }}
                    ></div>
                </div>
            </div>
        );
    };

    const verdict = result?.label || (result?.is_deepfake ? 'DEEPFAKE DETECTED' : 'LIKELY AUTHENTIC');
    const verdictTone = result?.label === 'REAL'
        ? 'bg-green-50 border-green-500 text-green-900'
        : result?.label === 'FAKE' || result?.is_deepfake
            ? 'bg-red-50 border-red-500 text-red-900'
            : 'bg-yellow-50 border-yellow-500 text-yellow-900';

    return (
        <div className="max-w-5xl mx-auto p-8 bg-white rounded-2xl shadow-xl border border-slate-100">
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

            <div className="mb-8">
                {mode === 'text' ? (
                    <textarea
                        className="w-full p-6 bg-slate-50 border border-slate-200 rounded-xl text-slate-800 placeholder:text-slate-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all min-h-[220px] text-lg resize-y"
                        placeholder="Paste a claim, article text, or news URL here..."
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                    />
                ) : (
                    <div className="group relative border-2 border-dashed border-slate-300 rounded-xl p-12 text-center hover:bg-slate-50 hover:border-indigo-400 transition-all cursor-pointer">
                        <input
                            type="file"
                            accept={mode === 'image' ? 'image/*' : 'video/*'}
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
                        <span>{polling ? 'Processing video...' : 'Generating verification report...'}</span>
                    </span>
                ) : 'Run GenAI Analysis'}
            </button>

            {error && (
                <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-r-lg">
                    <strong className="font-bold block mb-1">Analysis Failed</strong>
                    {error}
                </div>
            )}

            {result && (
                <div className="mt-12 animate-fade-in space-y-8">
                    <div className={`p-6 rounded-2xl border-l-8 shadow-sm ${verdictTone}`}>
                        <div className="flex items-center justify-between mb-2 gap-4">
                            <h2 className="text-3xl font-extrabold uppercase tracking-wide">{verdict}</h2>
                            <span className="text-4xl">
                                {result?.label === 'REAL' ? '✅' : result?.label === 'FAKE' || result?.is_deepfake ? '🚨' : '⚠️'}
                            </span>
                        </div>
                        <p className="text-lg opacity-90 leading-relaxed font-medium">
                            {result.summary || result.final_reasoning || result.verdict_explanation || result.short_explanation}
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-slate-50 p-6 rounded-xl border border-slate-100">
                            <h3 className="text-slate-500 text-xs font-bold uppercase tracking-wider mb-4">Metrics</h3>
                            {renderConfidenceBar(result.confidence || result.confidence_score, 'Confidence Score')}
                            {result.credibility_analysis && renderConfidenceBar(result.credibility_analysis.credibility_score, 'Source Credibility')}
                        </div>

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
                                    {result.credibility_analysis?.source_reputation || 'No source reputation data available.'}
                                </p>
                            )}
                        </div>
                    </div>

                    {mode !== 'video' && (
                        <>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <SectionCard title="Detected Claims" icon="🧠">
                                    <BulletList items={result.detected_claims} emptyText="No clear claims were extracted." />
                                </SectionCard>
                                <SectionCard title="Verification Strategy" icon="🗺️">
                                    <BulletList items={result.verification_strategy} emptyText="No explicit verification strategy returned." />
                                </SectionCard>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <SectionCard title="Evidence Supporting the Claim" icon="✅">
                                    <BulletList items={result.evidence_for} emptyText="No strong supporting evidence found." />
                                </SectionCard>
                                <SectionCard title="Evidence Against the Claim" icon="🚫">
                                    <BulletList items={result.evidence_against} emptyText="No strong contradicting evidence found." />
                                </SectionCard>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <SectionCard title="Key Facts" icon="💡">
                                    <BulletList items={result.key_facts} emptyText="No key facts extracted." />
                                </SectionCard>
                                <SectionCard title="Uncertainty Notes" icon="🫥">
                                    <BulletList items={result.uncertainty_notes} emptyText="No major uncertainty notes returned." />
                                </SectionCard>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <SectionCard title="Cross Verification" icon="⚖️">
                                    <div className="space-y-4 text-sm">
                                        <div>
                                            <span className="block text-slate-500 font-semibold mb-1">Common Points:</span>
                                            <p className="text-slate-700">{result.cross_verification?.common_points || 'N/A'}</p>
                                        </div>
                                        <div>
                                            <span className="block text-slate-500 font-semibold mb-1">Discrepancies:</span>
                                            <p className="text-slate-700">{result.cross_verification?.discrepancies || 'N/A'}</p>
                                        </div>
                                    </div>
                                </SectionCard>
                                <SectionCard title="Final Reasoning" icon="🧾">
                                    <p className="text-slate-700 text-sm leading-6 mb-4">{result.final_reasoning || 'No final reasoning returned.'}</p>
                                    <div className="rounded-lg bg-indigo-50 border border-indigo-100 p-4">
                                        <span className="block text-xs uppercase font-bold tracking-wider text-indigo-500 mb-1">Recommended Action</span>
                                        <p className="text-sm text-slate-700">{result.recommended_user_action || 'Verify through trusted reporting before sharing.'}</p>
                                    </div>
                                </SectionCard>
                            </div>
                        </>
                    )}

                    {(result.citations || []).length > 0 && (
                        <div className="bg-slate-50 p-6 rounded-xl border border-slate-100">
                            <h3 className="text-slate-500 text-xs font-bold uppercase tracking-wider mb-4">Sources</h3>
                            <div className="grid gap-3">
                                {result.citations.map((cite, i) => {
                                    const url = cite?.url || cite;
                                    const snippet = cite?.snippet;
                                    return (
                                        <a
                                            key={i}
                                            href={url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center p-3 bg-white hover:bg-indigo-50 border border-slate-200 rounded-lg transition-colors group"
                                        >
                                            <span className="text-xl mr-3 group-hover:scale-110 transition-transform">🔗</span>
                                            <div className="overflow-hidden">
                                                <div className="text-sm font-semibold text-indigo-600 truncate">{url}</div>
                                                {snippet && <div className="text-xs text-slate-500 truncate mt-0.5">{snippet}</div>}
                                            </div>
                                        </a>
                                    );
                                })}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Detector;

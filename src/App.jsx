import React, { useState } from 'react';
import { ShieldAlert, ShieldCheck, AlertCircle, Upload, FileText, Loader2, CheckCircle2 } from 'lucide-react';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [inputText, setInputText] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  
  const [modelFile, setModelFile] = useState(null);
  const [tokenizerFile, setTokenizerFile] = useState(null);
  const [uploadMsg, setUploadMsg] = useState('');

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!inputText && !selectedFile) {
        setError("Please provide text or pick a file.");
        return;
    }
    
    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    if (inputText) formData.append('text', inputText);
    if (selectedFile) formData.append('file', selectedFile);

    try {
      const resp = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        body: formData,
      });
      
      if (!resp.ok) {
        const errData = await resp.json();
        throw new Error(errData.detail || "Server error");
      }
      
      const data = await resp.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleModelUpload = async () => {
    if (!modelFile) return;
    const formData = new FormData();
    formData.append('file', modelFile);
    try {
        const resp = await fetch(`${API_BASE}/upload-model`, { method: 'POST', body: formData });
        const data = await resp.json();
        setUploadMsg(data.message);
    } catch (err) { setUploadMsg("Failed to upload model."); }
  };

  const handleTokenizerUpload = async () => {
    if (!tokenizerFile) return;
    const formData = new FormData();
    formData.append('file', tokenizerFile);
    try {
        const resp = await fetch(`${API_BASE}/upload-tokenizer`, { method: 'POST', body: formData });
        const data = await resp.json();
        setUploadMsg(data.message);
    } catch (err) { setUploadMsg("Failed to upload tokenizer."); }
  };

  const getRiskColor = (level) => {
    if (level === "Safe") return "Safe";
    if (level === "Suspicious") return "Suspicious";
    return "High";
  };

  const getRiskIcon = (level) => {
    if (level === "Safe") return <ShieldCheck className="w-8 h-8 icon-safe" />;
    if (level === "Suspicious") return <AlertCircle className="w-8 h-8 icon-suspicious" />;
    return <ShieldAlert className="w-8 h-8 icon-risk" />;
  };

  const highlightText = (text, phrases) => {
    if (!text) return "";
    let highlighted = text;
    phrases.forEach(phrase => {
      const regex = new RegExp(`(${phrase})`, 'gi');
      highlighted = highlighted.replace(regex, '<span class="highlight-red">$1</span>');
    });
    return highlighted;
  };

  return (
    <div className="container">
      <header>
        <h1>ScamShield AI</h1>
        <p className="subtitle">Detect job scams and fraudulent internships using advanced AI analysis.</p>
      </header>

      <div className="glass-card">
        <form onSubmit={handleAnalyze}>
          <div className="input-group">
            <label>Analyze Job Description or Offer Text</label>
            <textarea 
              placeholder="Paste job details, emails, or offer text here..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />
          </div>

          <div className="file-row">
            <div className="input-group">
              <label>Or Upload Screenhot/PDF</label>
              <div className="file-input-wrapper">
                <Upload size={20} className="mr-2" />
                <span>{selectedFile ? selectedFile.name : "Select JPG/PNG/PDF"}</span>
                <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} />
              </div>
            </div>
          </div>

          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? <><span className="loading-spinner"></span> Analyzing...</> : "Start Risk Analysis"}
          </button>
        </form>

        {error && <div className="mt-4 text-red-400 font-medium">⚠️ {error}</div>}
      </div>

      {results && (
        <div className="results-section glass-card" style={{ animation: 'fadeIn 0.5s ease-out' }}>
          <div className="risk-header">
            <div className="flex items-center gap-4">
              {getRiskIcon(results.risk_level)}
              <div>
                <h2 className="text-2xl font-bold m-0">{results.risk_level}</h2>
                <span className="text-muted">Detected Risk Level</span>
              </div>
            </div>
            <div className={`risk-badge risk-${getRiskColor(results.risk_level)}`}>
              {results.confidence_score}% Confidence
            </div>
          </div>

          <div className="confidence-bar">
            <div className="confidence-fill" style={{ width: `${results.confidence_score}%` }}></div>
          </div>

          <div className="mt-6">
            <h3 className="text-lg font-bold mb-3">AI Reasoning</h3>
            <p className="text-muted leading-relaxed">{results.reasoning}</p>
          </div>

          <div className="mt-6">
            <h3 className="text-lg font-bold mb-3">AI Proof & Evidence (Extracted Text)</h3>
            <div 
              className="proof-container"
              dangerouslySetInnerHTML={{ __html: highlightText(results.extracted_text, results.highlighted_phrases) }}
            />
          </div>

          {results.highlighted_phrases.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-bold mb-3">Detected Risk Triggers</h3>
              <div className="flex flex-wrap gap-2">
                {results.highlighted_phrases.map((phrase, i) => (
                  <span key={i} className="trigger-badge">
                    {phrase}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="mt-8">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <CheckCircle2 className="text-primary" size={20} /> Recommended Actions
            </h3>
            <div className="guidance-list">
              {results.actions.map((action, i) => (
                <div key={i} className="guidance-item">
                  <span className="text-primary font-bold">{i + 1}.</span>
                  <span>{action}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="model-upload-section">
        <h3 className="text-xl font-bold mb-2">Advanced: Update Analysis Model</h3>
        <p className="text-muted mb-4">Upload your custom trained Keras model and tokenizer from the Colab notebook.</p>
        
        <div className="flex gap-4">
          <div className="w-full">
            <div className="file-upload-tile">
              <Upload className="icon-upload" />
              <span className="font-semibold text-sm">DL Model (.h5)</span>
              <span className="file-status">{modelFile ? modelFile.name : "Click to select"}</span>
              <input type="file" onChange={(e) => setModelFile(e.target.files[0])} />
            </div>
            <button onClick={handleModelUpload} className="btn-primary mt-2 text-sm py-2">Upload Model</button>
          </div>
          
          <div className="w-full">
            <div className="file-upload-tile">
              <Upload className="icon-upload" />
              <span className="font-semibold text-sm">Tokenizer (.pickle)</span>
              <span className="file-status">{tokenizerFile ? tokenizerFile.name : "Click to select"}</span>
              <input type="file" onChange={(e) => setTokenizerFile(e.target.files[0])} />
            </div>
            <button onClick={handleTokenizerUpload} className="btn-primary mt-2 text-sm py-2">Upload Tokenizer</button>
          </div>
        </div>
        
        {uploadMsg && <p className="mt-4 text-primary font-bold">{uploadMsg}</p>}
      </div>

      <footer className="mt-20 text-center text-muted text-sm border-t border-white/5 pt-10 w-full mb-10">
        ScamShield AI © 2026 • Professional Security & Fraud Prevention
      </footer>
    </div>
  );
}

export default App;

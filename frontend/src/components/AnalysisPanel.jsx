import { useState } from "react";
import { analyzeImage, errorMessage } from "../api";

export default function AnalysisPanel({ onResult }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const pick = (f) => {
    setFile(f);
    setResult(null);
    setPreview(f ? URL.createObjectURL(f) : null);
  };

  const run = async () => {
    setLoading(true);
    setError("");
    try {
      const r = await analyzeImage(file);
      setResult(r);
      onResult(r);
    } catch (e) {
      setError(errorMessage(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Site image analysis</h2>
      <input type="file" accept="image/jpeg,image/png,image/webp" onChange={(e) => pick(e.target.files[0])} />
      {preview && <img className="preview" src={preview} alt="Site preview" />}
      <button disabled={!file || loading} onClick={run}>
        {loading ? "Analysing…" : "Analyse image"}
      </button>
      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <p><b>Stage:</b> {result.stage} &nbsp; <b>Progress:</b> {result.progress_percent}%</p>
          <div className="bar"><div style={{ width: `${result.progress_percent}%` }} /></div>
          <p>{result.summary}</p>
          <h3>Materials</h3>
          <p>{result.materials.join(", ") || "None detected"}</p>
          <h3>Defects</h3>
          {result.defects.length === 0 ? <p>None detected</p> : (
            <ul>
              {result.defects.map((d, i) => (
                <li key={i}><span className={`sev ${d.severity}`}>{d.severity}</span> <b>{d.type}</b> – {d.description}</li>
              ))}
            </ul>
          )}
          <h3>Safety issues</h3>
          {result.safety_issues.length === 0 ? <p>None detected</p> : (
            <ul>{result.safety_issues.map((s, i) => <li key={i}>{s}</li>)}</ul>
          )}
        </div>
      )}
    </section>
  );
}

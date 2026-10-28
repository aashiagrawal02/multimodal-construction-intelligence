import { useState } from "react";
import { visualize, errorMessage } from "../api";

export default function VisualizePanel() {
  const [description, setDescription] = useState("modern two-storey house with balcony and solar panels");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const run = async () => {
    setLoading(true);
    setError("");
    try {
      const r = await visualize({ description, seed: Math.floor(Math.random() * 100000) });
      setImage(r.image_url);
    } catch (e) {
      setError(errorMessage(e));
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Construction visualisation (Flux via Pollinations)</h2>
      <textarea rows={3} value={description} onChange={(e) => setDescription(e.target.value)} />
      <button disabled={!description.trim() || loading} onClick={run}>
        {loading ? "Generating…" : "Generate render"}
      </button>
      {error && <p className="error">{error}</p>}
      {image && (
        <img
          className="preview"
          src={image}
          alt="Generated render"
          onLoad={() => setLoading(false)}
          onError={() => { setLoading(false); setError("Image generation failed, try again."); }}
        />
      )}
    </section>
  );
}

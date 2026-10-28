import { useState } from "react";
import { estimateProject, errorMessage } from "../api";

const inr = (n) => new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(n);

export default function PlanningPanel({ onResult }) {
  const [form, setForm] = useState({ area_sqft: 1200, floors: 1, quality: "standard", city_tier: 2 });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const run = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const r = await estimateProject({
        ...form,
        area_sqft: Number(form.area_sqft),
        floors: Number(form.floors),
        city_tier: Number(form.city_tier),
      });
      setResult(r);
      onResult(r);
    } catch (err) {
      setError(errorMessage(err));
    }
  };

  return (
    <section className="card">
      <h2>Construction planning & valuation</h2>
      <form onSubmit={run} className="grid">
        <label>Plot/floor area (sq.ft)
          <input type="number" min="1" value={form.area_sqft} onChange={(e) => set("area_sqft", e.target.value)} />
        </label>
        <label>Floors
          <input type="number" min="1" max="50" value={form.floors} onChange={(e) => set("floors", e.target.value)} />
        </label>
        <label>Quality
          <select value={form.quality} onChange={(e) => set("quality", e.target.value)}>
            <option value="economy">Economy</option>
            <option value="standard">Standard</option>
            <option value="premium">Premium</option>
          </select>
        </label>
        <label>City tier
          <select value={form.city_tier} onChange={(e) => set("city_tier", e.target.value)}>
            <option value={1}>Tier 1 (metro)</option>
            <option value={2}>Tier 2</option>
            <option value={3}>Tier 3 / town</option>
          </select>
        </label>
        <button type="submit">Estimate</button>
      </form>
      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <p className="big">{inr(result.total_cost)}</p>
          <p>{result.built_up_area_sqft} sq.ft built-up · {inr(result.rate_per_sqft)}/sq.ft · ~{result.total_weeks} weeks</p>
          <h3>Cost breakdown</h3>
          <table>
            <tbody>
              {result.breakdown.map((l) => (
                <tr key={l.item}><td>{l.item}</td><td>{l.percent}%</td><td>{inr(l.amount)}</td></tr>
              ))}
            </tbody>
          </table>
          <h3>Timeline</h3>
          <table>
            <tbody>
              {result.timeline.map((p) => (
                <tr key={p.phase}><td>{p.phase}</td><td>{p.weeks} wk</td></tr>
              ))}
            </tbody>
          </table>
          <p className="note">Indicative estimate only. Get local contractor quotes before budgeting.</p>
        </div>
      )}
    </section>
  );
}

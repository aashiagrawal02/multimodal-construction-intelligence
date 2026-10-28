import { useState } from "react";
import { askAssistant, errorMessage } from "../api";

export default function AssistantPanel({ context }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const hasContext = Object.keys(context).length > 0;

  const send = async (e) => {
    e.preventDefault();
    const q = question.trim();
    if (!q) return;
    setQuestion("");
    setMessages((m) => [...m, { role: "user", text: q }]);
    setLoading(true);
    try {
      const r = await askAssistant(q, hasContext ? context : null);
      setMessages((m) => [...m, { role: "assistant", text: r.answer }]);
    } catch (err) {
      setMessages((m) => [...m, { role: "assistant", text: `Error: ${errorMessage(err)}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Construction assistant</h2>
      <p className="note">
        {hasContext
          ? "Using your site analysis / cost estimate as context."
          : "Tip: run a site analysis or cost estimate first for context-aware answers."}
      </p>
      <div className="chat">
        {messages.map((m, i) => <div key={i} className={`msg ${m.role}`}>{m.text}</div>)}
        {loading && <div className="msg assistant">Thinking…</div>}
      </div>
      <form onSubmit={send} className="row">
        <input value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="e.g. How long should I cure the slab?" />
        <button type="submit" disabled={loading}>Ask</button>
      </form>
    </section>
  );
}

import { useEffect, useState } from "react";
import { getHealth } from "./api";
import AnalysisPanel from "./components/AnalysisPanel.jsx";
import PlanningPanel from "./components/PlanningPanel.jsx";
import VisualizePanel from "./components/VisualizePanel.jsx";
import AssistantPanel from "./components/AssistantPanel.jsx";

const TABS = [
  { id: "analysis", label: "Site Analysis" },
  { id: "planning", label: "Planning & Cost" },
  { id: "visualize", label: "Visualize" },
  { id: "assistant", label: "Assistant" },
];

export default function App() {
  const [tab, setTab] = useState("analysis");
  const [health, setHealth] = useState(null);
  // Shared project context so the assistant can use earlier results
  const [context, setContext] = useState({});

  useEffect(() => {
    getHealth().then(setHealth).catch(() => setHealth({ status: "offline" }));
  }, []);

  const patchContext = (key, value) => setContext((c) => ({ ...c, [key]: value }));

  return (
    <div className="app">
      <header>
        <h1>Multimodal Construction Intelligence Platform</h1>
        <span className={`badge ${health?.status === "ok" ? (health.demo_mode ? "warn" : "ok") : "bad"}`}>
          {health?.status === "ok" ? (health.demo_mode ? "Demo mode" : "Live AI") : "Backend offline"}
        </span>
      </header>

      <nav>
        {TABS.map((t) => (
          <button key={t.id} className={tab === t.id ? "active" : ""} onClick={() => setTab(t.id)}>
            {t.label}
          </button>
        ))}
      </nav>

      <main>
        {tab === "analysis" && <AnalysisPanel onResult={(r) => patchContext("site_analysis", r)} />}
        {tab === "planning" && <PlanningPanel onResult={(r) => patchContext("cost_estimate", r)} />}
        {tab === "visualize" && <VisualizePanel />}
        {tab === "assistant" && <AssistantPanel context={context} />}
      </main>
    </div>
  );
}

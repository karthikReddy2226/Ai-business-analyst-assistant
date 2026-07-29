import { useStore } from "./store";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function Insights() {
  const { insights, setInsights, questionInsights } = useStore();

  const loadGeneral = async () => {
    setInsights("Loading insights...");
    try {
      const r = await axios.get(`${API_BASE}/insights`);
      setInsights(r.data.insights);
    } catch (e) {
      setInsights("Rate limit reached — wait a few seconds, then click Refresh.");
    }
  };

  if (questionInsights) {
    return (
      <div className="insights-wrap">
        <div className="insights-header">
          <h3>🧠 Insights: "{questionInsights.question}"</h3>
          <button onClick={loadGeneral}>Show general insights instead</button>
        </div>
        <div className="insights-body">
          {questionInsights.loading ? "Analyzing this question..." : questionInsights.text}
        </div>
      </div>
    );
  }

  return (
    <div className="insights-wrap">
      <div className="insights-header">
        <h3>🧠 Auto Insights</h3>
        <button onClick={loadGeneral}>{insights ? "Refresh" : "Generate general insights"}</button>
      </div>
      <div className="insights-body">{insights || "Click Generate insights, or click '🧠 Insights on this' under any chat answer."}</div>
    </div>
  );
}
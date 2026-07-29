import { useEffect, useState } from "react";
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer,
} from "recharts";
import { getSummary } from "./api";
import { useStore } from "./store";

const COLORS = ["#6366f1", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981", "#3b82f6"];

function SingleChart({ chart }) {
  const rows = chart.labels.map((label, i) => ({ name: label, value: chart.values[i] }));
  return (
    <div className="chart-card">
      <h4>{chart.title}</h4>
      <ResponsiveContainer width="100%" height={260}>
        {chart.chart_type === "line" ? (
          <LineChart data={rows}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" /><YAxis /><Tooltip />
            <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} />
          </LineChart>
        ) : chart.chart_type === "pie" ? (
          <PieChart>
            <Pie data={rows} dataKey="value" nameKey="name" outerRadius={90} label>
              {rows.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        ) : (
          <BarChart data={rows}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" /><YAxis /><Tooltip />
            <Bar dataKey="value" fill="#6366f1" radius={[6, 6, 0, 0]} />
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}

export default function Dashboard() {
  const { currentChart } = useStore();
  const [summary, setSummary] = useState(null);

  useEffect(() => { getSummary().then(setSummary); }, []);

  const charts = currentChart?.charts || [];

  return (
    <div className="dashboard-wrap">
      {summary && (
        <div className="stat-row">
          <Stat label="Total Revenue" value={`$${summary.total_revenue.toLocaleString()}`} />
          <Stat label="Avg Order Value" value={`$${summary.avg_order_value}`} />
          <Stat label="Total Orders" value={summary.total_orders} />
          <Stat label="Avg Rating" value={summary.avg_rating} />
        </div>
      )}

      {currentChart?.loading && <p>Generating charts...</p>}
      {currentChart?.error && <p>{currentChart.error}</p>}
      {!currentChart && <p>Ask a question in Chat, then click 📊 Visualize this.</p>}

      <div className="chart-grid">
        {charts.map((c, i) => <SingleChart key={i} chart={c} />)}
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="stat-card">
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
    </div>
  );
}
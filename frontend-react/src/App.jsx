import { useState } from "react";
import { StoreProvider } from "./store";
import Sidebar from "./Sidebar";
import Chat from "./Chat";
import Dashboard from "./Dashboard";
import Insights from "./Insights";
import "./App.css";

export default function App() {
  const [tab, setTab] = useState("chat");
  return (
    <StoreProvider>
      <div className="app-shell">
        <Sidebar />
        <div className="main-panel">
          <div className="tab-bar">
            <button className={tab === "chat" ? "active" : ""} onClick={() => setTab("chat")}>💬 Chat</button>
            <button className={tab === "dashboard" ? "active" : ""} onClick={() => setTab("dashboard")}>📊 Dashboard</button>
            <button className={tab === "insights" ? "active" : ""} onClick={() => setTab("insights")}>🧠 Insights</button>
          </div>
          <div style={{ display: tab === "chat" ? "block" : "none", height: "100%" }}><Chat /></div>
          <div style={{ display: tab === "dashboard" ? "block" : "none" }}><Dashboard /></div>
          <div style={{ display: tab === "insights" ? "block" : "none" }}><Insights /></div>
        </div>
      </div>
    </StoreProvider>
  );
}
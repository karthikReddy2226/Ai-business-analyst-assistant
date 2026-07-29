import { useState } from "react";
import { useStore } from "./store";

export default function Sidebar() {
  const { sessions, currentSession, newChat, selectChat } = useStore();
  const [search, setSearch] = useState("");

  const filtered = sessions.filter((s) =>
    s.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="sidebar">
      <div className="sidebar-top">
        <input
          className="sidebar-search"
          placeholder="Search chats..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button className="new-chat-btn" onClick={newChat} title="New chat">+</button>
      </div>
      <div className="sidebar-list">
        {filtered.map((s) => (
          <div
            key={s.id}
            className={`sidebar-item ${s.id === currentSession.id ? "active" : ""}`}
            onClick={() => selectChat(s.id)}
          >
            {s.title}
          </div>
        ))}
      </div>
    </div>
  );
}
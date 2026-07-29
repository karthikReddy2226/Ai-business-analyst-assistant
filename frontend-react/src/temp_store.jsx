import { createContext, useContext, useState, useEffect } from "react";

const StoreContext = createContext(null);

function loadSessions() {
  const saved = localStorage.getItem("chat-sessions");
  if (saved) return JSON.parse(saved);
  const id = crypto.randomUUID();
  return {
    sessions: [{ id, title: "New chat", messages: [
      { role: "assistant", content: "Ask me anything about your sales data." },
    ]}],
    currentId: id,
  };
}

export function StoreProvider({ children }) {
  const [{ sessions, currentId }, setState] = useState(loadSessions);
  const [currentChart, setCurrentChart] = useState(null);
  const [insights, setInsights] = useState(null);
  const [questionInsights, setQuestionInsights] = useState(null);

  useEffect(() => {
    localStorage.setItem("chat-sessions", JSON.stringify({ sessions, currentId }));
  }, [sessions, currentId]);

  const currentSession = sessions.find((s) => s.id === currentId) || sessions[0];

  const newChat = () => {
    const id = crypto.randomUUID();
    setState((s) => ({
      sessions: [
        { id, title: "New chat", messages: [
          { role: "assistant", content: "Ask me anything about your sales data." },
        ]},
        ...s.sessions,
      ],
      currentId: id,
    }));
  };

  const selectChat = (id) => setState((s) => ({ ...s, currentId: id }));

  const addMessage = (sessionId, msg) => {
    setState((s) => ({
      ...s,
      sessions: s.sessions.map((sess) => {
        if (sess.id !== sessionId) return sess;
        const messages = [...sess.messages, msg];
        const title =
          sess.title === "New chat" && msg.role === "user"
            ? msg.content.slice(0, 30)
            : sess.title;
        return { ...sess, messages, title };
      }),
    }));
  };

  return (
    <StoreContext.Provider
      value={{
        sessions, currentSession, newChat, selectChat, addMessage,
        currentChart, setCurrentChart,
        insights, setInsights,
        questionInsights, setQuestionInsights,
      }}
    >
      {children}
    </StoreContext.Provider>
  );
}

export const useStore = () => useContext(StoreContext);
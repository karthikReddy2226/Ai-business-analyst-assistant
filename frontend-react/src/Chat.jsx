import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useStore } from "./store";
import { askQuestion, getChartData, getQuestionInsights } from "./api";

export default function Chat() {
  const { currentSession, addMessage, setCurrentChart, setQuestionInsights } = useStore();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);
  const bottomRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [currentSession.messages]);

  const send = async (text) => {
    const question = text ?? input;
    if (!question.trim()) return;
    addMessage(currentSession.id, { role: "user", content: question });
    setInput("");
    setLoading(true);
    try {
      const answer = await askQuestion(question);
      addMessage(currentSession.id, { role: "assistant", content: answer, question });
    } catch (e) {
      addMessage(currentSession.id, { role: "assistant", content: "Error reaching backend." });
    }
    setLoading(false);
  };

  const visualize = async (question) => {
    setCurrentChart({ loading: true });
    try {
      setCurrentChart(await getChartData(question));
    } catch (e) {
      setCurrentChart({ error: "Could not generate chart." });
    }
  };


  const explainInsights = async (question) => {
  setQuestionInsights({ loading: true, question });
  try {
    const text = await getQuestionInsights(question);
    setQuestionInsights({ question, text });
  } catch (e) {
    setQuestionInsights({ question, text: "Could not generate insights — try again in a moment." });
  }
};
  const toggleMic = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Voice input isn't supported in this browser. Try Chrome.");
      return;
    }
    if (recording) {
      recognitionRef.current?.stop();
      setRecording(false);
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      setInput((prev) => (prev ? prev + " " + transcript : transcript));
    };
    recognition.onend = () => setRecording(false);
    recognitionRef.current = recognition;
    recognition.start();
    setRecording(true);
  };

  return (
    <div className="chat-wrap">
      <div className="chat-messages">
        {currentSession.messages.map((m, i) => (
          <div key={i} className={`msg-row ${m.role}`}>
            <div className="msg-bubble">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
              {m.role === "assistant" && m.question && (
                <div className="msg-actions">
                    <button className="visualize-btn" onClick={() => visualize(m.question)}>
                        📊 Visualize this
                    </button>
                    <button className="visualize-btn" onClick={() => explainInsights(m.question)}>
                        🧠 Insights on this
                    </button>
                </div>
               )}
            </div>
          </div>
        ))}
        {loading && <div className="msg-row assistant"><div className="msg-bubble">Thinking...</div></div>}
        <div ref={bottomRef} />
      </div>
      <div className="chat-input-bar">
        <button className={`mic-btn ${recording ? "recording" : ""}`} onClick={toggleMic} title="Voice input">🎤</button>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask about revenue, top products, ratings..."
        />
        <button className="send-btn" onClick={() => send()}>Send</button>
      </div>
    </div>
  );
}
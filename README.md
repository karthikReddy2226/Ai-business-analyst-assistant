# 🤖 AI Business Analyst Assistant

**Ask your sales data questions in plain English — get instant answers, auto-generated charts, and AI-driven insights.**

An end-to-end analytics assistant that turns a 2,000+ row retail sales dataset into a conversational BI tool. Built with a **FastAPI + LangChain agent backend** and a **React 19 dashboard frontend**, it lets a non-technical user ask things like *"Which city has the highest revenue?"* and get a real, SQL-grounded answer — plus a one-click chart and deeper insights on that exact question.

🔗 **Live Demo:** [ai-business-analyst-assistant-beryl.vercel.app](https://ai-business-analyst-assistant-beryl.vercel.app/)

---

## 📌 Overview

Retail managers rarely know SQL, but they always have questions about their sales. This project replaces manual spreadsheet digging with a **natural-language-to-SQL agent** that:

1. Converts a plain-English question into a valid SQLite query
2. Executes it against a real transactional dataset
3. Returns a plain-language answer **with the actual numbers**
4. Can auto-generate matching charts and follow-up insights for that same question

It's a compact, full-stack demonstration of applying LLM tool-calling to a real business-analytics workflow rather than a generic chatbot wrapper.

## ✨ Key Features

| Feature | Description |
|---|---|
| 💬 **Conversational Q&A** | Ask free-form questions about revenue, ratings, products, or cities — answered with real numbers pulled live from the database |
| 🧠 **Agentic SQL Tool-Calling** | An LLM agent (via LangChain) autonomously writes, runs, and self-corrects SQLite queries against the exact table schema |
| 📊 **"Visualize This"** | One click turns any chat answer into 1–3 auto-generated bar / line / pie charts (Recharts), picked by the model based on question type |
| 🔍 **"Insights on This"** | Digs deeper into the specific question just asked and surfaces 2–4 non-obvious, numeric findings — not generic overview stats |
| 🎤 **Voice Input** | Browser-native speech-to-text for hands-free querying |
| 📈 **Live Dashboard** | Real-time summary KPIs (total revenue, AOV, order count, avg. rating) computed directly from the dataset |
| 🗂️ **Multi-Session Chat** | Persisted chat history across sessions via local storage, ChatGPT-style sidebar |

## 🧱 Tech Stack

**Backend**
- FastAPI (REST API, CORS-enabled)
- LangChain + Groq (`openai/gpt-oss-120b`) for the tool-calling agent
- SQLite (query engine) + Pandas/openpyxl (data ingestion)

**Frontend**
- React 19 + Vite 8
- Recharts (data visualization)
- Axios, React Markdown
- Native Web Speech API for voice input

**Data**
- 2,065-row retail transactions dataset · 17 columns · 3 branches across 3 cities (Hyderabad, Mumbai, Delhi) · 6 product lines

## 🏗️ Architecture

```
React (Vite) UI  ──HTTP──▶  FastAPI  ──▶  LangChain Agent (Groq LLM)
     │  Chat / Dashboard          │              │
     │  Recharts visuals          │              ▼
     └────────────────────────────┘        SQL tool ──▶ SQLite (orders table)
```

The agent is given the **exact live schema** at startup and is instructed to write column-safe SQL (handling spaces/symbols), self-correct on SQL errors, and always answer with concrete figures — not vague summaries.

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/ask` | Natural-language question → agent-generated SQL → plain-language answer |
| `GET` | `/insights` | Top 3 store-wide insights, agent-generated |
| `POST` | `/question-insights` | Deep-dive insights tied to a specific prior question |
| `POST` | `/chart-data` | Agent-generated chart spec(s) (bar/line/pie) for a question |
| `GET` | `/analytics/summary` | Total revenue, AOV, order count, avg. rating |
| `GET` | `/analytics/revenue-by-product` | Revenue grouped by product line |
| `GET` | `/analytics/revenue-by-city` | Revenue grouped by city |
| `GET` | `/analytics/revenue-by-date` | Revenue trend over time |

## 🚀 Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
# add GROQ_API_KEY to a .env file
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend-react
npm install
npm run dev
```

The app auto-builds `data/ecommerce.db` from the bundled Excel dataset on first run — no manual DB setup required.

## 📁 Project Structure

```
Ai-business-analyst-assistant/
├── backend/
│   ├── main.py          # FastAPI app + REST endpoints
│   ├── agent.py          # LangChain agent (Q&A, insights, charts)
│   ├── tools/             # SQL execution + analytics helpers
│   └── data/               # Dataset + auto-generated SQLite DB
├── frontend-react/       # Production React + Vite dashboard (deployed)
└── frontend/               # Early Streamlit prototype
```

## 🗺️ Future Improvements

- [ ] Support CSV/Excel upload so users can plug in their own datasets
- [ ] Add authentication + per-user saved dashboards
- [ ] Cache repeated queries to reduce LLM calls
- [ ] Add automated tests for the SQL-generation agent

## 👤 Author

**Karthik Reddy**
[GitHub](https://github.com/karthikReddy2226) · [Live Project](https://ai-business-analyst-assistant-beryl.vercel.app/)

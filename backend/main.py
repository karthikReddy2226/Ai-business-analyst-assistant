from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask_agent, generate_insights, generate_chart_data, generate_question_insights
import os
import pandas as pd
import sqlite3

import os
import pandas as pd
import sqlite3

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "ecommerce.db")
EXCEL_PATH = os.path.join(BASE_DIR, "data", "Realmart_Sales_Dataset.xlsx")


def database_needs_build():
    if not os.path.exists(DB_PATH):
        return True
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        exists = cursor.fetchone() is not None
        conn.close()
        return not exists
    except Exception:
        return True


if database_needs_build():
    print("Building database from Excel...")
    df = pd.read_excel(EXCEL_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("orders", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Database created successfully with {len(df)} rows.")
else:
    print("Database already has 'orders' table, skipping build.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://ai-business-analyst-assistant-beryl.vercel.app",
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Business Analyst Backend Running"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    return {"answer": ask_agent(request.question)}


@app.get("/insights")
def insights():
    return {"insights": generate_insights()}


@app.post("/chart-data")
def chart_data(request: QuestionRequest):
    return generate_chart_data(request.question)


@app.post("/question-insights")
def question_insights(request: QuestionRequest):
    return {"insights": generate_question_insights(request.question)}


from tools.analytics import (
    get_revenue_by_product_line,
    get_revenue_by_city,
    get_revenue_by_date,
    get_summary_stats,
)

@app.get("/analytics/revenue-by-product")
def revenue_by_product():
    return get_revenue_by_product_line()

@app.get("/analytics/revenue-by-city")
def revenue_by_city():
    return get_revenue_by_city()

@app.get("/analytics/revenue-by-date")
def revenue_by_date():
    return get_revenue_by_date()

@app.get("/analytics/summary")
def summary():
    return get_summary_stats()
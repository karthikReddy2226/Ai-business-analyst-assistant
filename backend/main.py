from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask_agent, generate_insights, generate_chart_data, generate_question_insights
import os
import pandas as pd
import sqlite3

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "ecommerce.db")
EXCEL_PATH = os.path.join(BASE_DIR, "data", "Realmart_Sales_Dataset.xlsx")

if not os.path.exists(DB_PATH):
    print("Database not found — building it from Excel...")
    df = pd.read_excel(EXCEL_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("orders", conn, if_exists="replace", index=False)
    conn.close()
    print("Database created successfully.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask_agent, generate_insights, generate_chart_data, generate_question_insights

app = FastAPI()


import os
import subprocess

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "ecommerce.db")

if not os.path.exists(DB_PATH):
    subprocess.run(["python", "setup_db.py"], cwd=os.path.dirname(__file__))

    
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


@app.post("/question-insights")
def question_insights(request: QuestionRequest):
    return {"insights": generate_question_insights(request.question)}

@app.post("/chart-data")
def chart_data(request: QuestionRequest):
    return generate_chart_data(request.question)



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


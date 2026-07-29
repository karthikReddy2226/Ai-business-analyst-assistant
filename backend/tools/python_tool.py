import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ecommerce.db")


def analyze_data(code: str) -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM orders", conn)
        conn.close()
        result = eval(code, {"__builtins__": {}}, {"df": df, "pd": pd})
        return str(result)
    except Exception as e:
        return f"Error: {e}"
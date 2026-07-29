import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ecommerce.db")


def run_sql(query: str) -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        if not result:
            return "Query ran successfully but returned no rows."
        return str(result)
    except Exception as e:
        return f"SQL Error: {e}"


def get_schema() -> str:
    """Returns the actual column names of the 'orders' table, exactly as stored."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(orders);")
    columns = cursor.fetchall()
    conn.close()
    # columns: (cid, name, type, notnull, dflt_value, pk)
    return ", ".join(f'"{col[1]}"' for col in columns)
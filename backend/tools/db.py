import sqlite3

def run_sql(query: str):
    conn = sqlite3.connect("data/ecommerce.db")
    cursor = conn.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results
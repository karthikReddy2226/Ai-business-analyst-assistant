import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ecommerce.db")


def get_revenue_by_product_line():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT "Product line", SUM("Total") FROM orders GROUP BY "Product line" ORDER BY SUM("Total") DESC')
    rows = cursor.fetchall()
    conn.close()
    return [{"name": r[0], "value": round(r[1], 2)} for r in rows]


def get_revenue_by_city():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT "City", SUM("Total") FROM orders GROUP BY "City" ORDER BY SUM("Total") DESC')
    rows = cursor.fetchall()
    conn.close()
    return [{"name": r[0], "value": round(r[1], 2)} for r in rows]


def get_revenue_by_date():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT "Date", SUM("Total") FROM orders GROUP BY "Date" ORDER BY "Date"')
    rows = cursor.fetchall()
    conn.close()
    return [{"date": r[0], "value": round(r[1], 2)} for r in rows]


def get_summary_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT SUM("Total"), AVG("Total"), COUNT(*), AVG("Rating") FROM orders')
    row = cursor.fetchone()
    conn.close()
    return {
        "total_revenue": round(row[0], 2),
        "avg_order_value": round(row[1], 2),
        "total_orders": row[2],
        "avg_rating": round(row[3], 2),
    }
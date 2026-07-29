import sqlite3
import pandas as pd

conn = sqlite3.connect("backend/data/ecommerce.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(orders);")
columns = cursor.fetchall()

for col in columns:
    print(col)

conn.close()

import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
EXCEL_PATH = os.path.join(BASE_DIR, "data", "Realmart_Sales_Dataset.xlsx")
DB_PATH = os.path.join(BASE_DIR, "data", "ecommerce.db")

df = pd.read_excel(EXCEL_PATH)

conn = sqlite3.connect(DB_PATH)
df.to_sql("orders", conn, if_exists="replace", index=False)

conn.close()

print("✅ Database created successfully!")
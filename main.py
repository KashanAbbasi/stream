from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_NAME = "crypto.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def home():
    return {"message": "Crypto Analytics API Running 🚀"}


@app.get("/coins")
def get_all_coins():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM crypto_market
        ORDER BY extracted_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/top-gainers")
def top_gainers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM crypto_market
        ORDER BY price_change_24h DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/stats")
def stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(market_cap) FROM crypto_market")
    total_market_cap = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(current_price) FROM crypto_market")
    avg_price = cursor.fetchone()[0]

    conn.close()

    return {
        "total_market_cap": total_market_cap,
        "average_price": avg_price
    }
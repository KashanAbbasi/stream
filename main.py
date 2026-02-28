from fastapi import FastAPI, HTTPException
import sqlite3
from contextlib import closing

app = FastAPI(
    title="Crypto Analytics API",
    description="Crypto Market Insights API",
    version="1.0"
)

DB_NAME = "crypto.db"


# ---------- DATABASE ----------
def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- HOME ----------
@app.get("/")
def home():
    return {"message": "Crypto Analytics API Running 🚀"}


# ---------- ALL COINS ----------
@app.get("/coins")
def get_all_coins():
    try:
        with closing(get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM crypto_market
                ORDER BY extracted_at DESC
            """)
            rows = cursor.fetchall()

        return [dict(row) for row in rows]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- TOP GAINERS ----------
@app.get("/top-gainers")
def top_gainers():
    try:
        with closing(get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM crypto_market
                ORDER BY price_change_24h DESC
                LIMIT 5
            """)
            rows = cursor.fetchall()

        return [dict(row) for row in rows]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- MARKET STATS ----------
@app.get("/stats")
def stats():
    try:
        with closing(get_connection()) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT COALESCE(SUM(market_cap),0) FROM crypto_market"
            )
            total_market_cap = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COALESCE(AVG(current_price),0) FROM crypto_market"
            )
            avg_price = cursor.fetchone()[0]

        return {
            "total_market_cap": total_market_cap,
            "average_price": avg_price
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

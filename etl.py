import requests
import sqlite3
import datetime
import sys

DB_NAME = "crypto.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto_market (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin_id TEXT,
        symbol TEXT,
        name TEXT,
        current_price REAL,
        market_cap INTEGER,
        total_volume INTEGER,
        price_change_24h REAL,
        market_cap_rank INTEGER,
        volatility_score REAL,
        extracted_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": "false"
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print("API Error:", response.text)
        sys.exit()

    data = response.json()

    if not isinstance(data, list):
        print("Unexpected API response:", data)
        sys.exit()

    return data


def insert_data(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for coin in data:
        try:
            price_change = coin.get("price_change_percentage_24h") or 0
            volume = coin.get("total_volume") or 0

            volatility_score = abs(price_change) * volume

            cursor.execute("""
            INSERT INTO crypto_market (
                coin_id,
                symbol,
                name,
                current_price,
                market_cap,
                total_volume,
                price_change_24h,
                market_cap_rank,
                volatility_score,
                extracted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coin.get("id"),
                coin.get("symbol"),
                coin.get("name"),
                coin.get("current_price"),
                coin.get("market_cap"),
                volume,
                price_change,
                coin.get("market_cap_rank"),
                volatility_score,
                datetime.datetime.now().isoformat()
            ))

        except Exception as e:
            print("Skipped one record:", e)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Running ETL...")
    create_table()
    data = fetch_data()
    insert_data(data)
    print("ETL Completed Successfully 🚀")
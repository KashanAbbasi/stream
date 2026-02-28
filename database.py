import sqlite3

conn = sqlite3.connect("crypto_db.sqlite")
cur = conn.cursor()

# Create table with logo support
cur.execute("""
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
    logo TEXT,
    extracted_at TIMESTAMP
)
""")

conn.commit()
print("✅ Database ready with logo support!")
conn.close()
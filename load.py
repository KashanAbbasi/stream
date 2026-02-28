import sqlite3

def load_data(df):
    conn = sqlite3.connect("crypto_db.sqlite")
    cur = conn.cursor()
    
    for _, row in df.iterrows():
        # Convert timestamp if needed
        extracted_at = row['extracted_at']
        if str(type(extracted_at)).find("Timestamp") != -1:
            extracted_at = extracted_at.to_pydatetime()
        
        cur.execute("""
            INSERT OR REPLACE INTO crypto_market
            (coin_id, symbol, name, current_price, market_cap, total_volume, price_change_24h, market_cap_rank, volatility_score, logo, extracted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['id'], row['symbol'], row['name'], row['current_price'], row['market_cap'],
            row['total_volume'], row['price_change_24h'], row['market_cap_rank'],
            row['volatility_score'], row['logo'], extracted_at
        ))
    
    conn.commit()
    conn.close()
    print(f"✅ {len(df)} rows loaded into SQLite!")
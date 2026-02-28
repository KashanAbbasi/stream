import streamlit as st
import pandas as pd
import sqlite3

# Page config
st.set_page_config(page_title="Crypto Dashboard", layout="wide", page_icon="💰")

# -----------------------------
# Auto-refresh using Streamlit's timer trick (no experimental_rerun)
# -----------------------------
# This will reload the script every 60 seconds
st_autorefresh_interval = 60  # seconds
st.markdown(
    f"""<meta http-equiv="refresh" content="{st_autorefresh_interval}">""",
    unsafe_allow_html=True
)

# -----------------------------
# Fetch data from SQLite
# -----------------------------
def get_data():
    conn = sqlite3.connect("crypto_db.sqlite")
    df = pd.read_sql("SELECT * FROM crypto_market ORDER BY market_cap_rank ASC", conn)
    conn.close()
    return df

df = get_data()

if df.empty:
    st.warning("No data yet. Wait for ETL to run.")
else:
    st.title("🪙 Advanced Crypto Dashboard")
    
    # -----------------------------
    # Top KPIs
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Market Cap", f"${df['market_cap'].sum():,.0f}")
    col2.metric("Highest Gainer (24h)", df.loc[df['price_change_24h'].idxmax()]['name'])
    col3.metric("Most Volatile", df.loc[df['volatility_score'].idxmax()]['name'])
    col4.metric("Average Price", f"${df['current_price'].mean():.2f}")
    
    st.markdown("---")
    
    # -----------------------------
    # Coin cards with logo + info
    # -----------------------------
    st.subheader("All Coins Overview")
    for _, row in df.iterrows():
        cols = st.columns([1,3,2,2,2,2])
        with cols[0]:
            if 'logo' in row and row['logo']:
                st.image(row['logo'], width=50)
            else:
                st.text("No Logo")
        with cols[1]:
            st.markdown(f"**{row['name']} ({row['symbol'].upper()})**")
        with cols[2]:
            st.markdown(f"Price: ${row['current_price']:.2f}")
        with cols[3]:
            st.markdown(f"Market Cap: ${row['market_cap']:,}")
        with cols[4]:
            st.markdown(f"24h Change: {row['price_change_24h']:.2f}%")
        with cols[5]:
            st.markdown(f"Volatility: {row['volatility_score']:,}")
        st.markdown("---")
    
    # -----------------------------
    # Charts
    # -----------------------------
    st.subheader("Market Cap Comparison")
    st.bar_chart(df[['name', 'market_cap']].set_index('name'))
    
    st.subheader("24h Price Change")
    st.line_chart(df[['name', 'price_change_24h']].set_index('name'))
    
    st.subheader("Volatility Ranking")
    st.bar_chart(df[['name', 'volatility_score']].set_index('name'))
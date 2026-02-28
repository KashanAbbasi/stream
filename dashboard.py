import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Crypto Analytics", layout="wide")

# -------- AUTO REFRESH ----------
st.experimental_set_query_params(refresh=str(time.time()))

# -------- FETCH DATA ----------
try:
    coins_response = requests.get("http://127.0.0.1:8000/coins")
    stats_response = requests.get("http://127.0.0.1:8000/stats")

    coins_data = coins_response.json()
    stats_data = stats_response.json()

except Exception as e:
    st.error("Backend not running. Start FastAPI first.")
    st.stop()

if len(coins_data) == 0:
    st.warning("No data found. Run ETL first.")
    st.stop()

df = pd.DataFrame(coins_data)

# Remove duplicates (latest per coin)
df = df.sort_values("extracted_at", ascending=False)
df = df.drop_duplicates(subset=["coin_id"])

# -------- SIDEBAR ----------
st.sidebar.title("📊 Crypto Dashboard")

menu = st.sidebar.selectbox(
    "Select View",
    ["Overview", "Coin Detail", "Rankings"]
)

# -------- OVERVIEW PAGE ----------
if menu == "Overview":

    st.title("🚀 Market Overview")

    col1, col2, col3 = st.columns(3)

    total_market_cap = df["market_cap"].sum()
    avg_price = df["current_price"].mean()
    highest_gainer = df.loc[df["price_change_24h"].idxmax()]["name"]

    col1.metric("Total Market Cap", f"${total_market_cap:,.0f}")
    col2.metric("Average Price", f"${avg_price:,.2f}")
    col3.metric("Highest Gainer", highest_gainer)

    st.divider()

    st.subheader("Market Cap Comparison")
    st.bar_chart(df.set_index("name")["market_cap"])

    st.subheader("24h Price Change")
    st.line_chart(df.set_index("name")["price_change_24h"])

# -------- COIN DETAIL PAGE ----------
elif menu == "Coin Detail":

    st.title("🔍 Coin Detail View")

    coin_list = df["name"].tolist()

    selected_coin = st.selectbox("Select Coin", coin_list)

    coin_df = df[df["name"] == selected_coin]

    col1, col2, col3 = st.columns(3)

    col1.metric("Price", f"${coin_df['current_price'].values[0]:,.2f}")
    col2.metric("24h Change", f"{coin_df['price_change_24h'].values[0]:.2f}%")
    col3.metric("Market Cap Rank", int(coin_df['market_cap_rank'].values[0]))

    st.divider()

    st.subheader("Volume")
    st.bar_chart(coin_df.set_index("name")["total_volume"])

    st.subheader("Volatility Score")
    st.bar_chart(coin_df.set_index("name")["volatility_score"])

# -------- RANKINGS PAGE ----------
elif menu == "Rankings":

    st.title("🏆 Rankings")

    st.subheader("Top 5 Gainers")
    top_gainers = df.sort_values("price_change_24h", ascending=False).head(5)
    st.table(top_gainers[["name", "price_change_24h"]])

    st.subheader("Top 5 Market Cap")
    top_market = df.sort_values("market_cap", ascending=False).head(5)
    st.table(top_market[["name", "market_cap"]])

    st.subheader("Top 5 Most Volatile")
    top_vol = df.sort_values("volatility_score", ascending=False).head(5)
    st.table(top_vol[["name", "volatility_score"]])

# -------- FOOTER ----------
st.sidebar.markdown("---")
st.sidebar.info("Auto refresh every time ETL runs 🚀")
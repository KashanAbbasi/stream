import requests
import time

def extract_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,  # Show top 50 coins
        "page": 1,
        "sparkline": "false"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 429:
            print("Rate limit reached, waiting 60 seconds...")
            time.sleep(60)
            response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Add logo URLs
        for coin in data:
            coin['logo'] = coin.get('image', '')
        return data
    except Exception as e:
        print("Error in extraction:", e)
        return []
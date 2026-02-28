import pandas as pd
from datetime import datetime

def transform_data(raw):
    df = pd.DataFrame(raw)
    # Drop rows with missing essential info
    df = df.dropna(subset=["id", "symbol", "current_price"])
    
    # Create volatility score
    df["volatility_score"] = abs(df["price_change_24h"]) * df["total_volume"]
    
    # Add extraction timestamp
    df["extracted_at"] = datetime.now()
    
    return df
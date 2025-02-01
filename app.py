import pandas as pd
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
import time

# Initialize CoinGecko API
cg = CoinGeckoAPI()

# Check API connectivity
print("API Status:", cg.ping())

# Function to retrieve cryptocurrency data
def fetch_crypto_data(cryptos, currency="eur"):
    data = cg.get_price(
        ids=cryptos, vs_currencies=currency, include_market_cap=True,
        include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True
    )
    df = pd.DataFrame(data).T  # Transpose for readability
    df["last_updated_at"] = pd.to_datetime(df["last_updated_at"], unit="s")
    return df

# Fetch multiple cryptocurrencies
target_cryptos = ["bitcoin", "ethereum", "binancecoin", "polkadot"]
df = fetch_crypto_data(target_cryptos)
print(df)

# Plot price changes
plt.figure(figsize=(10, 5))
plt.bar(df.index, df["eur_24h_change"], color=["blue" if x > 0 else "red" for x in df["eur_24h_change"]])
plt.xlabel("Cryptocurrency")
plt.ylabel("24h Change (%)")
plt.title("24-Hour Price Change of Cryptocurrencies")
plt.xticks(rotation=45)
plt.show()

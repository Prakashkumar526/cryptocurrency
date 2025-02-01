from flask import Flask, jsonify
from pycoingecko import CoinGeckoAPI
import pandas as pd

# Initialize Flask and CoinGecko API
app = Flask(__name__)
cg = CoinGeckoAPI()

# Check API connectivity
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": cg.ping()}), 200

# Endpoint to list all coins including coin ID
@app.route('/coins', methods=['GET'])
def list_coins():
    coins = cg.get_coins_list()
    return jsonify(coins), 200

# Endpoint to list all coin categories
@app.route('/categories', methods=['GET'])
def list_categories():
    categories = cg.get_coins_categories()
    return jsonify(categories), 200

# Endpoint to list specific coins by ID (Market data against CAD)
@app.route('/coins/<coin_id>', methods=['GET'])
def get_coin_by_id(coin_id):
    data = cg.get_price(ids=coin_id, vs_currencies="cad", include_market_cap=True,
                        include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True)
    if coin_id in data:
        df = pd.DataFrame(data).T
        df["last_updated_at"] = pd.to_datetime(df["last_updated_at"], unit="s")
        return jsonify(df.to_dict(orient="records")), 200
    return jsonify({"error": "Coin not found"}), 404

# Endpoint to list coins by category (Market data against CAD)
@app.route('/coins/category/<category>', methods=['GET'])
def get_coins_by_category(category):
    coins = cg.get_coins_by_category(category)
    coin_ids = [coin['id'] for coin in coins]
    data = cg.get_price(ids=coin_ids, vs_currencies="cad", include_market_cap=True,
                        include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True)
    df = pd.DataFrame(data).T
    df["last_updated_at"] = pd.to_datetime(df["last_updated_at"], unit="s")
    return jsonify(df.to_dict(orient="records")), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

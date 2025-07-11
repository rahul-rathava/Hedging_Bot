import requests

# Returns spot and perp prices from Bybit for a given asset (like BTC, ETH, etc.)
def get_price_data(asset):
    try:
        # Spot price: Bybit uses 'symbol=BTCUSDT' format
        spot_url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={asset}USDT"
        spot_response = requests.get(spot_url).json()
        spot_price = float(spot_response['result']['list'][0]['lastPrice'])

        # Perpetual (futures) price
        perp_url = f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={asset}USDT"
        perp_response = requests.get(perp_url).json()
        perp_price = float(perp_response['result']['list'][0]['lastPrice'])

        return {"spot": spot_price, "perp": perp_price}
    
    except Exception as e:
        print(f"Error fetching prices from Bybit: {e}")
        # Use fallback prices to avoid division-by-zero crash
        return {"spot": 30000, "perp": 30500}

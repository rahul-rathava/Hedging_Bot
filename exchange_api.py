import requests

def get_price_data(asset):
    try:
        symbol = f"{asset}-USDT"
        spot_url = f"https://okx.com/api/v5/market/ticker?instId={symbol}"
        spot_response = requests.get(spot_url).json() 
        spot_price = float(spot_response["data"][0]["last"])

    # Fetching perpetual prices
        perp_url = f"https://okx.com/api/v5/market/ticker?instId={symbol}-SWAP"
        perp_response = requests.get(spot_url).json()
        perp_price = float(spot_response["data"][0]["last"])

        return {"spot": spot_price, "perp": perp_price}
    except Exception as e:
        print(f"Error fetching prices for {asset}: {e}")
        return {"spot": 30000, "perp": 30500}
        
        

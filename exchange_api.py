import requests

def get_price_data(asset):
    try:
        symbol = f"{asset}-USDT"
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"
        response = requests.get(url).json()
        spot_price = float(response["data"][0]["last"])
        
        futures_url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-SWAP"
        response2 = requests.get(futures_url).json()
        perp_price = float(response2["data"][0]["last"])
        
        return {"spot": spot_price, "perp": perp_price}
    except:
        return {"spot": 0.0, "perp": 0.0}

def calculate_delta(position_size, spot_price):
    return position_size * spot_price

def calculate_hedge_size(delta, perp_price):
    if perp_price == 0:
        return 0  # prevent divide-by-zero error
    return delta / perp_price

def is_risk_high(delta, spot_price, threshold):
    return delta > threshold * spot_price

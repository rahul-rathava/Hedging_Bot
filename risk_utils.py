def calculate_delta_and_hedge(position_size, price_data):
    spot_price = price_data["spot"]
    perp_price = price_data["perp"]

    delta = position_size * spot_price  # Simplified delta = position × price
    hedge_ratio = 1  # 1:1 hedging
    hedge_size = delta / perp_price

    return delta, hedge_size

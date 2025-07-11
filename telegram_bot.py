from telegram.ext import Updater, CommandHandler
from exchange_api import get_price_data
from risk_utils import calculate_delta, calculate_hedge_size, is_risk_high
from telegram import InlineKeyboardButton, InlineKeyboardMarkup



def start(update, context):
    update.message.reply_text("🤖 Welcome to the Spot Risk Hedging Bot!\nUse /monitor_risk <asset> <size> <threshold>")



def monitor_risk(update, context):
    try:
        asset = context.args[0].upper()
        position_size = float(context.args[1])
        threshold = float(context.args[2])

        price_data = get_price_data(asset)
        spot_price = price_data["spot"]
        perp_price = price_data["perp"]

        delta = calculate_delta(position_size, spot_price)
        hedge_size = calculate_hedge_size(delta, perp_price)

        if is_risk_high(delta, spot_price, threshold):
            keyboard = [[InlineKeyboardButton("Hedge Now", callback_data=f"hedge|{asset}|{hedge_size:.4f}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text(
                f"⚠️ High risk for {asset}!\nPosition: {position_size}\nSpot Price: {spot_price}\nDelta: {delta}\nSuggested Hedge Size: {hedge_size:.4f}",
                reply_markup=reply_markup
            )
        else:
            update.message.reply_text(" Risk within safe limits.")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

        

def main():
    updater = Updater("7928784541:AAH9Y93RRVgw63iUFh0dimNNJ-jvqBWUcS0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("monitor_risk", monitor_risk))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

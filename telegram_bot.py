from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("Hedging Bot Started! Use /monitor_risk <asset> <size> <threshold>")

def monitor_risk(update, context):
    try:
        asset = context.args[0]
        position_size = float(context.args[1])
        threshold = float(context.args[2])

        price = 30000  # simulate BTC price
        delta = position_size * price

        if delta > threshold * price:
            update.message.reply_text(
                f" High risk for {asset}!\nPosition: {position_size}\nDelta: {delta}\nSuggested Hedge Size: {delta / price:.2f}"
            )
        else:
            update.message.reply_text("Risk within safe limits.")
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

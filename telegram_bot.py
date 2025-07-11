from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("Hedging Bot Started! Use /monitor_risk <asset> <size> <threshold>")

def main():
    updater = Updater("7928784541:AAH9Y93RRVgw63iUFh0dimNNJ-jvqBWUcS0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
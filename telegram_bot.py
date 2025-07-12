from telegram.ext import Updater, CommandHandler
from exchange_api import get_price_data
from risk_utils import calculate_delta, calculate_hedge_size, is_risk_high
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import matplotlib.pyplot as plt
import os

user_state = {}



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

        user_id = update.effective_user.id

        if user_id not in user_state:
            user_state[user_id] = {}

        user_state[user_id]["asset"] = asset
        user_state[user_id]["delta"] = delta
        user_state[user_id]["hedge_size"] = hedge_size

        if "auto" not in user_state[user_id]:
            user_state[user_id]["auto"] = False  # default to OFF

        if "history" not in user_state[user_id]:
            user_state[user_id]["history"] = []

        if is_risk_high(delta, spot_price, threshold):
            if user_state[user_id]["auto"]:
                # Auto-hedge now
                user_state[user_id]["history"].append({
                    "asset": asset,
                    "hedge_size": hedge_size
                })
                update.message.reply_text(
                    f"⚠️ Risk detected and auto-hedge triggered!\n✅ Hedged {hedge_size:.4f} {asset}."
                )
            else:
                # Show button if auto mode is off
                keyboard = [[InlineKeyboardButton("🛡️ Hedge Now", callback_data=f"hedge|{asset}|{hedge_size:.4f}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                update.message.reply_text(
                    f"⚠️ High risk for {asset}!\nPosition: {position_size}\nSpot Price: {spot_price}\nDelta: {delta}\nSuggested Hedge Size: {hedge_size:.4f}",
                    reply_markup=reply_markup
                )
        else:
            update.message.reply_text("Risk within safe limits.")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")


def hedge_status(update, context):
    user_id = update.effective_user.id
    data = user_state.get(user_id)

    if not data:
        update.message.reply_text(" No hedge info found. Please run /monitor_risk first.")
        return

    update.message.reply_text(
        f"📊 Current Hedge Status:\nAsset: {data['asset']}\nDelta: {data['delta']:.2f}\nSuggested Hedge Size: {data['hedge_size']:.4f}"
    )

def hedge_now(update, context):
    user_id = update.effective_user.id
    data = user_state.get(user_id)

    if not data:
        update.message.reply_text("❌ No hedge info found. Please run /monitor_risk first.")
        return

    update.message.reply_text(
        f"✅ Simulated hedge placed for {data['hedge_size']:.4f} {data['asset']} using perpetual futures."
    )

    user_state[user_id]["history"].append({
    "asset": data["asset"],
    "hedge_size": data["hedge_size"]
    })

def hedge_history(update, context):
    user_id = update.effective_user.id
    data = user_state.get(user_id)

    if not data or "history" not in data or not data["history"]:
        update.effective_message.reply_text("📭 No hedge history found.")

        return

    msg = "📜 Hedge History:\n"
    for i, h in enumerate(data["history"], start=1):
        msg += f"{i}. {h['asset']} - {h['hedge_size']:.4f}\n"

    update.effective_message.reply_text(msg)

def hedge_chart(update, context):
    user_id=update.effective_user.id
    data = user_state.get(user_id)

    if not data or "history" not in data or not data["history"]:
        update.effective_message.reply_text("📭 No hedge history to chart.")
        return

    # Extract data
    hedges = data["history"]
    labels = [f"H{i+1}" for i in range(len(hedges))]
    sizes = [h["hedge_size"] for h in hedges]

    # Plot
    plt.figure(figsize=(6,4))
    plt.bar(labels, sizes, color='skyblue')
    plt.xlabel("Hedge Events")
    plt.ylabel("Hedge Size")
    plt.title("📊 Your Hedge History")
    plt.tight_layout()

    # Save to file
    filename = f"hedge_chart_{user_id}.png"
    plt.savefig(filename)
    plt.close()

    # Send chart
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(filename, 'rb'))

    # Delete file after sending
    os.remove(filename)

def auto_hedge(update, context):
    user_id = update.effective_user.id
    arg = context.args[0].lower() if context.args else "off"

    if user_id not in user_state:
        user_state[user_id] = {}

    if arg == "on":
        user_state[user_id]["auto"] = True
        update.message.reply_text(" Auto-Hedging Enabled.")
    else:
        user_state[user_id]["auto"] = False
        update.message.reply_text(" Auto-Hedging Disabled.")



def main():
    updater = Updater("7928784541:AAH9Y93RRVgw63iUFh0dimNNJ-jvqBWUcS0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("monitor_risk", monitor_risk))
    dp.add_handler(CommandHandler("hedge_status", hedge_status))
    dp.add_handler(CommandHandler("hedge_now", hedge_now))
    dp.add_handler(CommandHandler("hedge_history", hedge_history))
    dp.add_handler(CommandHandler("hedge_chart", hedge_chart))
    dp.add_handler(CommandHandler("auto_hedge", auto_hedge))




    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

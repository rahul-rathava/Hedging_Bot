from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN
from risk_utils import calculate_delta_and_hedge
from exchange_api import get_price_data

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Spot Risk Hedging Bot!")

async def monitor_risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        asset = context.args[0].upper()
        position_size = float(context.args[1])
        threshold = float(context.args[2])
        user_id = update.effective_user.id

        price_data = get_price_data(asset)
        delta, hedge = calculate_delta_and_hedge(position_size, price_data)

        user_state[user_id] = {
            "asset": asset,
            "position": position_size,
            "threshold": threshold,
            "delta": delta,
            "hedge": hedge
        }

        if abs(delta) > threshold:
            keyboard = [
                [InlineKeyboardButton("Hedge Now", callback_data="hedge_now")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"⚠️ Risk Alert!\nAsset: {asset}\nPosition: {position_size}\nDelta: {delta:.4f}\nSuggested Hedge: {hedge:.4f}",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text("✅ Your position is within safe delta range.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = user_state.get(user_id, {})
    await query.edit_message_text(
        f"✅ Hedge executed (simulated)\nAsset: {data.get('asset')}\nHedge Size: {data.get('hedge'):.4f}"
    )

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("monitor_risk", monitor_risk))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    app.run_polling()

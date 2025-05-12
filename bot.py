from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7965345260:AAH5_6ei_kMdSuzezn-cC0PoooQNjES31wU"
STRIPE_LINK = "https://buy.stripe.com/28o01sgDr44Y8pibII"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Pagar suscripción / Pay subscription", url=STRIPE_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hi there! to have access to the channel, first you need to pay the monthly subscription:",
        reply_markup=reply_markup
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()

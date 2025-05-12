from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7965345260:AAH5_6ei_kMdSuzezn-cC0PoooQNjES31wU"
STRIPE_LINK = "https://buy.stripe.com/28o01sgDr44Y8pibII"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Pagar suscripción", url=STRIPE_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "¡Hola! Para acceder al canal exclusivo, primero paga tu suscripción mensual:",
        reply_markup=reply_markup
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()

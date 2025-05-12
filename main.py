import os
from flask import Flask, request
import stripe
from telegram import Bot
from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
CHANNEL_INVITE_LINK = os.getenv("CHANNEL_INVITE_LINK")
CHANNEL_ID = os.getenv("CHANNEL_ID")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")

bot = Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

stripe.api_key = STRIPE_SECRET_KEY

# Memoria temporal
telegram_users = {}

# Paso 1: Comando /start
def start(update, context):
    chat_id = update.effective_chat.id
    telegram_users[chat_id] = False  # Aún no ha pagado

    # Creamos sesión Stripe personalizada
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
        mode="subscription",
        success_url="https://t.me/BV_members_bot",
        cancel_url="https://t.me/BV_members_bot",
        metadata={"telegram_id": str(chat_id)}
    )

    context.bot.send_message(
        chat_id=chat_id,
        text=f"💳 To access the private channel, please complete your payment:\n{session.url}"
    )

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

# Paso 2: Webhook de Stripe
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        return str(e), 400

    # Pago exitoso
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        telegram_id = int(session["metadata"]["telegram_id"])

        bot.send_message(
            chat_id=telegram_id,
            text=f"🎉 Thanks for your payment! Here is your access link:\n{CHANNEL_INVITE_LINK}"
        )

    # Pago fallido
    if event["type"] == "invoice.payment_failed":
        customer = event["data"]["object"]
        telegram_id = customer["metadata"].get("telegram_id")
        if telegram_id:
            try:
                bot.send_message(chat_id=int(telegram_id), text="⚠️ Your payment failed. You have been removed.")
                bot.kick_chat_member(chat_id=CHANNEL_ID, user_id=int(telegram_id))
            except Exception as e:
                print("Error removing user:", e)

    return "OK", 200

if __name__ == "__main__":
    updater.start_polling()
    app.run(host="0.0.0.0", port=10000)

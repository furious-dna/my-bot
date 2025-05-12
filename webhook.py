import os
import stripe
from flask import Flask, request, jsonify
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
bot = Bot(token=os.getenv("BOT_TOKEN"))
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Telegram channel ID (like -1001234567890)

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError as e:
        return jsonify({"error": "Webhook signature verification failed"}), 400

    # --- Handle successful payment
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session.get("customer_email")
        # You could collect Telegram usernames via metadata
        print(f"✅ Payment success for {email}")
        # TODO: Add the user to your Telegram channel manually or send instructions

    # --- Handle failed recurring payment
    if event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        email = invoice.get("customer_email")
        print(f"❌ Payment failed for {email}")
        # TODO: Remove the user from Telegram channel if email or Telegram ID is mapped

    return jsonify({"status": "ok"}), 200

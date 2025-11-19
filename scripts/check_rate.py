import os
import sys
import requests
from datetime import datetime

def get_exchange_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('rates', {}).get('CNY')
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        sys.exit(1)

def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set.")
        sys.exit(1)

    rate = get_exchange_rate()
    if rate:
        date_str = datetime.now().strftime("%Y-%m-%d")
        message = f"💱 **USD to CNY Exchange Rate**\n📅 Date: {date_str}\n💰 Rate: 1 USD = {rate} CNY"
        send_telegram_message(bot_token, chat_id, message)
    else:
        print("Failed to retrieve exchange rate.")
        sys.exit(1)

if __name__ == "__main__":
    main()

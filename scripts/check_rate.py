import os
import sys

import requests
from datetime import datetime

def get_exchange_rate(base_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('rates', {}).get('CNY')
    except Exception as e:
        print(f"Error fetching {base_currency} exchange rate: {e}")
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
    rapidapi_key = os.environ.get("RAPIDAPI_KEY")

    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set.")
        sys.exit(1)

    # 1. Exchange Rates
    usd_rate = get_exchange_rate("USD")
    sgd_rate = get_exchange_rate("SGD")

    # 2. Stock Prices
    stocks = ["AAPL", "TSLA", "NVDA", "MSFT", "NFLX", "BTC-USD", "GC=F"]
    stock_data = []
    if rapidapi_key:
        try:
            # Join symbols with comma for batch request
            symbols_str = ",".join(stocks)
            url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"
            querystring = {"region": "US", "symbols": symbols_str}
            headers = {
                "x-rapidapi-key": rapidapi_key,
                "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            # The API returns a 'quoteResponse' object containing a 'result' list
            results = data.get('quoteResponse', {}).get('result', [])
            
            # Create a map for easy lookup
            price_map = {item['symbol']: item.get('regularMarketPrice') for item in results}
            
            for symbol in stocks:
                price = price_map.get(symbol)
                if price is not None:
                    stock_data.append(f"{symbol}: {price}")
                else:
                    stock_data.append(f"{symbol}: N/A")
                    
        except Exception as e:
            print(f"Error fetching stock prices: {e}")
            stock_data = ["Error fetching stock data"]
    else:
        stock_data = ["RapidAPI Key not provided. Skipping stocks."]

    # 3. Construct Message
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    message = f"📅 **Daily Financial Report** - {date_str}\n\n"
    
    message += "💱 **Exchange Rates (to CNY)**\n"
    if usd_rate:
        message += f"🇺🇸 USD: {usd_rate}\n"
    if sgd_rate:
        message += f"🇸🇬 SGD: {sgd_rate}\n"
    
    message += "\n📈 **Market Snapshot**\n"
    for item in stock_data:
        message += f"• {item}\n"

    send_telegram_message(bot_token, chat_id, message)

if __name__ == "__main__":
    main()

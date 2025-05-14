# Crypto Dashboard with Telegram Alerts

A live multi-coin crypto price dashboard built with **Streamlit** and powered by **CoinGecko** and **Telegram**.

## Features
- Tracks BTC, ETH, SOL, DOGE, and ADA in real-time
- Shows 24h % price change for each coin
- Logs each price snapshot to `crypto_log.csv`
- Sends Telegram alerts if a coin moves more than ±3%

## Demo
Run locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Telegram Setup
1. Create a bot using [@BotFather](https://t.me/botfather)
2. Start the bot and get your chat ID via:
```
https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```
3. Rename `.env.example` to `.env` and fill in your values.

## .env format
```
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

---

Built by Mychael Gray | Powered by OpenAI & CoinGecko
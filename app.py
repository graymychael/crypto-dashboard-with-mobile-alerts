import streamlit as st
import requests
import csv
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ALERT_THRESHOLD_PERCENT = 3

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=payload)
        return r.status_code == 200
    except:
        return False

st.set_page_config(page_title="Crypto Alert Dashboard", layout="wide")
st.title("Crypto Dashboard with Telegram Alerts")
st.markdown("---")

coins = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "dogecoin": "DOGE",
    "cardano": "ADA"
}

ids = ",".join(coins.keys())
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"

try:
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    data = r.json()

    cols = st.columns(len(coins))
    timestamp = datetime.utcnow().isoformat()
    row = [timestamp]

    for i, (coin_id, symbol) in enumerate(coins.items()):
        price = data[coin_id]["usd"]
        change = data[coin_id]["usd_24h_change"]
        row.append(price)
        alert_message = None

        if abs(change) >= ALERT_THRESHOLD_PERCENT:
            alert_message = f"{symbol}: {change:+.2f}% in 24h | ${price:,.2f}"

        with cols[i]:
            st.metric(label=symbol, value=f"${price:,.2f}", delta=f"{change:.2f}%")
            if alert_message:
                st.warning(alert_message)

        if alert_message:
            sent = send_telegram_alert(f"[{timestamp}] {alert_message}")
            if sent:
                st.success(f"Alert sent for {symbol}")
            else:
                st.error(f"Failed to send alert for {symbol}")

    filename = "crypto_log.csv"
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp"] + list(coins.values()))
        writer.writerow(row)

except Exception as e:
    st.error("Error fetching or processing data.")
    st.text(str(e))

st.caption("Streamlit + CoinGecko + Telegram | Built by Mychael Gray")
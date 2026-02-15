from flask import Flask, request, render_template_string
import datetime
import json
import os

app = Flask(__name__)

def log_visit():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'Direct')
    path = request.path
    time = datetime.datetime.utcnow().isoformat()

    data = {
        "timestamp": time,
        "ip": ip,
        "user_agent": user_agent,
        "referer": referer,
        "path": path
    }
    print("[TRACKER]", json.dumps(data, indent=2, ensure_ascii=False))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def track_and_redirect(path):
    log_visit()

    target_url = f"https://telegra.ph/{path}" if path else "https://telegra.ph"

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>ПАСТА НА MANWAYNFT by kemerovo</title>
        <meta name="description" content="Эксклюзивная паста от kemerovo. Только для избранных.">

        <meta property="og:title" content="ПАСТА НА MANWAYNFT by kemerovo" />
        <meta property="og:description" content="Эксклюзивная паста от kemerovo. Только для избранных." />
        <meta property="og:type" content="article" />
        <meta property="og:url" content="{request.url}" />
        <meta property="og:image" content="https://i.imgur.com/5KbQq9L.png" />

        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="ПАСТА НА MANWAYNFT by kemerovo" />
        <meta name="twitter:description" content="Эксклюзивная паста от kemerovo. Только для избранных." />
        <meta name="twitter:image" content="https://i.imgur.com/5KbQq9L.png" />

        <meta http-equiv="refresh" content="1;url={target_url}">
        
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: #000;
                color: #0f0;
                font-family: monospace;
                font-size: 24px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        ПАСТА НА MANWAYNFT by kemerovo<br>
        <span style="font-size:14px; color:#0a0;">Загрузка...</span>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
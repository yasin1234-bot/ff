import os
import sys
import subprocess
import threading
import time
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, render_template_string
from flask_socketio import SocketIO

# রেন্ডার বা ক্লাউড হোস্টিংয়ের জন্য বাফারিং বন্ধ করা
os.environ['PYTHONUNBUFFERED'] = '1'

app = Flask(__name__)
# সেশন সিকিউরিটির জন্য সিক্রেট কি
app.secret_key = "bot_secret_access_key_2026_99" 
# রেন্ডারে রিয়েল-টাইম লগের জন্য async_mode threading বা eventlet ব্যবহার করা হয়
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ইউজার সেশন ডাটা স্টোর করার জন্য ডিকশনারি
user_sessions = {} 
ADMIN_CONFIG = "admin_config.txt"
folder = "data"
os.makedirs(folder, exist_ok=True)
# --- আল্ট্রা প্রিমিয়াম সাইবার লগইন ডিজাইন (ফাঁকা ফাঁকা সংস্করণ) ---
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIP TCP BOT | CORE ACCESS</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #ff6b35; --dark: #050505; }
        body { 
            background-color: var(--dark); 
            height: 100vh; display: flex; align-items: center; justify-content: center;
            font-family: 'Share Tech Mono', monospace; overflow: hidden; color: white;
        }

        /* ব্যাকগ্রাউন্ড এনিমেশন */
        .bg-animate {
            position: absolute; inset: 0;
            background: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
            z-index: -1;
        }
        .grid-overlay {
            position: absolute; inset: 0;
            background-image: linear-gradient(rgba(255, 107, 53, 0.05) 1px, transparent 1px), 
                              linear-gradient(90deg, rgba(255, 107, 53, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: -1; opacity: 0.3;
        }

        /* মেইন কার্ড */
        .glass-panel {
            background: rgba(10, 10, 10, 0.8);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 107, 53, 0.3);
            padding: 50px 40px; border-radius: 20px;
            width: 400px; box-shadow: 0 0 50px rgba(0,0,0,1);
            position: relative; overflow: hidden;
        }

        .glass-panel::before {
            content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
            background: conic-gradient(transparent, transparent, transparent, var(--neon));
            animation: rotate 6s linear infinite; z-index: -1;
        }
        @keyframes rotate { 100% { transform: rotate(360deg); } }

        .inner-content { background: var(--dark); border-radius: 15px; padding: 35px; }

        .glitch-text {
            font-family: 'Orbitron', sans-serif; font-weight: 900;
            font-size: 24px; text-align: center; letter-spacing: 4px;
            color: var(--neon); text-shadow: 0 0 10px var(--neon);
            margin-bottom: 40px; /* টাইটেলের পর গ্যাপ বাড়ানো হয়েছে */
        }

        /* ইনপুট ফিল্ডের স্টাইল ও গ্যাপ */
        .input-box {
            width: 100%; padding: 15px; background: #0f0f0f;
            border: 1px solid #333; color: var(--neon);
            border-radius: 8px; margin-bottom: 30px; /* ইনপুটগুলোর মাঝে গ্যাপ বাড়ানো হয়েছে */
            outline: none; transition: 0.3s; text-align: center;
            display: block;
        }
        .input-box:focus { border-color: var(--neon); box-shadow: 0 0 15px rgba(255,107,53,0.2); }

        .login-btn {
            width: 100%; padding: 15px; background: var(--neon);
            color: black; font-weight: bold; border-radius: 8px;
            text-transform: uppercase; letter-spacing: 2px;
            transition: 0.4s; cursor: pointer; margin-top: 10px;
        }
        .login-btn:hover { background: #fff; box-shadow: 0 0 25px var(--neon); }

        #err-msg { color: #ff4444; font-size: 12px; text-align: center; margin-bottom: 15px; display: none; }
        .footer-note { font-size: 10px; color: #555; text-align: center; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="bg-animate"></div>
    <div class="grid-overlay"></div>

    <div class="glass-panel">
        <div class="inner-content">
            <h1 class="glitch-text">VIP TCP BOT TRIAL</h1>
            <div id="err-msg">ACCESS DENIED: INVALID KEY</div>
            
            <input type="text" id="u" class="input-box" placeholder="👤 Enter Name" autocomplete="off">

<input type="password" id="p" class="input-box" placeholder="🔑 Enter Password">

<button onclick="window.location.href='https://t.me/yourchannel'" 
        style="display: block; 
                margin-top: -29px; 
                padding: 6px 0; 
                width: 50%; 
                background-color: #ff4444; 
                color: white; 
                border: none; 
                border-radius: 6px; 
                cursor: pointer; 
                font-size: 13px;">
    Get Password
</button>

<button class="login-btn" onclick="handleLogin()" 
        style="margin-top: 15px;">
    LOGIN NOW ➜
</button>

<div class="footer-note">
    [SYS] : FREE TCP BOY TRIAL WEB<br>
    [OWNER] : —͞𝚈𝙰𝚂𝙸𝙽 </> 𝙱𝙷𝙰𝙸 💖
</div>

    <script>
        async function handleLogin() {
            const u = document.getElementById('u').value;
            const p = document.getElementById('p').value;
            const res = await fetch('/api/login_auth', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: u, password: p})
            });
            const data = await res.json();
            if(data.status === 'success') {
                window.location.href = '/';
            } else {
                const err = document.getElementById('err-msg');
                err.style.display = 'block';
                setTimeout(() => { err.style.display = 'none'; }, 3000);
            }
        }
    </script>
</body>
</html>
"""

# অ্যাডমিন কনফিগারেশন লোড করা
def get_config():
    conf = {"pass": "YASIN2026", "duration": 120}
    if os.path.exists(ADMIN_CONFIG):
        with open(ADMIN_CONFIG, 'r') as f:
            for line in f:
                if '=' in line:
                    parts = line.strip().split('=')
                    if len(parts) == 2:
                        key, val = parts
                        if key == 'admin_password': conf['pass'] = val
                        if key == 'global_duration': conf['duration'] = int(val)
    return conf

# অ্যাডমিন কনফিগারেশন সেভ করা
def save_config(password, duration):
    with open(ADMIN_CONFIG, 'w') as f:
        f.write(f"admin_password={password}\nglobal_duration={duration}\n")

# লগইন চেক করার ডেকোরেটর
def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    wrap.__name__ = f.__name__
    return wrap

# বটের এক্সপায়ারি চেক করার মনিটর
def expiry_monitor():
    while True:
        now = datetime.now()
        for name, data in list(user_sessions.items()):
            if data['running'] and data['end_time'] != "unlimited":
                if now > data['end_time']:
                    if data['proc']:
                        data['proc'].terminate()
                    user_sessions[name]['running'] = False
                    socketio.emit('status_update', {'running': False, 'user': name})
        time.sleep(2)

threading.Thread(target=expiry_monitor, daemon=True).start()

def stream_logs(proc, name):
    try:
        # রিয়েল-টাইম লগের জন্য iter এবং readline ব্যবহার
        for line in iter(proc.stdout.readline, ''):
            if line:
                socketio.emit('new_log', {'data': line.strip(), 'user': name})
        proc.stdout.close()
    except Exception as e:
        print(f"Logging error for {name}: {e}")

# --- রুটস (Routes) ---

@app.route('/login')
def login():
    if 'logged_in' in session:
        return redirect(url_for('index'))
    return render_template_string(LOGIN_HTML)

@app.route('/api/login_auth', methods=['POST'])
def login_auth():
    data = request.json
    u = data.get('username')
    p = data.get('password')
    if u == "admin" and p == "YASIN BHAI":
        session['logged_in'] = True
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid credentials!"})

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/check_status', methods=['POST'])
@login_required
def check_status():
    data = request.json
    name = data.get('name')
    if name in user_sessions and user_sessions[name]['running']:
        info = user_sessions[name]
        rem_sec = -1 if info['end_time'] == "unlimited" else int((info['end_time'] - datetime.now()).total_seconds())
        return jsonify({"running": True, "rem_sec": max(0, rem_sec)})
    return jsonify({"running": False})

@app.route('/api/control', methods=['POST'])
@login_required
def bot_control():
    data = request.json
    action, name, uid, pw = data.get('action'), data.get('name'), data.get('uid'), data.get('password')
    conf = get_config()

    if action == 'start':
        if not uid or not pw:
            return jsonify({"status": "error", "message": "UID/PW required!"})

        if name in user_sessions and user_sessions[name]['running']:
            return jsonify({"status": "error", "message": "ALREADY RUNNING!"})

    try:
        # 📁 Folder create
        folder = "data"
        os.makedirs(folder, exist_ok=True)

        # 🧾 Unique file per user
        file_path = os.path.join(folder, f"{name}_bot.txt")

        # 💾 Save UID & PASS
        with open(file_path, "w") as f:
            f.write(f"uid={uid}\npassword={pw}")

        # 🚀 Run bot
        proc = subprocess.Popen(
            [sys.executable, '-u', 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # ⏱️ সময় সেট
        end_time = "unlimited" if conf['duration'] == -1 else datetime.now() + timedelta(minutes=conf['duration'])

        # 👤 User session save
        user_sessions[name] = {
            'proc': proc,
            'end_time': end_time,
            'running': True
        }

        # 📡 লগ stream
        threading.Thread(target=stream_logs, args=(proc, name), daemon=True).start()

        rem_sec = conf['duration'] * 60 if conf['duration'] != -1 else -1

        return jsonify({
            "status": "success",
            "running": True,
            "rem_sec": rem_sec
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

@app.route('/api/admin', methods=['POST'])
@login_required
def admin_api():
    data = request.json
    conf = get_config()
    if data.get('password') != conf['pass']: return jsonify({"status": "error", "message": "Wrong Passkey!"})
    action = data.get('action')
    if action == 'login':
        active_users = []
        for n, i in user_sessions.items():
            if i['running']:
                rem_m = -1 if i['end_time'] == "unlimited" else max(0, int((i['end_time'] - datetime.now()).total_seconds() / 60))
                active_users.append({"name": n, "rem_min": rem_m})
        return jsonify({"status": "success", "duration": conf['duration'], "users": active_users})
    elif action == 'save_global':
        save_config(conf['pass'], int(data.get('duration', 120)))
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

@app.route('/api/proxy_guild')
@login_required
def proxy_guild():
    t, gid, reg, uid, pw = request.args.get('type'), request.args.get('guild_id'), request.args.get('region'), request.args.get('uid'), request.args.get('password')
    base_url = "https://danger-guild-management.vercel.app"
    urls = {
        'info': f"{base_url}/guild?guild_id={gid}&region={reg}",
        'join': f"{base_url}/join?guild_id={gid}&uid={uid}&password={pw}",
        'members': f"{base_url}/members?guild_id={gid}&uid={uid}&password={pw}",
        'leave': f"{base_url}/leave?guild_id={gid}&uid={uid}&password={pw}",
        'search': f"{base_url}/search?name={name}&region={reg}"
    }
    try:
        resp = requests.get(urls.get(t), timeout=15)
        return jsonify(resp.json())
    except: return jsonify({"error": "API Error"})

if __name__ == '__main__':
    # Render-এ পোর্ট এনভায়রনমেন্ট ভেরিয়েবল থেকে নিতে হয়
    port = int(os.environ.get("PORT", 10000))
    # Render-এ রিয়েল-টাইম লগের জন্য host '0.0.0.0' হওয়া বাধ্যতামূলক
    socketio.run(app, host='0.0.0.0', port=port)

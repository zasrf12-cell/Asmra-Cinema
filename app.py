import sqlite3
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_bots'

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ترسانة البوتات</title>
</head>
<body style="margin: 0; background: #141414;">
    {{ content | safe }}
</body>
</html>
"""

def init_db():
    conn = sqlite3.connect('/home/Asmra/mysite/bots.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            token TEXT NOT NULL,
            status TEXT DEFAULT 'شغال'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    
    if request.method == 'POST' and 'pin' in request.form:
        if request.form.get('pin') == '8080808':
            session['logged_in'] = True
        else:
            error = '❌ الرمز السري خطأ!'

    if session.get('logged_in'):
        if request.method == 'POST' and 'bot_name' in request.form:
            b_name = request.form.get('bot_name')
            b_token = request.form.get('bot_token')
            if b_name and b_token:
                conn = sqlite3.connect('/home/Asmra/mysite/bots.db')
                c = conn.cursor()
                c.execute('INSERT INTO bots (name, token) VALUES (?, ?)', (b_name, b_token))
                conn.commit()
                conn.close()

        conn = sqlite3.connect('/home/Asmra/mysite/bots.db')
        c = conn.cursor()
        c.execute('SELECT id, name, token, status FROM bots')
        bots_list = c.fetchall()
        conn.close()

        bots_html = ""
        for b in bots_list:
            bots_html += f"""
            <li style="background: #2a2a2a; padding: 12px; margin-bottom: 10px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #444;">
                <div>
                    <strong style="color: #00fcc; font-size: 16px;">🤖 {b[1]}</strong><br>
                    <small style="color: #aaa;">المعرّف: {b[2]}</small>
                </div>
                <span style="background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{b[3]}</span>
            </li>
            """

        if not bots_html:
            bots_html = "<p style='color: #aaa; text-align: center;'>لا توجد بوتات مضافة حتى الآن. أضف أول بوت للترسانة!</p>"

        content = f"""
        <div style="background: #141414; min-height: 100vh; color: white; padding: 20px; font-family: Tahoma, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h1 style="color: #00fcc; margin: 0; font-size: 22px;">⚡ لوحة تحكم ترسانة البوتات</h1>
                    <a href="/admin" style="background: #00fcc; color: #141414; padding: 8px 15px; border-radius: 5px; text-decoration: none; font-weight: bold; font-size: 14px;">🏠 الرئيسية</a>
                </div>
                
                <div style="background: #1f1f1f; padding: 20px; border-radius: 10px; margin-bottom: 25px; border: 1px solid #333;">
                    <h3 style="margin-top: 0; color: #fff; margin-bottom: 15px;">➕ إضافة بوت جديد ({len(bots_list)} / 13)</h3>
                    <form method="POST">
                        <input type="text" name="bot_name" placeholder="اسم البوت (مثلاً: Bot 1)" required style="width: 100%; padding: 10px; margin-bottom: 10px; background: #2a2a2a; border: 1px solid #444; color: white; border-radius: 5px; box-sizing: border-box;">
                        <input type="text" name="bot_token" placeholder="Token أو معلومات البوت" required style="width: 100%; padding: 10px; margin-bottom: 15px; background: #2a2a2a; border: 1px solid #444; color: white; border-radius: 5px; box-sizing: border-box;">
                        <button type="submit" style="width: 100%; padding: 10px; background: #10b981; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">حفظ وإضافة للترسانة 🚀</button>
                    </form>
                </div>

                <div style="background: #1f1f1f; padding: 20px; border-radius: 10px; border: 1px solid #333;">
                    <h3 style="margin-top: 0; color: #fff; margin-bottom: 15px;">📋 قائمة البوتات الحالية</h3>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        {bots_html}
                    </ul>
                </div>
            </div>
        </div>
        """
    else:
        content = f"""
        <div style="background: #141414; min-height: 100vh; color: white; display: flex; justify-content: center; align-items: center; font-family: Tahoma, sans-serif;">
            <div class="panel" style="max-width: 400px; width: 90%; background: #1f1f1f; padding: 30px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); text-align: center; border: 1px solid #333;">
                <h2 style="color: #00fcc; font-size: 22px; margin-bottom: 20px;">🔑 شباك التذاكر والإدارة</h2>
                {f'<p style="color: #e50914; font-size: 14px; font-weight: bold; margin-bottom: 15px;">{error}</p>' if error else ''}
                <form method="POST">
                    <p style="color: #aaa; font-size: 14px; margin-bottom: 15px;">منطقة سرية - مخصصة للمسؤول فقط</p>
                    <input type="password" name="pin" placeholder="الرمز السري" required style="width: 100%; padding: 12px; margin-bottom: 20px; background: #2a2a2a; border: 1px solid #444; color: white; border-radius: 6px; font-size: 16px; box-sizing: border-box; text-align: center;">
                    <button type="submit" style="width: 100%; padding: 12px; background: #e50914; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer;">دخول 🔒</button>
                </form>
            </div>
        </div>
        """
    return render_template_string(BASE_LAYOUT, content=content)


@app.route('/manage_bots', methods=['GET', 'POST'])
def manage_bots():
    if not session.get('logged_in'):
        return '<h3 style="color:red; text-align:center; padding:50px;">❌ ممنوع الدخول - منطقة سرية!</h3>'

    conn = sqlite3.connect('bots.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bots (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, token TEXT, status TEXT DEFAULT 'شغال')''')
    c.execute('''CREATE TABLE IF NOT EXISTS bot_achievements (id INTEGER PRIMARY KEY AUTOINCREMENT, bot_name TEXT, achievement TEXT, time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()

    if request.method == 'POST':
        b_name = request.form.get('bot_name')
        b_token = request.form.get('bot_token')
        if b_name and b_token:
            c.execute('INSERT INTO bots (name, token) VALUES (?, ?)', (b_name, b_token))
            conn.commit()

    c.execute('SELECT id, name, token, status FROM bots')
    bots_list = c.fetchall()

    c.execute('SELECT bot_name, achievement, time_stamp FROM bot_achievements ORDER BY id DESC LIMIT 10')
    achievements_list = c.fetchall()
    conn.close()

    bots_html = ""
    for b in bots_list:
        bots_html += f"<li><b>{b[1]}</b> - {b[2]} <span style='color:green;'>({b[3]})</span></li>"
    if not bots_html:
        bots_html = "<p style='color: gray;'>لا توجد بوتات مضافة.</p>"

    ach_html = ""
    for ac in achievements_list:
        ach_html += f"<li><b>{ac[0]}</b>: {ac[1]} <small>({ac[2]})</small></li>"
    if not ach_html:
        ach_html = "<p style='color: gray;'>لا توجد إنجازات.</p>"

    content = f"""
    <div style="background: #141414; min-height: 100vh; color: white; padding: 20px; font-family: Tahoma;">
        <div style="max-width: 600px; margin: 0 auto;">
            <h1>⚡ ترسانة البوتات والأتمتة</h1>
            <a href="/admin" style="color: #00fcc;">🔙 رجوع لشباك التذاكر</a>
            <div style="background: #1f1f1f; padding: 20px; margin-top: 20px; border-radius: 8px;">
                <h3>➕ إضافة بوت جديد</h3>
                <form method="POST">
                    <input type="text" name="bot_name" placeholder="اسم البوت" required style="width:100%; padding:8px; margin-bottom:10px; background:#2a2a2a; color:white; border:1px solid #444;"><br>
                    <input type="text" name="bot_token" placeholder="Token البوت" required style="width:100%; padding:8px; margin-bottom:10px; background:#2a2a2a; color:white; border:1px solid #444;"><br>
                    <button type="submit" style="background: #10b981; color:white; padding:10px; width:100%; border:none; border-radius:5px; font-weight:bold;">حفظ وتشغيل أوتوماتيكي 🚀</button>
                </form>
            </div>
            <div style="background: #1f1f1f; padding: 20px; margin-top: 20px; border-radius: 8px;">
                <h3>📋 البوتات الحالية</h3>
                <ul>{bots_html}</ul>
            </div>
            <div style="background: #1f1f1f; padding: 20px; margin-top: 20px; border-radius: 8px;">
                <h3>🏆 سجل الإنجازات</h3>
                <ul>{ach_html}</ul>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_LAYOUT if 'BASE_LAYOUT' in globals() else "<body>{{content|safe}}</body>", content=content)

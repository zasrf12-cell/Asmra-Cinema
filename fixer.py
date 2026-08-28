import re

file_path = 'app.py'

try:
    print("🔍 جاري قراءة الملف...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # حذف أي دالة manage_bots قديمة ومكررة بالكامل
    pattern = r'@app\.route\(\s*[\'"]\/manage_bots[\'"].*?(?=\n@app\.route|\Z)'
    new_content, count = re.subn(pattern, '', content, flags=re.DOTALL)
    print(f"🧹 تم تنظيف وحذف النسخ القديمة بنجاح.")

    # الكود النظيف الجديد
    clean_function = """

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

    content = f\"\"\"
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
    \"\"\"
    return render_template_string(BASE_LAYOUT if 'BASE_LAYOUT' in globals() else "<body>{{content|safe}}</body>", content=content)
"""

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content.strip() + "\n" + clean_function)

    print("✨ تم تعديل وترتيب الملف أوتوماتيكياً بواسطة البوت بنجاح تام! 🚀")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")

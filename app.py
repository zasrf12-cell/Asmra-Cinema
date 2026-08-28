import os
import sqlite3
from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = 'cinema_asmra_master_key'

# تحديد مسار قاعدة البيانات بدقة تامة في نفس المجلد
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURRENT_DIR, 'movies.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # إنشاء جدول الأفلام بالأعمدة الكاملة والصحيحة
    c.execute('''CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        rating TEXT,
        poster TEXT,
        description TEXT,
        video_url TEXT,
        release_year TEXT,
        views INTEGER
    )''')
    # إنشاء جدول طلبات الأفلام
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_name TEXT,
        status TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سينما أسمرة الملكية</title>
    <style>
        body { background-color: #080808; color: #fff; font-family: sans-serif; margin: 0; padding: 0; }
        header { background: #121212; padding: 15px; border-bottom: 2px solid #e50914; }
        h1 { color: #e50914; text-align: center; margin: 0 0 10px 0; font-size: 22px; }
        .nav-links { text-align: center; }
        .nav-links a { color: #fff; text-decoration: none; margin: 0 4px; padding: 7px 12px; background: #222; border-radius: 4px; font-size: 12px; display: inline-block; font-weight: bold; }
        .nav-links a:hover { background: #00ffcc; color: #000; }
        .container { max-width: 850px; margin: auto; padding: 15px; }
        .movie-box { background: #171717; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #333; }
        .movie-poster { width: 100%; max-height: 300px; object-fit: cover; border-radius: 6px; }
        .movie-title { font-size: 18px; font-weight: bold; color: #00ffcc; margin-top: 10px; }
        video { width: 100%; border-radius: 6px; border: 1px solid #00ffcc50; margin-top: 10px; }
        .panel { background: #121212; padding: 15px; border-radius: 8px; border: 1px solid #333; }
        input, textarea { width: 100%; padding: 10px; margin: 6px 0; background: #222; border: 1px solid #444; color: #fff; border-radius: 4px; box-sizing: border-box; }
        button { background: #e50914; color: #fff; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; font-size: 14px; }
        button:hover { background: #b20710; }
    </style>
</head>
<body>
    <header>
        <h1>🎬 سينما أسمرة الملكية</h1>
        <div class="nav-links">
            <a href="/">الرئيسية 🏠</a>
            <a href="/requests">طلبات الأفلام 📋</a>
            <a href="/admin">شباك التذاكر 🎟️</a>
        </div>
    </header>
    <div class="container">
        {{ content|safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, genre, rating, poster, description, video_url, release_year, views FROM movies ORDER BY id DESC")
    movies = c.fetchall()
    conn.close()

    content = ""
    if not movies:
        content = "<p style='text-align: center; color: #888; padding: 30px;'>لا توجد أفلام حالياً، ارفعها من شباك التذاكر!</p>"
    for m in movies:
        content += f"""
        <div class="movie-box">
            <img src="{m[4]}" class="movie-poster">
            <div class="movie-title">{m[1]}</div>
            <p style="color: #fffe2a; font-size: 12px; margin: 6px 0;">⭐ التقييم: {m[3]} | 📅 السنة: {m[7]} | 🏷️ التصنيف: {m[2]}</p>
            <video controls preload="auto">
                <source src="{m[6]}" type="video/mp4">
            </video>
            <p style="color: #aaa; font-size: 13px; margin-top: 8px;">{m[5]}</p>
        </div>
        """
    return render_template_string(BASE_LAYOUT, content=content)

@app.route('/requests', methods=['GET', 'POST'])
def requests_page():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        if movie_name:
            c.execute("INSERT INTO requests (movie_name, status) VALUES (?, ?)", (movie_name, 'قيد المراجعة ⏳'))
            conn.commit()
    c.execute("SELECT movie_name, status FROM requests ORDER BY id DESC")
    reqs = c.fetchall()
    conn.close()

    content = """
    <div class="panel">
        <h2 style="font-size: 18px; color: #00ffcc; margin-top:0;">📋 طلبات الأفلام السحابية</h2>
        <form method="POST">
            <input type="text" name="movie_name" placeholder="اكتب اسم الفيلم المطلوب..." required>
            <button type="submit">إرسال الطلب 📥</button>
        </form>
        <h3 style="margin-top: 15px; font-size: 15px; border-bottom: 1px solid #333; padding-bottom: 5px;">📜 الطلبات السابقة</h3>
        <ul>
    """
    if not reqs:
        content += "<p style='color: #777; font-size: 13px;'>لا توجد طلبات حتى الآن.</p>"
    for r in reqs:
        content += f"<li style='font-size: 13px; margin: 6px 0;'><b>{r[0]}</b> - <span style='color: #fffe2a;'>{r[1]}</span></li>"
    content += "</ul></div>"
    return render_template_string(BASE_LAYOUT, content=content)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST' and 'pin' in request.form:
        if request.form.get('pin') == '1233':
            session['logged_in'] = True
        else:
            error = '❌ الرمز السري خطأ!'

    if not session.get('logged_in'):
        content = f"""
        <div class="panel" style="max-width: 400px; margin: 30px auto; text-align: center;">
            <h2 style="font-size: 18px; color: #00ffcc;">🔑 شباك التذاكر والإدارة</h2>
            {f'<p style="color: #e50914; font-size: 12px; font-weight: bold;">{error}</p>' if error else ''}
            <form method="POST">
                <p style="font-size: 12px; color: #aaa;">الرمز الافتراضي = 1233</p>
                <input type="password" name="pin" placeholder="الرمز السري" required>
                <button type="submit">دخول 🔓</button>
            </form>
        </div>
        """
        return render_template_string(BASE_LAYOUT, content=content)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, rating FROM movies ORDER BY id DESC")
    movies = c.fetchall()
    conn.close()

    content = """
    <div class="panel">
        <h2 style="font-size: 18px; color: #00ffcc; margin-top:0;">➕ إضافة فيلم جديد</h2>
        <form action="/add_movie" method="POST">
            <input type="text" name="title" placeholder="اسم الفيلم" required>
            <input type="text" name="genre" placeholder="التصنيف" required>
            <input type="text" name="rating" placeholder="التقييم (مثال: 4.8/5)" required>
            <input type="text" name="poster" placeholder="رابط البوستر (صورة)" required>
            <textarea name="description" placeholder="قصة الفيلم..." rows="2" required></textarea>
            <input type="text" name="video_url" placeholder="رابط فيديو MP4 مباشر" required>
            <input type="text" name="release_year" placeholder="سنة الإنتاج" required>
            <button type="submit">نشر الفيلم 🚀</button>
        </form>
        
        <h3 style="margin-top: 25px; font-size: 15px; border-bottom: 1px solid #333; padding-bottom: 5px;">🗑️ إدارة وحذف الأفلام</h3>
        <ul style="list-style: none; padding: 0;">
    """
    if not movies:
        content += "<p style='color: #777; font-size: 13px;'>لا توجد أفلام مضافة.</p>"
    for m in movies:
        content += f"""
        <li style="background: #1a1a1a; margin: 6px 0; padding: 10px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #333;">
            <span style="font-size: 13px; font-weight: bold;">{m[1]}</span>
            <a href="/delete_movie/{m[0]}" style="background: #e50914; color: #fff; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px; font-weight: bold;">حذف 🗑️</a>
        </li>
        """
    content += "</ul></div>"
    return render_template_string(BASE_LAYOUT, content=content)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    if session.get('logged_in'):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO movies (title, genre, rating, poster, description, video_url, release_year, views) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (request.form.get('title'), request.form.get('genre'), request.form.get('rating'), request.form.get('poster'), request.form.get('description'), request.form.get('video_url'), request.form.get('release_year'), 0))
        conn.commit()
        conn.close()
    return redirect(url_for('admin'))

@app.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    if session.get('logged_in'):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

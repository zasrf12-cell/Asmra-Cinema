import os

def update_code():
    target_file = 'flask_app.py'
    print("🤖 بوت الصيانة الذكي يبدأ فحص وتنظيف ملفات السينما...")
    
    # الكود الكامل والنظيف لسينما أسمرة
    clean_code = '''from flask import Flask, render_template_string, request, redirect, url_for, session
import sqlite3
import random
import datetime
import threading
import time

app = Flask(__name__)
app.secret_key = 'cinema_asmra_master_key_2026'

def init_db():
    conn = sqlite3.connect('cinema.db')
    cursor = conn.cursor()
    cursor.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            genre TEXT,
            rating TEXT,
            poster TEXT,
            description TEXT,
            video_url TEXT,
            release_year TEXT,
            views INTEGER DEFAULT 0,
            telegram_cloud_status TEXT DEFAULT 'متصل بسحابة تلجرام'
        )
    \'\'\')
    cursor.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS box_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_desc TEXT,
            timestamp TEXT
        )
    \'\'\')
    cursor.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS room_chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            timestamp TEXT
        )
    \'\'\')
    cursor.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_name TEXT,
            status TEXT DEFAULT 'قيد المراجعة السحابية'
        )
    \'\'\')
    conn.commit()
    conn.close()

def bot_auto_publisher():
    while True:
        time.sleep(120)
        pool = [
            ('رحلة إلى المريخ', 'مغامرات', '4.3/5', 'https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800', 'أول مهمة استكشاف بشرية تكتشف أسرار الكوكب الأحمر.', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4', '2026'),
            ('سقوط العوالم الكبرى', 'خيال علمي', '4.9/5', 'https://images.unsplash.com/photo-1534447677768-be436bb09401?w=800', 'حرب عالمية فاصلة بين البشر وكائنات الفضاء الحديثة.', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', '2026'),
            ('أسرار المافيا والظلام', 'جريمة وأكشن', '4.8/5', 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800', 'رحلة انتقام خطيرة داخل أزقة المدينة المظلمة.', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4', '2025'),
        ]
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        for movie in pool:
            cursor.execute("SELECT COUNT(*) FROM movies WHERE title = ?", (movie[0],))
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO movies (title, genre, rating, poster, description, video_url, release_year, telegram_cloud_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                               (movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], 'تم النسخ والربط السحابي بـ Telegram ☁️'))
                conn.commit()
                break
        conn.close()

threading.Thread(target=bot_auto_publisher, daemon=True).start()

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سينما أسمرة الملكية</title>
    <style>
        body { background-color: #080808; color: #f2f2f2; font-family: Tahoma, sans-serif; margin: 0; padding: 0; }
        header { background: linear-gradient(to bottom, #151515, #080808); padding: 18px; text-align: center; border-bottom: 3px solid #e50914; box-shadow: 0 4px 15px rgba(0,0,0,0.9); }
        h1 { color: #e50914; margin: 0; font-size: 22px; text-shadow: 2px 2px 6px rgba(0,0,0,0.9); }
        .nav-links { margin-top: 10px; display: flex; justify-content: center; flex-wrap: wrap; gap: 6px; }
        .nav-links a { color: #fff; text-decoration: none; background: #1a1a1a; padding: 6px 10px; border-radius: 4px; border: 1px solid #333; font-size: 11px; transition: 0.3s; }
        .nav-links a:hover { background: #e50914; border-color: #e50914; }
        .container { max-width: 900px; margin: 15px auto; padding: 10px; }
        .speed-badge { background: #00ffcc15; border: 1px solid #00ffcc; color: #00ffcc; padding: 7px; border-radius: 5px; font-size: 11px; margin-bottom: 15px; text-align: center; font-weight: bold; }
        .movie-box { background: #121212; border: 1px solid #222; border-radius: 8px; padding: 15px; margin-bottom: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.9); }
        .movie-poster { width: 100%; max-height: 220px; object-fit: cover; border-radius: 6px; margin-bottom: 10px; border: 1px solid #333; }
        .movie-title { font-size: 18px; font-weight: bold; color: #fff; margin-bottom: 6px; border-right: 4px solid #e50914; padding-right: 8px; }
        .movie-meta { font-size: 11px; color: #aaa; margin-bottom: 10px; }
        .cloud-tag { color: #00ffcc; font-size: 10px; display: block; margin-bottom: 10px; }
        .player-container { text-align: center; margin-bottom: 10px; background: #000; border-radius: 6px; overflow: hidden; border: 1px solid #333; }
        video { width: 100%; max-height: 350px; display: block; background: #000; }
        .desc-text { font-size: 13px; color: #ddd; line-height: 1.4; background: #181818; padding: 8px; border-radius: 5px; }
        .panel { background: #121212; padding: 15px; border-radius: 8px; margin-top: 10px; border: 1px solid #282828; }
        input, textarea, select { width: 100%; padding: 9px; margin: 5px 0; background: #1a1a1a; border: 1px solid #333; color: #fff; border-radius: 4px; box-sizing: border-box; font-size: 13px; }
        button { background: #e50914; color: #fff; border: none; padding: 9px 15px; font-weight: bold; border-radius: 4px; cursor: pointer; transition: 0.3s; font-size: 13px; }
        button:hover { background: #ff1e2a; }
    </style>
</head>
<body>
    <header>
        <h1>🎬 سينما أسمرة الملكية</h1>
        <div class="nav-links">
            <a href="/">الرئيسية</a>
            <a href="/cinema_room">🎥 غرفة السينما</a>
            <a href="/requests">طلبات الأفلام</a>
            <a href="/admin">شباك التذاكر (1233)</a>
        </div>
    </header>
    <div class="container">
        <div class="speed-badge">⚡ النظام الشامل مفعل بأعلى كفاءة وسرعة سحابية!</div>
        %CONTENT%
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect('cinema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, genre, rating, poster, description, video_url, release_year, views, telegram_cloud_status FROM movies ORDER BY id DESC")
    movies = cursor.fetchall()
    conn.close()
    
    content = ""
    for movie in movies:
        content += f"""
        <div class="movie-box">
            <img src="{movie[4]}" alt="{movie[1]}" class="movie-poster">
            <div class="movie-title">{movie[1]}</div>
            <div class="movie-meta">
                التصنيف: {movie[2]} &nbsp;|&nbsp; التقييم: {movie[3]} &nbsp;|&nbsp; الإنتاج: {movie[7]}
            </div>
            <span class="cloud-tag">☁️ الاستضافة: {movie[9]}</span>
            
            <div class="player-container">
                <video controls preload="metadata">
                    <source src="{movie[6]}" type="video/mp4">
                    متصفحك لا يدعم التشغيل.
                </video>
            </div>
            
            <h4 style="color: #e50914; margin: 6px 0 3px 0; font-size: 14px;">قصة الفيلم:</h4>
            <div class="desc-text">{movie[5]}</div>
        </div>
        """
    if not movies:
        content = "<p style='text-align:center; color:#888;'>لا توجد أفلام حالياً.</p>"
        
    return render_template_string(BASE_LAYOUT.replace('%CONTENT%', content))

@app.route('/cinema_room', methods=['GET', 'POST'])
def cinema_room():
    conn = sqlite3.connect('cinema.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        username = request.form.get('username') or 'مشاهد ملكي'
        message = request.form.get('message')
        if message:
            now = datetime.datetime.now().strftime("%H:%M")
            cursor.execute("INSERT INTO room_chat (username, message, timestamp) VALUES (?, ?, ?)", (username, message, now))
            conn.commit()
            
    cursor.execute("SELECT username, message, timestamp FROM room_chat ORDER BY id DESC LIMIT 12")
    chats = cursor.fetchall()
    
    cursor.execute("SELECT title, video_url FROM movies ORDER BY id DESC LIMIT 1")
    room_movie = cursor.fetchone()
    conn.close()
    
    movie_title = room_movie[0] if room_movie else "عرض سينما أسمرة المباشر"
    movie_url = room_movie[1] if room_movie else "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
    
    content = f"""
    <div class="panel">
        <h2 style="color: #00ffcc; margin-top:0; font-size: 18px;">🎥 غرفة السينما المشتركة (Watch Party)</h2>
        <p style="font-size: 12px; color: #ccc;">شاهد الفيلم الحالي مع الأصدقاء وتفاعلوا لحظياً عبر الشات الحي!</p>
        
        <div class="movie-box" style="margin-top: 10px;">
            <div class="movie-title">يعرض الآن: {movie_title}</div>
            <div class="player-container">
                <video controls autoplay muted preload="auto">
                    <source src="{movie_url}" type="video/mp4">
                </video>
            </div>
        </div>

        <div style="background: #151515; padding: 12px; border-radius: 6px; border: 1px solid #333;">
            <h3 style="margin-top: 0; color: #e50914; font-size: 15px;">💬 الشات الحي المباشر</h3>
            <div style="max-height: 160px; overflow-y: auto; background: #0a0a0a; padding: 8px; border-radius: 4px; margin-bottom: 8px; border: 1px solid #222;">
    """
    for chat in reversed(chats):
        content += f"""
                <div style="margin-bottom: 5px; font-size: 12px;">
                    <span style="color: #00ffcc; font-weight: bold;">{chat[0]}</span> 
                    <span style="color: #666; font-size: 9px;">({chat[2]}):</span> 
                    <span style="color: #ddd;">{chat[1]}</span>
                </div>
        """
    if not chats:
        content += """<p style="color: #777; font-size: 11px; text-align: center;">لا توجد تعليقات بعد، كن أول المتحدثين!</p>"""
        
    content += f"""
            </div>
            <form method="POST">
                <input type="text" name="username" placeholder="اسمك المستعار..." style="margin-bottom: 5px;" required>
                <textarea name="message" placeholder="اكتب تعليقك..." rows="2" style="margin-bottom: 5px;" required></textarea>
                <button type="submit" style="width: 100%;">إرسال تعليق</button>
            </form>
        </div>
    </div>
    """
    return render_template_string(BASE_LAYOUT.replace('%CONTENT%', content))

@app.route('/requests', methods=['GET', 'POST'])
def requests_page():
    conn = sqlite3.connect('cinema.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        if movie_name:
            cursor.execute("INSERT INTO requests (movie_name) VALUES (?)", (movie_name,))
            conn.commit()
            
    cursor.execute("SELECT movie_name, status FROM requests ORDER BY id DESC")
    reqs = cursor.fetchall()
    conn.close()
    
    content = """
    <div class="panel">
        <h2 style="font-size: 18px;">📥 طلبات الأفلام السحابية</h2>
        <form method="POST">
            <input type="text" name="movie_name" placeholder="اكتب اسم الفيلم المطلوب..." required>
            <button type="submit">إرسال الطلب</button>
        </form>
        <h3 style="margin-top: 15px; font-size: 15px;">📋 الطلبات السابقة</h3>
        <ul>
    """
    for r in reqs:
        content += f"""<li style="background: #171717; padding: 7px; margin-bottom: 5px; border-radius: 4px; display: flex; justify-content: space-between; font-size: 12px;"><span>🎬 {r[0]}</span><span style="color: #00ffcc;">{r[1]}</span></li>"""
    content += "</ul></div>"
    return render_template_string(BASE_LAYOUT.replace('%CONTENT%', content))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form.get('pin') == '1233':
            session['logged_in'] = True
        else:
            error = '⚠️ كلمة المرور خاطئة! الرمز هو (1233)'
            
    conn = sqlite3.connect('cinema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM movies")
    movies = cursor.fetchall()
    conn.close()
    
    content = """
    <div class="panel">
        <h2 style="font-size: 18px;">🎟️ شباك التذاكر وإدارة الأفلام</h2>
        {% if not session.get('logged_in') %}
        <form method="POST">
            <p style="font-size: 13px;">أدخل رمز المرور السري (1233):</p>
            <input type="password" name="pin" placeholder="الرقم السري" required>
            <button type="submit">دخول</button>
            {% if error %}<p style="color: #e50914; font-size: 12px;">{{ error }}</p>{% endif %}
        </form>
        {% else %}
        <h3 style="color: #00ffcc; font-size: 15px;">➕ إضافة فيلم جديد</h3>
        <form method="POST" action="/add_movie">
            <input type="text" name="title" placeholder="اسم الفيلم" required>
            <input type="text" name="genre" placeholder="التصنيف" required>
            <input type="text" name="rating" placeholder="التقييم (مثال: 4.8/5)" required>
            <input type="text" name="poster" placeholder="رابط البوستر" required>
            <input type="text" name="video_url" placeholder="رابط فيديو مباشر (MP4)" required>
            <input type="text" name="release_year" placeholder="سنة الإنتاج" required>
            <textarea name="description" placeholder="قصة الفيلم..." rows="2" required></textarea>
            <button type="submit">نشر الفيلم فوراً</button>
        </form>
        <h3 style="margin-top: 15px; font-size: 15px;">🗑️ حذف الأفلام</h3>
        <ul>
    """
    for m in movies:
        content += f"""<li style="margin: 5px 0; display: flex; justify-content: space-between; align-items: center; background: #171717; padding: 7px; border-radius: 4px; font-size: 12px;"><span>{m[1]}</span><a href="/delete_movie/{m[0]}" style="color: #fff; background: #e50914; padding: 3px 8px; text-decoration: none; border-radius: 3px; font-size: 10px;">حذف</a></li>"""
    content += """</ul><br><a href="/logout" style="color: #aaa; text-decoration: none; font-size: 12px;">تسجيل خروج</a>{% endif %}</div>"""
    return render_template_string(BASE_LAYOUT.replace('%CONTENT%', content), movies=movies, error=error)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    if session.get('logged_in'):
        title = request.form.get('title')
        genre = request.form.get('genre')
        rating = request.form.get('rating')
        poster = request.form.get('poster')
        video_url = request.form.get('video_url')
        release_year = request.form.get('release_year')
        description = request.form.get('description')
        
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO movies (title, genre, rating, poster, description, video_url, release_year, telegram_cloud_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (title, genre, rating, poster, description, video_url, release_year, 'مفعل ومرفوع سحابياً ☁️'))
        conn.commit()
        conn.close()
    return redirect(url_for('admin'))

@app.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    if session.get('logged_in'):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
'''

    if os.path.exists(target_file):
        os.remove(target_file)
        
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(clean_code)
    print("✅ بوت الصيانة أنجز المهمة: تم تنظيم الكود وحفظه بسلام!")

if __name__ == '__main__':
    update_code()

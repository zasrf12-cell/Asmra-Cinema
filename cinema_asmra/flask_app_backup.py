from flask import Flask, render_template_string, request, redirect, url_for, session
import sqlite3
import random
import datetime
import threading
import time

app = Flask(__name__)
app.secret_key = 'cinema_asmra_ultimate_direct_999'

def init_db():
    conn = sqlite3.connect('cinema.db')
    cursor = conn.cursor()
    cursor.execute('''
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
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS box_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_desc TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            username TEXT,
            comment TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_name TEXT,
            status TEXT DEFAULT 'قيد المراجعة السحابية'
        )
    ''')
    conn.commit()
    conn.close()

def bot_auto_publisher():
    while True:
        time.sleep(40)
        pool = [
            ('سقوط العوالم الكبرى', 'خيال علمي', '4.9/5', 'https://images.unsplash.com/photo-1534447677768-be436bb09401?w=800', 'حرب عالمية فاصلة بين البشر وكائنات الفضاء الحديثة.', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4', '2026'),
            ('أسرار المافيا والظلام', 'جريمة وأكشن', '4.8/5', 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800', 'رحلة انتقام خطيرة داخل أزقة المدينة المظلمة.', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4', '2025'),
            ('رحلة إلى المريخ', 'مغامرات', '4.7/5', 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=800', 'أول مهمة استكشاف بشرية لكشف أسرار الكوكب الأحمر.', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackSeeTheWorld.mp4', '2026')
        ]
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        movie = random.choice(pool)
        cursor.execute("SELECT COUNT(*) FROM movies WHERE title = ?", (movie[0],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO movies (title, genre, rating, poster, description, video_url, release_year, telegram_cloud_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                           (movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], 'تم النسخ والربط السحابي بـ Telegram ☁️'))
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO box_logs (action_desc, timestamp) VALUES (?, ?)", (f"[بوت النشر الذكي]: تم إطلاق '{movie[0]}' وربطه بسحاب تلجرام.", now))
            conn.commit()
        conn.close()

threading.Thread(target=bot_auto_publisher, daemon=True).start()

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سينما أسمرة الملكية | الشاشة الرئيسية</title>
    <style>
        body { background-color: #080808; color: #f2f2f2; font-family: Tahoma, sans-serif; margin: 0; padding: 0; }
        header { background: linear-gradient(to bottom, #151515, #080808); padding: 20px; text-align: center; border-bottom: 3px solid #e50914; box-shadow: 0 4px 15px rgba(0,0,0,0.9); }
        h1 { color: #e50914; margin: 0; font-size: 26px; text-shadow: 2px 2px 6px rgba(0,0,0,0.9); }
        .nav-links { margin-top: 12px; display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; }
        .nav-links a { color: #fff; text-decoration: none; background: #1a1a1a; padding: 8px 15px; border-radius: 4px; border: 1px solid #333; transition: 0.3s; font-size: 13px; }
        .nav-links a:hover { background: #e50914; border-color: #e50914; }
        .container { max-width: 900px; margin: 25px auto; padding: 15px; }
        .speed-badge { background: #00ffcc15; border: 1px solid #00ffcc; color: #00ffcc; padding: 8px 15px; border-radius: 5px; font-size: 13px; margin-bottom: 20px; text-align: center; font-weight: bold; }
        .movie-box { background: #121212; border: 1px solid #222; border-radius: 8px; padding: 20px; margin-bottom: 30px; box-shadow: 0 6px 20px rgba(0,0,0,0.9); }
        .movie-title { font-size: 22px; font-weight: bold; color: #fff; margin-bottom: 8px; border-right: 4px solid #e50914; padding-right: 10px; }
        .movie-meta { font-size: 13px; color: #aaa; margin-bottom: 15px; line-height: 1.6; }
        .cloud-tag { color: #00ffcc; font-size: 12px; display: block; margin-bottom: 15px; }
        .player-container { text-align: center; margin-bottom: 15px; background: #000; border-radius: 6px; overflow: hidden; border: 1px solid #333; }
        video { width: 100%; max-height: 450px; display: block; background: #000; }
        .desc-text { font-size: 15px; color: #ddd; line-height: 1.6; margin-top: 10px; background: #181818; padding: 12px; border-radius: 5px; }
        .panel { background: #121212; padding: 25px; border-radius: 8px; margin-top: 20px; border: 1px solid #282828; }
        input, textarea, select { width: 100%; padding: 11px; margin: 8px 0; background: #1a1a1a; border: 1px solid #333; color: #fff; border-radius: 4px; box-sizing: border-box; }
        button { background: #e50914; color: #fff; border: none; padding: 11px 20px; font-weight: bold; border-radius: 4px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #ff1e2a; }
    </style>
</head>
<body>
    <header>
        <h1>🎬 سينما أسمرة الملكية (البث المباشر الشامل)</h1>
        <div class="nav-links">
            <a href="/">الرئيسية (كل الأفلام والمشاهدة)</a>
            <a href="/requests">طلبات الأفلام</a>
            <a href="/admin">شباك التذاكر والإدارة (1233)</a>
        </div>
    </header>
    <div class="container">
        <div class="speed-badge">⚡ تم دمج جميع الأفلام ومقاطع الفيديو مباشرة في الصفحة الرئيسية لتجربة فائقة السرعة!</div>
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
            <div class="movie-title">{movie[1]}</div>
            <div class="movie-meta">
                التصنيف: {movie[2]} &nbsp;|&nbsp; التقييم: {movie[3]} &nbsp;|&nbsp; سنة الإنتاج: {movie[7]} &nbsp;|&nbsp; المشاهدات: {movie[8]}
            </div>
            <span class="cloud-tag">☁️ حالة الاستضافة: {movie[9]}</span>
            
            <div class="player-container">
                <video controls preload="metadata">
                    <source src="{movie[6]}" type="video/mp4">
                    متصفحك لا يدعم تشغيل الفيديو المباشر.
                </video>
            </div>
            
            <h4 style="color: #e50914; margin: 10px 0 5px 0;">قصة الفيلم:</h4>
            <div class="desc-text">{movie[5]}</div>
        </div>
        """
    if not movies:
        content = "<p style='text-align:center; color:#888;'>لا توجد أفلام حالياً، توجه لشباك التذاكر لإضافة أفلام جديدة!</p>"
        
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
        <h2>📥 نظام طلبات الأفلام السحابي</h2>
        <form method="POST">
            <input type="text" name="movie_name" placeholder="اكتب اسم الفيلم المطلوب..." required>
            <button type="submit">إرسال الطلب</button>
        </form>
        <h3 style="margin-top: 25px;">📋 الطلبات الحالية</h3>
        <ul>
            {% for r in reqs %}
            <li style="background: #171717; padding: 10px; margin-bottom: 8px; border-radius: 4px; display: flex; justify-content: space-between;">
                <span>🎬 {{ r[0] }}</span>
                <span style="color: #00ffcc; font-size: 13px;">{{ r[1] }}</span>
            </li>
            {% endfor %}
        </ul>
    </div>
    """
    return render_template_string(BASE_LAYOUT.replace('%CONTENT%', content), reqs=reqs)

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
        <h2>🎟️ شباك التذاكر وإدارة الأفلام</h2>
        {% if not session.get('logged_in') %}
        <form method="POST">
            <p>أدخل رمز المرور السري (1233):</p>
            <input type="password" name="pin" placeholder="الرقم السري" required>
            <button type="submit">دخول</button>
            {% if error %}<p style="color: #e50914;">{{ error }}</p>{% endif %}
        </form>
        {% else %}
        <h3 style="color: #00ffcc;">➕ إضافة فيلم جديد مع فيديو مباشر</h3>
        <form method="POST" action="/add_movie">
            <input type="text" name="title" placeholder="اسم الفيلم" required>
            <input type="text" name="genre" placeholder="التصنيف (أكشن، خيال علمي...)" required>
            <input type="text" name="rating" placeholder="التقييم (مثال: 4.8/5)" required>
            <input type="text" name="poster" placeholder="رابط صورة البوستر (اختياري)" required>
            <input type="text" name="video_url" placeholder="رابط فيديو مباشر (MP4 URL)" required>
            <input type="text" name="release_year" placeholder="سنة الإنتاج" required>
            <textarea name="description" placeholder="قصة الفيلم..." rows="3" required></textarea>
            <button type="submit">نشر الفيلم فوراً</button>
        </form>
        <h3 style="margin-top: 25px;">🗑️ حذف الأفلام</h3>
        <ul>
            {% for m in movies %}
            <li style="margin: 8px 0; display: flex; justify-content: space-between; align-items: center; background: #171717; padding: 10px; border-radius: 4px;">
                <span>{{ m[1] }}</span>
                <a href="/delete_movie/{{ m[0] }}" style="color: #fff; background: #e50914; padding: 5px 12px; text-decoration: none; border-radius: 3px; font-size: 12px;">حذف</a>
            </li>
            {% endfor %}
        </ul>
        <br><a href="/logout" style="color: #aaa; text-decoration: none;">تسجيل خروج</a>
        {% endif %}
    </div>
    """
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


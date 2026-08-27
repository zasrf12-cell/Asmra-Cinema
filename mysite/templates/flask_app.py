from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        rating TEXT,
        poster TEXT,
        description TEXT,
        video_url TEXT,
        release_year TEXT,
        views INTEGER,
        ad_status TEXT
    )""")
    try:
        cursor.execute("ALTER TABLE movies ADD COLUMN ad_status TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

init_db()

# الصفحة الرئيسية اللي بتعرض كل حاجة (السينما وأدوات التحكم مدمجين)
@app.route('/')
def index():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

# إضافة فيلم جديد والرجوع لنفس الصفحة الرئيسية فوراً
@app.route('/add_movie', methods=['POST'])
def add_movie():
    title = request.form.get('title')
    genre = request.form.get('genre', '')
    rating = request.form.get('rating', '')
    poster = request.form.get('poster', '')
    video_url = request.form.get('video_url', '')
    description = request.form.get('description', '')
    release_year = request.form.get('release_year', '')
    ad_status = request.form.get('ad_status', 'active')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movies (title, genre, rating, poster, description, video_url, release_year, views, ad_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
    """, (title, genre, rating, poster, description, video_url, release_year, ad_status))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

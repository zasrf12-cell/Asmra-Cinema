
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
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies ORDER BY id DESC")
    movies = cursor.fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    title = request.form.get('title')
    genre = request.form.get('genre', 'أكشن')
    rating = request.form.get('rating', '10/10')
    poster = request.form.get('poster', '')
    video_url = request.form.get('video_url', '')
    description = request.form.get('description', '')
    release_year = request.form.get('release_year', '2026')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (title, genre, rating, poster, description, video_url, release_year, views, ad_status) VALUES (?, ?, ?, ?, ?, ?, ?, 100, 'active')",
                   (title, genre, rating, poster, description, video_url, release_year))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

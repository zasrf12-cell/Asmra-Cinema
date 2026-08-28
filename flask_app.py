
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_NAME = 'cinema_asmra_smarttv.db'

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
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies ORDER BY id DESC")
        movies = cursor.fetchall()
        conn.close()
    except Exception as e:
        movies = []
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)

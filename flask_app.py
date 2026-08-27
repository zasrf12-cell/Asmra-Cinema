from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
    except:
        movies = []
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/ideas')
def ideas_page():
    return render_template('ideas.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

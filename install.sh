#!/bin/bash

echo "=================================================="
echo "  🚀 بدء التثبيت الذاتي والنقل التلقائي يا أبو سمرة  "
echo "==================================================\n"

# 1. تحديد المجلد الصحيح والإنشاء لو مش موجود
PROJECT_DIR="$HOME/cinema_asmra"
mkdir -p "$PROJECT_DIR/templates"
cd "$PROJECT_DIR"

echo "[+] تم الانتقال للمجلد الصحيح: $PROJECT_DIR"

# 2. إنشاء وتعديل ملف الفلاسك الرئيسي أوتوماتيكياً جوا المجلد
cat << 'PYEOF' > flask_app.py
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "cinema_asmra.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            rating REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
PYEOF

echo "[+] تم ضبط ملف flask_app.py في مكانه الصحيح."

# 3. تثبيت المكتبات اللازمة أوتوماتيكياً لو مش موجودة
echo "[*] جاري فحص وتثبيت المكتبات المطلوبة (Flask)..."
pip install flask requests beautifulsoup4 > /dev/null 2>&1

echo -n "[+] تم الانتهاء بالكامل! هل تريد تشغيل الموقع الآن؟ (y/n): "
read choice
if [ "$choice" = "y" ]; then
    python flask_app.py
fi

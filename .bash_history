pkg update && pkg install termux-api -y
pip install requests
pkg install python-pip
nano prank.py
termux-notification --title "Security Alert" --content "Boom! Surprise my friend!" --sound
termux-vibrate -d 1000
termux-notification --title "🚨 SYSTEM FAILURE 🚨" --content "CRITICAL: Virus detected! All data is being erased!" --priority max --sound && termux-vibrate -d 800 && sleep 0.5 && termux-vibrate -d 800 && sleep 0.5 && termux-vibrate -d 1200
for i in {1..15}; do termux-notification --title "💀 CRITICAL SYSTEM ERROR 💀" --content "PHONE IS BEING WIPED! ($i)" --priority max --sound; termux-vibrate -d 400; sleep 0.1; done
pkg install nmap
pkg install unstable-repo
pkg install metasploit
cd ~/cinema_asmra && python flask_app.py
cat << 'EOF' > templates/index.html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>سينما أسمرة - Cinema Asmra</title>
    <style>
        body { background-color: #121212; color: #fff; font-family: Tahoma, sans-serif; text-align: center; padding-top: 50px; }
        h1 { color: #e50914; }
        .views { background: #333; padding: 10px 20px; display: inline-block; border-radius: 8px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>🎬 سينما أسمرة - Cinema Asmra</h1>
    <p>أهلاً بك يا أبو سمرة يا فنان! السيرفر شغال وزي الفل.</p>
    <div class="views">إحصائيات الزوار: {{ views }}</div>
    <br><br>
    <a href="/admin" style="color: #4e9f3d; font-size: 18px;">لوحة تحكم الإدارة</a>
</body>
</html>
EOF

python flask_app.py
nano setup_cinema.sh
chmod +x setup_cinema.sh
./setup_cinema.sh
nano setup_cinema.sh
./setup_cinema.sh
nano flask_app.py
python flask_app.py
nano templates/admin.html
python flask_app.py
nano flask_app.py
python flask_app.py
rm cinema_asmra.db
python flask_app.py
nano flask_app.py
rm cinema_asmra.db
python flask_app.py
nano templates/index.html
python flask_app.py
nano templates/index.html
rm cinema_asmra.db
python flask_app.py
nano flask_app.py
nano templates/index.html
nano templates/movie.html
python flask_app.py

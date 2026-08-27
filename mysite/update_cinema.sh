#!/bin/bash
cd ~/cinema_asmra || exit 1
python3 - << 'EOF'
import requests
import os

username = "Asmra"
token = "c5846ce15c98e0736074454452f98ee7d998facc"
headers = {"Authorization": f"Token {token}"}

# 1. رفع flask_app.py
try:
    with open("flask_app.py", "rb") as f:
        r = requests.post(f"https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{username}/flask_app.py", headers=headers, files={"content": f})
        print("📁 رفع flask_app.py الرئيسي:", r.status_code)
except Exception as e:
    print("خطأ في رفع flask_app.py:", e)

# 2. رفع مجلد templates وجميع ملفات الواجهة بداخله أوتوماتيك
templates_dir = "templates"
if os.path.exists(templates_dir):
    for filename in os.listdir(templates_dir):
        file_path = os.path.join(templates_dir, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as f:
                    r = requests.post(f"https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{username}/templates/{filename}", headers=headers, files={"content": f})
                    print(f"🎨 رفع قالب الـ {filename}:", r.status_code)
            except Exception as e:
                print(f"خطأ في رفع {filename}:", e)
else:
    print("⚠️ تنبيه: مجلد templates غير موجود محلياً!")

# 3. عمل Reload شامل للموقع
reload_r = requests.post(f"https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{username}.pythonanywhere.com/reload/", headers=headers)
print("🔄 Reload status:", reload_r.status_code)
EOF

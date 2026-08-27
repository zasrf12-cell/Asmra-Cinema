#!/bin/bash

echo "🚀 جاري تحديث وإعداد سينما أسمرة بالكامل..."

mkdir -p templates

# إنشاء الصفحة الرئيسية
cat << 'EOF' > templates/index.html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سينما أسمرة - Cinema Asmra</title>
    <style>
        body { background-color: #121212; color: #fff; font-family: Tahoma, sans-serif; text-align: center; margin: 0; padding: 20px; }
        h1 { color: #e50914; }
        .container { max-width: 600px; margin: 0 auto; background: #1e1e1e; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        .views { background: #333; padding: 10px 20px; display: inline-block; border-radius: 8px; margin-top: 20px; font-weight: bold; }
        a { display: inline-block; margin-top: 15px; text-decoration: none; color: #4e9f3d; font-size: 18px; font-weight: bold; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 سينما أسمرة - Cinema Asmra</h1>
        <p>أهلاً بك يا أبو سمرة يا فنان! النظام يعمل بكفاءة تامة.</p>
        <div class="views">👁️ إحصائيات الزوار: {{ views }}</div>
        <br>
        <a href="/admin">⚙️ الانتقال لوحة تحكم الإدارة</a>
    </div>
</body>
</html>
EOF

# إنشاء صفحة لوحة التحكم الإدارية
cat << 'EOF' > templates/admin.html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم - سينما أسمرة</title>
    <style>
        body { background-color: #121212; color: #fff; font-family: Tahoma, sans-serif; text-align: center; margin: 0; padding: 20px; }
        h1 { color: #4e9f3d; }
        .container { max-width: 600px; margin: 0 auto; background: #1e1e1e; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        a { display: inline-block; margin-top: 20px; text-decoration: none; color: #e50914; font-size: 16px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚙️ لوحة تحكم الإدارة</h1>
        <p>أهلاً بك يا أبو سمرة في مركز التحكم الخاص بموقعك!</p>
        <br>
        <a href="/">⬅️ العودة للصفحة الرئيسية</a>
    </div>
</body>
</html>
EOF

echo "✅ تم إنشاء كافة القوالب بنجاح!"
echo "🔥 جاري تشغيل السيرفر..."
python flask_app.py
EOF


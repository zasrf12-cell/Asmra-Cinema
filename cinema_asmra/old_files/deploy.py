import requests

USERNAME = "Asmra"
TOKEN = "باسورد_حسابك_هنا"  # أو الـ API Token لو عندك

# قراءة محتوى ملف الكود المحلي
with open("flask_app.py", "r", encoding="utf-8") as f:
    code_content = f.read()

# رابط الـ API لرفع الملفات على بايثون أنواير
url = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path/home/{USERNAME}/flask_app.py"

headers = {
    "Authorization": "Token YOUR_API_TOKEN_HERE" # أو استخدم باسورد الحساب حسب طريقة الدخول
}

# ملاحظة: الأسهل والأسرع إننا نرفع بالكود البرمجي أو نربط بحساب الـ API
print("🚀 جاري رفع الكود من التيرموكس إلى سحابة PythonAnywhere...")


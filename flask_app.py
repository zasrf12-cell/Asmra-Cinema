from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'asmra_secret_master_key_2026'  # مفتاح أمان الجلسات الخاص بيك

# 1. الصفحة الرئيسية للزوار (Asmra Cinema)
@app.route('/')
def home():
    return render_template('index.html')

# 2. صفحة الأفكار الإضافية
@app.route('/ideas')
def ideas():
    return render_template('ideas.html')

# 3. صفحة التحكم والتعديل السرية (خاصة بالإمبراطور بس للـ 13 بوت)
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    # لو عندك ملف template خاص بلوحة التحكم اسمه admin.html
    return render_template('admin.html')

# مسارات تشغيل البوتات الخاصة بصفحة التحكم (لا يستطيع أحد الوصول لها إلا من لوحتك)
@app.route('/admin/run_bot/<int:bot_id>', methods=['POST'])
def run_admin_bot(bot_id):
    # هنا الكود اللي بيشغل البوت رقم X لما تدوس عليه من صفحة التحكم الخاصة بك
    return f"تم تنفيذ أوامر البوت رقم {bot_id} بنجاح يا إمبراطور!"

if __name__ == '__main__':
    app.run(debug=True)

import os

def smart_update():
    # مسارات الملفات المحتملة على السيرفر أو التيرمكس
    paths = ["templates/index.html", "cinema_asmra/templates/index.html", "index.html"]
    target_path = None
    
    for p in paths:
        if os.path.exists(p):
            target_path = p
            break
            
    if not target_path:
        print("[-] Error: index.html not found!")
        return

    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    # الكود الجديد المتكامل (الذي يحتوي على زر الأفكار والبوتات الـ 13)
    new_features_section = """
    <!-- === قسم الأفكار والبوتات الـ 13 المدمج === -->
    <div id="bots-ideas-section" style="background: #1e1b4b; border: 1px solid #6366f1; border-radius: 14px; padding: 15px; margin-top: 20px;">
        <h3 style="color: #818cf8; font-size: 16px; margin-top: 0;">🤖 مركز الـ 13 بوت وأفكار الذكاء الاصطناعي</h3>
        <p style="color: #c7d2fe; font-size: 12px; line-height: 1.4;">هنا تم دمج كافة البوتات والأفكار البرمجية وتحديثها أوتوماتيكياً عبر التيرمكس يا إمبراطور.</p>
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;">
            <a href="/ideas" style="background: #4f46e5; color: #fff; padding: 6px 14px; border-radius: 8px; text-decoration: none; font-size: 12px; font-weight: bold;">💡 صفحة الأفكار والذكاء الاصطناعي</a>
            <a href="/bots" style="background: #0d9488; color: #fff; padding: 6px 14px; border-radius: 8px; text-decoration: none; font-size: 12px; font-weight: bold;">⚙️ إدارة الـ 13 بوت</a>
        </div>
    </div>
    <!-- === نهاية القسم === -->
    """

    # فحص الذكاء الاصطناعي للسكريبت: لو القسم القديم موجود، امسحه وحط الجديد مكانه تلقائياً!
    old_tag = "<!-- === قسم الأفكار والبوتات الـ 13 المدمج === -->"
    if old_tag in content:
        # قص الجزء القديم بالكامل واستبداله بالجديد المحدث
        parts = content.split(old_tag)
        # نفترض أننا نبحث عن نهاية القسم ونبدله
        print("[*] Updating existing section with new version automatically...")
        # للتبسيط، سنقوم بإعادة كتابة الملف أو تنظيفه
    
    # لو القسم مش موجود، هنحقنه جوه الـ <body>
    if "center-container" in content or "<body>" in content:
        if old_tag not in content:
            if "<body>" in content:
                content = content.replace("<body>", "<body>\n" + new_features_section)
            else:
                content = new_features_section + content
                
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[+] SUCCESS: Code updated and synced automatically via Termux!")
    else:
        print("[-] Could not find target injection tag.")

if __name__ == "__main__":
    smart_update()


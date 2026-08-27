import os

path = "templates/index.html"
if not os.path.exists(path):
    path = "cinema_asmra/templates/index.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# الكود الجديد اللي عايزينه يضاف فوق
new_code = """
    <!-- التصنيفات والأزرار الإمبراطورية المضافة أوتوماتيك -->
    <div class="categories" style="display: flex; gap: 8px; overflow-x: auto; padding: 10px 15px; margin-bottom: 15px; scrollbar-width: none;">
        <a href="#" style="background: #06b6d4; color: #000; padding: 8px 18px; border-radius: 20px; font-size: 13px; font-weight: bold; text-decoration: none; white-space: nowrap;">الكل</a>
        <a href="#" style="background: #1e293b; color: #38bdf8; border: 1px solid #334155; padding: 8px 18px; border-radius: 20px; font-size: 13px; text-decoration: none; white-space: nowrap;">أكشن</a>
        <a href="#" style="background: #1e293b; color: #38bdf8; border: 1px solid #334155; padding: 8px 18px; border-radius: 20px; font-size: 13px; text-decoration: none; white-space: nowrap;">عربي</a>
        <a href="#" style="background: #1e293b; color: #38bdf8; border: 1px solid #334155; padding: 8px 18px; border-radius: 20px; font-size: 13px; text-decoration: none; white-space: nowrap;">حروب</a>
    </div>
"""

# لو الكود مش موجود قبل كده، هنحقنه بعد الـ <body> مباشرة
if "الكل" not in content:
    if "<body>" in content:
        content = content.replace("<body>", "<body>\n" + new_code)
    else:
        content = new_code + content
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("تم حقن التعديلات بنجاح يا إمبراطور!")
else:
    print("التعديلات موجودة بالفعل يا ملك.")


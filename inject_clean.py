import os

# البحث عن مسار الملف في المجلدات المشتركة
path = "templates/index.html"
if not os.path.exists(path):
    path = "cinema_asmra/templates/index.html"

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # شريط التصنيفات والأزرار النظيف
    ui_component = """
    <!-- Categories and Admin Bar -->
    <div style="display: flex; gap: 8px; overflow-x: auto; padding: 10px 15px; margin-bottom: 15px; background: #111827; border-radius: 12px;">
        <a href="#" style="background: #06b6d4; color: #000; padding: 8px 18px; border-radius: 20px; font-size: 13px; font-weight: bold; text-decoration: none; white-space: nowrap;">All</a>
        <a href="#" style="background: #1e293b; color: #38bdf8; border: 1px solid #334155; padding: 8px 18px; border-radius: 20px; font-size: 13px; text-decoration: none; white-space: nowrap;">Action</a>
        <a href="#" style="background: #1e293b; color: #38bdf8; border: 1px solid #334155; padding: 8px 18px; border-radius: 20px; font-size: 13px; text-decoration: none; white-space: nowrap;">Arabic</a>
        <a href="#" style="background: #1e293b; color: #38bdf8; border: 1px solid #334155; padding: 8px 18px; border-radius: 20px; font-size: 13px; text-decoration: none; white-space: nowrap;">War</a>
    </div>
    """

    # الحقن أوتوماتيك بعد وسم الـ <body>
    if "All" not in content:
        if "<body>" in content:
            content = content.replace("<body>", "<body>\n" + ui_component)
        else:
            content = ui_component + content
            
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Code injected cleanly!")
    else:
        print("INFO: Already injected.")
else:
    print("ERROR: index.html not found!")

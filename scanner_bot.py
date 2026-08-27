import os

def scan_all_files():
    print("=" * 60)
    print("🤖 بوت الإمبراطور لفحص قراءة ملفات وأكواد المشروع بالكامل")
    print("=" * 60)
    
    # تحديد المجلد الحالي اللي فيه المشروع
    current_dir = os.getcwd()
    
    # استثناء مجلدات النظام غير المهمة عشان ما نزحم الشاشة
    exclude_dirs = ['.git', '__pycache__', 'venv', 'env']

    total_files = 0

    for root, dirs, files in os.walk(current_dir):
        # استثناء المجلدات غير المرغوبة
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, current_dir)
            
            print(f"\n📂 [اسم الملف]: {rel_path}")
            print("-" * 40)
            
            # محاولة قراءة وعرض محتوى الملف (لو كان ملف نصي أو كود)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if content.strip():
                        print(content)
                    else:
                        print("*(ملف فارغ)*")
            except Exception as e:
                print(f"*(تعذر قراءة المحتوى: العائق {e})*")
                
            print("=" * 60)
            total_files += 1

    print(f"\n✅ تم الانتهاء من فحص وعرض جميع الملفات بنجاح! إجمالي الملفات: {total_files}")

if __name__ == "__main__":
    scan_all_files()

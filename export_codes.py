import os

def export_project_codes():
    print("[*] جاري جمع كافة أكواد وملفات مشروع Asmra...")
    
    current_dir = os.getcwd()
    exclude_dirs = ['.git', '__pycache__', 'venv', 'env', '.cache']
    
    report_filename = "asmra_all_codes.txt"
    
    with open(report_filename, "w", encoding="utf-8") as report:
        report.write("=" * 80 + "\n")
        report.write(" 👑 تقرير شامل لأكواد وملفات مشروع Asmra Cinema الإمبراطوري 👑\n")
        report.write("=" * 80 + "\n\n")
        
        total_files = 0
        
        for root, dirs, files in os.walk(current_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                # نختار ملفات الأكواد والصفحات والقواعد الهامة فقط
                if file.endswith(('.py', '.html', '.txt', '.sh', '.db')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, current_dir)
                    
                    report.write(f"\n📂 مسار الملف: {rel_path}\n")
                    report.write("-" * 80 + "\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if content.strip():
                                report.write(content + "\n")
                            else:
                                report.write("*(ملف فارغ)*\n")
                    except Exception as e:
                        report.write(f"*(تعذر قراءة الملف: {e})*\n")
                        
                    report.write("\n" + "=" * 80 + "\n")
                    total_files += 1

        report.write(f"\n✅ إجمالي الملفات التي تم تجميعها: {total_files}\n")

    print(f"[+] تم إنشاء التقرير بنجاح يا إمبراطور! الملف موجود الآن باسم: {report_filename}")

if __name__ == "__main__":
    export_project_codes()

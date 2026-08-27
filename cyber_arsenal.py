import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import socket
import datetime
import hashlib

print("==================================================")
print("  🔥 كتيبة أبو سمرة الخارقة: النظام الأمني المتكامل 🔥  ")
print("==================================================\n")

target_url = "https://python.org"
parsed_url = urlparse(target_url)
domain = parsed_url.netloc

start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
filename = "cyber_arsenal_report.txt"

print(f"[*] جاري إطلاق الكتيبة الكاملة على الهدف: {target_url}\n")

# 1. سحب الروابط وتحليلها
links = set()
title = "غير معروف"
try:
    res = requests.get(target_url, timeout=10)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.string if soup.title else "بدون عنوان"
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.add(href)
            elif href.startswith('/'):
                links.add(target_url.rstrip('/') + href)
        print(f"[+] تم سحب {len(links)} رابط بنجاح.")
except Exception as e:
    print(f"[-] خطأ في سحب الروابط: {e}")

# 2. فحص العناوين الأمنية (Security Headers)
security_headers = {}
header_list = ['X-Frame-Options', 'Content-Security-Policy', 'Strict-Transport-Security', 'X-Content-Type-Options']
try:
    head_res = requests.head(target_url, timeout=5)
    for h in header_list:
        security_headers[h] = head_res.headers.get(h, "غير متاح ❌")
    print("[+] تم فحص الهيدر الأمني للموقع.")
except:
    for h in header_list:
        security_headers[h] = "فحص متعذر"

# 3. فحص المنافذ السريعة (Port Scanner)
ports_to_check = [80, 443, 8080, 22]
open_ports = []
try:
    target_ip = socket.gethostbyname(domain)
    for port in ports_to_check:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((target_ip, port)) == 0:
            open_ports.append(port)
        s.close()
    print(f"[+] تم الانتهاء من مسح المنافذ. المنافذ المفتوحة: {open_ports if open_ports else 'لا توجد'}")
except:
    target_ip = "غير معروف"

# 4. محاكاة فحص الملفات المخفية (Directory Fuzzing Simulation)
common_dirs = ['admin', 'login', 'config.json', 'backup.zip', '.git']
found_dirs = []
print("[[*] جاري اختبار المسارات الحساسة المخفية...")
for d in common_dirs:
    test_d_url = target_url.rstrip('/') + '/' + d
    try:
        d_res = requests.head(test_d_url, timeout=3)
        if d_res.status_code < 400:
            found_dirs.append(test_d_url)
    except:
        pass

# 5. توليد وتشفير تجريبي (Hash Generator Demo)
sample_text = "AbuSamra_Security_2026"
md5_hash = hashlib.md5(sample_text.encode()).hexdigest()
sha256_hash = hashlib.sha256(sample_text.encode()).hexdigest()

# كتابة التقرير الشامل
with open(filename, "w", encoding="utf-8") as f:
    f.write("=" * 65 + "\n")
    f.write(f"     التقرير الأمني الشامل للكتيبة - إعداد البطل: أبو سمرة      \n")
    f.write(f"     وقت التنفيذ: {start_time}\n")
    f.write("=" * 65 + "\n\n")
    
    f.write(f"1. Target Info:\n- URL: {target_url}\n- IP: {target_ip}\n- Title: {title}\n\n")
    
    f.write(f"2. Security Headers Analysis:\n")
    for k, v in security_headers.items():
        f.write(f"- {k}: {v}\n")
    f.write("\n")
    
    f.write(f"3. Open Ports:\n- {open_ports}\n\n")
    
    f.write(f"4. Discovered Paths/Files:\n")
    if found_dirs:
        for fd in found_dirs:
            f.write(f"- Found: {fd}\n")
    else:
        f.write("- No sensitive paths exposed on root level.\n")
    f.write("\n")
    
    f.write(f"5. Cryptography & Hashing Demo:\n- Sample: {sample_text}\n- MD5: {md5_hash}\n- SHA256: {sha256_hash}\n\n")
    
    f.write(f"6. Harvested Links ({len(links)}):\n")
    for link in links:
        f.write(f"-> {link}\n")

print(f"\n[+] يا عيني يا فنان! تم تجميع الكتيبة وحفظ التقرير الأسطوري في ملف: {filename}")
print("[+] مبروك عليك الشغل العالي البرتغالي العابر للحدود يا أبو سمرة!")

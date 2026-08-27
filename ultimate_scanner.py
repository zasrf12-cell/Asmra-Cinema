import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import socket
import datetime

print("==================================================")
print("  🔥 أداة أبو سمرة الخارقة: الفحص الأمني الشامل 🔥  ")
print("==================================================\n")

target_url = "https://python.org"
parsed_url = urlparse(target_url)
domain = parsed_url.netloc

print(f"[*] جاري بدء العمليات الشاملة على الهدف: {target_url}\n")
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 1. مرحلة جمع الروابط
try:
    response = requests.get(target_url, timeout=10)
    if response.status_code == 200:
        print("[+] تم الاستطلاع بنجاح وتجاوز الجدران!")
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "بدون عنوان"
        
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.add(href)
            elif href.startswith('/'):
                links.add(target_url.rstrip('/') + href)
                
        print(f"[-] تم اصطياد عدد {len(links)} رابط برمجي.")
    else:
        print("[-] فشل الاتصال بالهدف الرئيسي.")
        links = set()
        title = "فشل الاتصال"
except Exception as e:
    print(f"[-] حدث خطأ في سحب الروابط: {e}")
    links = set()
    title = "خطأ"

# 2. مرحلة فحص المنافذ الحساسة للسيرفر
print("\n[*] جاري تنفيذ فحص المنافذ الحساسة (Port Scanning)...")
ports_to_check = [80, 443, 8080, 22]
open_ports = []

try:
    target_ip = socket.gethostbyname(domain)
    for port in ports_to_check:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            res = s.connect_ex((target_ip, port))
            if res == 0:
                open_ports.append(port)
                print(f" [🔓 مفتوح] منفذ رقم {port}")
            else:
                print(f" [🔒 مغلق] منفذ رقم {port}")
            s.close()
        except:
            pass
except:
    target_ip = "غير معروف"

# 3. كتابة التقرير الفخم
filename = "ultimate_report.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write(f"      التقرير الأمني الشامل - إعداد البطل: أبو سمرة      \n")
    f.write(f"      وقت التنفيذ: {start_time}\n")
    f.write("=" * 60 + "\n\n")
    
    f.write(f"[Target Information]\n")
    f.write(f"URL: {target_url}\n")
    f.write(f"IP Address: {target_ip}\n")
    f.write(f"Title: {title}\n\n")
    
    f.write(f"[Port Scan Results]\n")
    f.write(f"Open Ports Found: {open_ports if open_ports else 'None'}\n\n")
    
    f.write(f"[Harvested Links ({len(links)})]\n")
    for link in links:
        f.write(f"-> {link}\n")

print(f"\n[+] يا عيني يا فنان! تم حفظ التقرير الأسطوري كامل في ملف: {filename}")
print("[+] مبروك عليك إنجاز الشغل العالي البرتغالي يا أبو سمرة!")

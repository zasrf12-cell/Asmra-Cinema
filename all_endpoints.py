import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

print("==================================================")
print("  🔥 أداة كشف كل النوافذ والروابط الشاملة يا أبو سمرة 🔥 ")
print("==================================================\n")

target_url = "https://python.org"
print(f"[*] جاري استخراج كل النوافذ من الهدف: {target_url} ...\n")

try:
    res = requests.get(target_url, timeout=10)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        links = set()
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.add(href)
            elif href.startswith('/'):
                links.add(target_url.rstrip('/') + href)
                
        print(f"[+] تم العثور على عدد ({len(links)}) نافذة ورابط نشط!\n")
        print("--------------------------------------------------")
        
        # طباعة كل رابط ونافذة بالتفصيل
        for i, link in enumerate(sorted(links), 1):
            print(f"[{i}] -> {link}")
            
        print("--------------------------------------------------")
        print("[+] تم الانتهاء من استعراض كافة النوافذ بنجاح يا فنان!")
    else:
        print(f"[-] فشل الاتصال، كود الاستجابة: {res.status_code}")
except Exception as e:
    print(f"[-] حدث خطأ: {e}")

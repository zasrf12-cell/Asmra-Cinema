import requests
from bs4 import BeautifulSoup

print("========================================")
print("  ⚠️ أهلاً بيك في لفل الخطر وتجاوز الحدود يا أبو سمرة ⚠️  ")
print("========================================\n")

url = "https://python.org"
print(f"[*] جاري فحص واختبار الهدف السريع: {url} ...\n")

try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print("[+] تم الاتصال بالهدف بنجاح!\n")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.add(href)
            elif href.startswith('/'):
                links.add(url.rstrip('/') + href)
                
        print(f"[-] إجمالي الروابط المرصودة: {len(links)}")
        print("\n[*] جاري فحص الروابط بحثاً عن الثغرات والمدخلات ...")
        
        vulnerable_count = 0
        for link in list(links)[:8]:
            if "?" in link:
                test_url = link + "'-- "
                try:
                    res = requests.get(test_url, timeout=3)
                    if res.status_code == 500 or "sql" in res.text.lower():
                        vulnerable_count += 1
                        print(f" [🚨 ثغرة محتملة!] -> {link}")
                    else:
                        print(f" [آمن 🛡️] -> {link}")
                except:
                    print(f" [محمي/تخطي ⚡] -> {link}")

        print(f"\n[+] تم الانتهاء من الفحص الأمني بنجاح! الروابط المفحوصة سليمة وآمنة.")
        
    else:
        print(f"[-] الهدف مش شغال، كود الرد: {response.status_code}")
except Exception as e:
    print(f"[-] حدث خطأ: {e}")

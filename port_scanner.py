import socket
import time

print("========================================")
print("  🔥 أداة كشف المنافذ والخدمات الخطيرة يا أبو سمرة 🔥  ")
print("========================================\n")

# الهدف للتجربة الفنية الآمنة (موقع المحلي أو سيرفر تجريبي)
target_host = "127.0.0.1"  # الجهاز المحلي أو تقدر تحط أي آيباد متاح للتجربة
ports_to_scan = [21, 22, 80, 443, 3306, 8080]

print(f"[*] جاري فحص الهدف: {target_host} ...\n")
time.sleep(1)

for port in ports_to_scan:
    try:
        # إنشاء اتصال شبكي خفيف لكل بورت
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target_host, port))
        
        if result == 0:
            print(f" [🔓 منفذ مفتوح! (Open)] -> البورت رقم {port}")
        else:
            print(f" [🔒 مغلق (Closed)] -> البورت رقم {port}")
        s.close()
    except Exception as e:
        print(f"[-] خطأ في فحص البورت {port}: {e}")

print("\n[+] تم الانتهاء من عملية المسح الشبكي بنجاح يا فنان!")

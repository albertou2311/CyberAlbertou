# modules/auth.py (iyileştirilmiş)

import logging

AUTHORIZED_USERS = {
    "albertou": "Gok19Ay77"
}

def login():
    print("=== CyberAlbertou Giriş Ekranı ===")
    try:
        username = input("Kullanıcı adı: ").strip()
        password = input("Şifre: ").strip()

        if username in AUTHORIZED_USERS and AUTHORIZED_USERS[username] == password:
            print(f"[✓] Hoş geldin, {username}. Erişim verildi.")
            return True
        else:
            print("[✗] Hatalı kullanıcı adı veya şifre! Program sonlandırılıyor.")
            logging.warning(f"Başarısız giriş denemesi: {username}")
            return False
    except Exception as e:
        logging.error(f"Giriş sırasında hata oluştu: {e}")
        return False

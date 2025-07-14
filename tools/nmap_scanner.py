# tools/nmap_scanner.py

import socket
import subprocess
import re

def run_scan(ip_or_domain):
    print(f"[🌐] Nmap taraması başlatılıyor: {ip_or_domain}")
    try:
        # Domain ise IP'ye çevir
        try:
            ip = socket.gethostbyname(ip_or_domain)
        except:
            ip = ip_or_domain

        result = subprocess.run(["nmap", "-Pn", "-T4", "-sV", "--host-timeout", "60s", ip], capture_output=True, text=True)
        print(result.stdout)
        ports = re.findall(r"(\d+)/tcp\s+open", result.stdout)
        return list(map(int, ports))
    except Exception as e:
        print(f"[x] Hata: {e}")
        return []


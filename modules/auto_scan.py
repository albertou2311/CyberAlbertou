# modules/auto_scan.py

import modules.scanner as scanner
import modules.bruteforce_ssh as bf_ssh
import tools.nmap_scanner as nmap_tool
from modules.utils.logger import log_info, log_warning

def auto_scan(urls, ips, ssh_targets):
    """
    Otomatik zafiyet, port ve brute force taraması yapar.
    urls: Test edilecek URL listesi (parametreli)
    ips: Nmap taraması için IP listesi
    ssh_targets: Bruteforce için hedef IP listesi
    """
    log_info("=== Otomatik Tetikleme Başladı ===")

    # URL zafiyet taraması
    for url in urls:
        log_info(f"Zafiyet taraması için URL: {url}")
        result = scanner.scan(url)
        if result:
            log_warning(f"Zafiyet bulundu! URL: {url}")
        else:
            log_info(f"Zafiyet bulunamadı: {url}")

    # IP port taraması
    for ip in ips:
        log_info(f"Nmap port taraması için IP: {ip}")
        open_ports = nmap_tool.run_scan(ip)
        if open_ports:
            log_warning(f"Açık portlar bulundu: {ip} -> {open_ports}")
        else:
            log_info(f"Açık port bulunamadı: {ip}")

    # SSH Bruteforce saldırısı
    for target in ssh_targets:
        log_info(f"SSH brute force başlatılıyor: {target}")
        bf_ssh.start_bruteforce(target)

    log_info("=== Otomatik Tetikleme Tamamlandı ===")


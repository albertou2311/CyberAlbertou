# modules/osint.py

import requests
import socket
import whois
from modules import scanner, analyzer


def get_domain_info(domain):
    try:
        socket.inet_aton(domain)  # IP ise whois alma
        print("[-] IP adresi için domain bilgisi alınamaz.")
        return
    except socket.error:
        pass  # IP değilse domain olabilir

    try:
        w = whois.whois(domain)
        print("[+] Domain bilgisi:")
        print(f"  - Registrar: {w.registrar}")
        print(f"  - Oluşturulma tarihi: {w.creation_date}")
        print(f"  - Son güncelleme: {w.updated_date}")
    except Exception as e:
        print(f"[-] Domain bilgisi alınamadı: {e}")


def get_ip_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        print(f"[+] IP Lokasyon: {data.get('country')}, {data.get('city')} ({data.get('isp')})")
    except Exception as e:
        print(f"[-] IP lokasyon bilgisi alınamadı: {e}")


def run_osint(target):
    print(f"\n=== OSINT Başlatılıyor: {target} ===")
    target = target.strip().strip("'").strip('"')  # Temizle

    # IP çözümleme
    try:
        socket.inet_aton(target)
        ip = target
    except socket.error:
        try:
            ip = socket.gethostbyname(target)
            print(f"[✓] {target} IP adresi: {ip}")
        except Exception as e:
            print(f"[-] IP çözümlenemedi: {e}")
            ip = target

    get_domain_info(target)
    get_ip_location(ip)

    print("[*] Açık taraması başlatılıyor...")

    try:
        result = scanner.scan(f"http://{target}")
        if result:
            response_text = result[1] if isinstance(result, tuple) else None
            analyzer_inst = analyzer.Analyzer()
            if response_text:
                analyzer_inst.analyze_sql_response(response_text)
            analyzer_inst.show_recommendations()
        else:
            print("[-] Otomatik taramada sonuç çıkmadı.")
    except Exception as e:
        print(f"[ERROR] Scanner hatası: {e}")


def basic_osint_menu():
    print("=== OSINT Modülü Gelişmiş ===")
    target = input("Hedef domain veya IP girin: ").strip()
    run_osint(target)

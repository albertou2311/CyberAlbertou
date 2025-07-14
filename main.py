from tools import nmap_scanner
from modules import scanner, bruteforce_ssh, analyzer
import modules.bot as bot_mod
import tools.nmap_scanner as nmap_tool
import modules.analyzer as analyzer_mod
import modules.bruteforce_ssh as bf_ssh
import modules.scanner as scanner
import modules.osint as osint
from modules import auth
import modules.exploiter as exploiter
import modules.auto_scan as auto_scanx
import modules.param_detector as param_detector
import modules.another_tool as another_tool


def main():
    if not auth.login():
        exit()

    analyzer = analyzer_mod.Analyzer()

    print("=== CyberAlbertou Siber Güvenlik Asistanı ===")
    while True:
        print("\n1. OSINT Bilgi Topla  # Hedef hakkında açık kaynak verileri toplar")
        print("2. Zafiyet Taraması (SQLi, XSS, LFI)  # Parametreli URL'lerde güvenlik açıklarını tarar")
        print("3. Bruteforce Atağı (SSH, FTP, HTTP)  # SSH şifre kırma saldırısı başlatır")
        print("4. Nmap Port & Servis Taraması  # IP adresinde açık port ve servisleri keşfeder")
        print("5. Ağ Haritalama & Cihaz Keşfi  # Geliştirilecek (yakında)")
        print("6. DDoS Simülasyonu (Eğitim Amaçlı)  # Geliştirilecek (yakında)")
        print("7. Raporlama  # Geliştirilecek (yakında)")
        print("8. Bot Yönetimi (Arka Kapı, Komut Kontrol)  # Botları yönetmeyi sağlar")
        print("9. Otomatik Exploit Tespiti (Searchsploit ile)  # Hedef sistemdeki zafiyetler için exploit arar")
        print("10. Otomatik Tetikleme (URL, IP ve SSH Brute Force)  # Kullanıcıdan alınan dosyalarla tüm modülleri sırayla tetikler")
        print("11. Tümünü Otomatik Tara (Giriş Gerektirmez, Varsayılan dosyalar)  # Her şeyi otomatik yapar ve raporlar")
        print("12. [ Kaldırıldı ] Armitage ")
        print("13. URL'den Parametreleri Otomatik Bul ve Tara")
        print("14. Başka Pentest Aracı")
        print("15. Çıkış")

        choice = input("Seçiminiz: ").strip()

        if choice == "1":
            osint.basic_osint_menu()

        elif choice == "2":
            url = input("Test edilecek URL (parametreli): ").strip()
            if '?' not in url:
                print("[-] Lütfen parametreli bir URL giriniz! Örn: https://site.com/page.php?id=1")
                continue
            resp = scanner.scan(url)
            if resp:
                analyzer.analyze_sql_response(resp)
                analyzer.show_recommendations()
            else:
                print("[-] Tarama sonuçsuz kaldı.")

        elif choice == "3":
            target = input("Hedef IP adresi (SSH için): ").strip()
            bf_ssh.start_bruteforce(target)

        elif choice == "4":
            ip = input("Tarama yapılacak IP: ").strip()
            open_ports = nmap_tool.run_scan(ip)
            if open_ports:
                analyzer.analyze_ports(open_ports)
                analyzer.show_recommendations()
            else:
                print("[-] Açık port bulunamadı veya hedef erişilemiyor.")

        elif choice == "5":
            print("[*] Ağ Haritalama modülü yakında eklenecek.")

        elif choice == "6":
            print("[*] DDoS simülasyonu modülü yakında eklenecek.")

        elif choice == "7":
            print("[*] Raporlama modülü yakında eklenecek.")

        elif choice == "8":
            bot_mod.bot_management()

        elif choice == "9":
            target = input("Hedef IP veya domain girin: ").strip()
            exploiter.run(target)

        elif choice == "10":
            url_file = input("Test edilecek URL listesi dosyası: ").strip()
            ip_file = input("Nmap taraması için IP listesi dosyası: ").strip()
            ssh_file = input("SSH brute force hedef IP listesi dosyası: ").strip()

            try:
                with open(url_file, "r") as uf:
                    urls = [u.strip() for u in uf.readlines() if u.strip()]
                with open(ip_file, "r") as ipf:
                    ips = [i.strip() for i in ipf.readlines() if i.strip()]
                with open(ssh_file, "r") as sf:
                    ssh_targets = [s.strip() for s in sf.readlines() if s.strip()]
            except Exception as e:
                print(f"Dosya okuma hatası: {e}")
                continue

            auto_scan.auto_scan(urls, ips, ssh_targets)

        elif choice == "11":
            try:
                print("[*] Varsayılan dosyalar yükleniyor...")
                with open("data/urls.txt") as f:
                    urls = [x.strip() for x in f if x.strip()]
                with open("data/ips.txt") as f:
                    ips = [x.strip() for x in f if x.strip()]
                with open("data/ssh_targets.txt") as f:
                    ssh_targets = [x.strip() for x in f if x.strip()]
            except Exception as e:
                print(f"[!] Dosya hatası: {e}")
                continue

            print("[*] OSINT başlatılıyor...")
            for u in urls:
                osint.run_osint(u)

            print("[*] Zafiyet taraması başlatılıyor...")
            for url in urls:
                resp = scanner.scan(url)
                if resp:
                    analyzer.analyze_sql_response(resp)

            print("[*] SSH brute force başlatılıyor...")
            for ip in ssh_targets:
                bf_ssh.start_bruteforce(ip)

            print("[*] Nmap taraması başlatılıyor...")
            for ip in ips:
                open_ports = nmap_tool.run_scan(ip)
                analyzer.analyze_ports(open_ports)

            print("[✓] Tüm işlemler tamamlandı. Raporlar 'reports/' klasörüne kaydedildi.")

        elif choice == "12":
            print("[!]  Bu seçenek CyberAlbertou'da yok . Armitage'yi ayrı başlatın.") 

        elif choice == "13":
            target_url = input("Tarama için URL girin: ").strip()
            params = param_detector.detect_params(target_url)
            if not params:
                print("[-] URL'de parametre bulunamadı.")
            else:
                print(f"[+] Bulunan parametreler: {params}")
                for param in params:
                    full_url = f"{target_url}?{param}=test"
                    print(f"Tarama yapılıyor: {full_url}")
                    resp = scanner.scan(full_url)
                    if resp:
                        print("[✓] Zafiyet bulunabilir.")
                    else:
                        print("[-] Zafiyet bulunamadı.")

        elif choice == "14":
            print("[*] Başka pentest aracı çalıştırılıyor...")
            another_tool.run()

        elif choice == "15":
            print("Çıkış yapılıyor, görüşürüz!")
            break

        else:
            print("Geçersiz seçim, tekrar deneyin.")


if __name__ == "__main__":
    main()

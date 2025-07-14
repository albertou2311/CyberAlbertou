# modules/analyzer.py

class Analyzer:
    def __init__(self):
        self.recommendations = []

    def analyze_sql_response(self, response):
        if "mysql" in response.lower():
            self.recommendations.append("SQL Injection tespit edildi. sqlmap ile detaylı test önerilir.")
        if "<script>" in response.lower():
            self.recommendations.append("XSS açığı mevcut olabilir. Tarayıcı davranışı izlenmeli.")

    def analyze_ports(self, open_ports):
        if 22 in open_ports:
            self.recommendations.append("SSH portu açık. Brute force denenebilir.")
        if 80 in open_ports or 443 in open_ports:
            self.recommendations.append("HTTP/HTTPS servisi açık. Web uygulaması zafiyetleri araştırılabilir.")
        if 3306 in open_ports:
            self.recommendations.append("MySQL portu açık. Erişim kontrolü kontrol edilmeli.")

    def show_recommendations(self):
        print("\n[🧠] Öneriler:")
        if not self.recommendations:
            print("– Şu anlık öneri yok.")
        for r in self.recommendations:
            print(f"➤ {r}")

def analyze_ssh_bruteforce(result):
    if result is None:
        print("[!] SSH brute-force başarısız.")

def suggest_manual_commands_for_ssh(ip):
    print("\n[📌] SSH sonrası komut önerileri:")
    print(f"  – whoami")
    print(f"  – uname -a")
    print(f"  – netstat -tulnp")
    print(f"  – ls -la /home/")

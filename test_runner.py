# test_runner.py

import os
import traceback
from datetime import datetime
from modules import bruteforce_ssh, scanner, exploit, ai_suggestions
import asyncio

LOG_FILE = "logs/test_results.log"
os.makedirs("logs", exist_ok=True)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def run_all_tests():
    log("🚀 Tüm modül testleri başlatılıyor...\n")

    # 1. SSH Brute Force
    try:
        log("📡 1. SSH Brute Force Testi Başlatılıyor...")
        bruteforce_ssh.start_bruteforce()  # test IP
        brute_result = "SSH brute-force sonucu loglandı."
    except Exception as e:
        brute_result = f"SSH Testi başarısız: {e}"
        log(f"[HATA - SSH] {traceback.format_exc()}")

    # 2. Zafiyet Tarayıcısı
    try:
        log("\n🔎 2. Zafiyet Tarayıcısı Çalışıyor...")
        scan_result = asyncio.run(scanner.scan("http://testphp.vulnweb.com/listproducts.php?cat=1"))
        log(f"[+] Tarama tamamlandı. Sonuç: {scan_result}")
    except Exception as e:
        scan_result = f"Taramada hata: {e}"
        log(f"[HATA - Tarayıcı] {traceback.format_exc()}")

    # 3. Exploit Testi
    try:
        log("\n💥 3. Exploit Testi Çalışıyor...")
        exploit_result = exploit.run_exploits("testphp.vulnweb.com")
        log(f"[+] Exploit Sonuç: {exploit_result}")
    except Exception as e:
        exploit_result = f"Exploit hatası: {e}"
        log(f"[HATA - Exploit] {traceback.format_exc()}")

    # 4. AI Analizi
    try:
        log("\n🤖 4. AI Önerileri Üretiliyor...")
        ai_suggestions.run_ai_analysis(
            scan_results=str(scan_result),
            brute_result=str(brute_result),
            exploit_result=str(exploit_result)
        )
        log("[✓] AI analizi başarıyla tamamlandı.")
    except Exception as e:
        log(f"[HATA - AI] AI analizi hatası: {e}\n{traceback.format_exc()}")

    log("\n✅ Testler tamamlandı.")

if __name__ == "__main__":
    run_all_tests()

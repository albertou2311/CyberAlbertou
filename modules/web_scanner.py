# modules/web_scanner.py

import requests

def scan_vulnerabilities(target):
    print("[🌐] Web zafiyet taraması yapılıyor...")
    results = []

    urls = [
        f"http://{target}/",
        f"http://{target}/index.php",
        f"http://{target}/login.php",
        f"http://{target}/admin/",
    ]

    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            if "sql" in r.text.lower():
                results.append(f"Potansiyel SQL Injection: {url}")
            if "<script>" in r.text.lower():
                results.append(f"Potansiyel XSS açığı: {url}")
        except Exception:
            continue

    if not results:
        results.append("Zafiyet bulunamadı.")
    return results

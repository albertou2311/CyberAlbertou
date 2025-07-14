# tools/whois_lookup.py

import subprocess

def get_whois_info(target):
    try:
        result = subprocess.run(["whois", target], capture_output=True, text=True, timeout=10)
        return result.stdout
    except Exception as e:
        return f"Hata: {e}"

# tools/subdomain_finder.py

import requests

common_subdomains = [
    "www", "mail", "ftp", "test", "dev", "admin", "portal", "webmail", "smtp", "secure"
]

def find_subdomains(target):
    found = []
    for sub in common_subdomains:
        url = f"http://{sub}.{target}"
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                found.append(f"{sub}.{target}")
        except Exception:
            continue
    return found


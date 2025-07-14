from urllib.parse import urlparse, parse_qs

def detect_params(url):
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        return list(query.keys())
    except Exception as e:
        print(f"[!] Parametre algılama hatası: {e}")
        return []

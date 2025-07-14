import os
import re

USERNAME_FILE = "data/username.txt"
PASSWORD_FILE = "data/password.txt"

def clean_line(line):
    # Gereksiz boşlukları kaldır, küçük harfe çevir
    return line.strip().lower()

def add_to_file(filename, new_entries):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass

    with open(filename, 'r', encoding='utf-8') as f:
        existing = set([clean_line(line) for line in f if line.strip()])

    with open(filename, 'a', encoding='utf-8') as f:
        added_count = 0
        for entry in new_entries:
            entry_clean = clean_line(entry)
            if entry_clean and entry_clean not in existing:
                f.write(entry_clean + '\n')
                existing.add(entry_clean)
                added_count += 1
    return added_count

def extract_usernames(text):
    usernames = set()
    # Basit regex ile email adreslerini bul
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    for email in emails:
        local_part = email.split('@')[0]
        usernames.add(local_part)

    # Ayrıca basit isim soyisim ve olası kullanıcı adı kalıplarını çıkar
    # Örnek: "John Doe" gibi isimleri bulabilirsek username oluşturabiliriz
    # Burada örnek olarak basit isim soyisim regex eklenebilir
    # İstersen buraya özel patternler ekleyebiliriz

    return list(usernames)

def extract_passwords(text):
    passwords = set()
    # Basit örnek: belli kalıplar (şifre, password, pass: gibi kelimeler etrafındaki stringleri yakala)
    # Örnek: "password: 123456"
    found = re.findall(r'password[:=]\s*([^\s\'",]+)', text, re.I)
    for pw in found:
        passwords.add(pw)

    # Ayrıca şifre gibi görünen rastgele dizileri alabiliriz (opsiyonel)

    return list(passwords)


def update_wordlists_from_text(text):
    usernames = extract_usernames(text)
    passwords = extract_passwords(text)

    added_usernames = add_to_file(USERNAME_FILE, usernames)
    added_passwords = add_to_file(PASSWORD_FILE, passwords)

    print(f"[+] {added_usernames} yeni kullanıcı adı eklendi.")
    print(f"[+] {added_passwords} yeni parola eklendi.")

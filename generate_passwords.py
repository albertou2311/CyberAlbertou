# ~/CyberAlbertou/generate_passwords.py

import itertools
import random
import os

# Kaynak veriler
names = ["albertou", "yildirim", "admin", "root", "cyber", "test"]
years = ["2023", "2024", "2025"]
specials = ["!", "@", "#", "$", "%", "&", "*"]
keywords = ["pass", "login", "secure", "access", "user", "pw"]

# AI destekli varyasyonlar
base_words = names + keywords

# Kullanıcı adları için varyasyonlar
usernames = set()
for name in base_words:
    usernames.add(name)
    usernames.add(name.capitalize())
    usernames.add(name + "01")
    usernames.add(name + "_admin")

# Şifreler için varyasyonlar
passwords = set()
for name in base_words:
    for year in years:
        for special in specials:
            passwords.add(name + year)
            passwords.add(name + special)
            passwords.add(name + year + special)
            passwords.add(name.capitalize() + special + year)

# Rockyou tarzı ekler (örnekler)
popular = ["123456", "password", "qwerty", "letmein", "welcome"]
for p in popular:
    passwords.add(p)
    for s in specials:
        passwords.add(p + s)

# Yinelenenleri temizle
usernames = sorted(list(usernames))
passwords = sorted(list(passwords))

# Wordlists klasörü yoksa oluştur
os.makedirs("wordlists", exist_ok=True)

# Yaz
with open("wordlists/usernames.txt", "w") as u:
    u.write("\n".join(usernames))
with open("wordlists/passwords.txt", "w") as p:
    p.write("\n".join(passwords))

print(f"[✓] {len(usernames)} kullanıcı adı, {len(passwords)} şifre üretildi.")
print("[→] Kayıt: wordlists/usernames.txt & wordlists/passwords.txt")

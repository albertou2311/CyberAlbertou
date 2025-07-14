# tools/wordlist_generator_v2.py

import argparse
import os
import random
import string
from datetime import datetime

# Karakter setleri
SPECIAL_CHARS = "!@#$%^&*()-_=+.,?/"

# Basit kombinasyonlar
def generate_basic_words(name, surname, birth, company):
    combos = [
        name, surname, f"{name}{surname}", f"{surname}{name}",
        f"{name}_{surname}", f"{surname}_{name}",
        f"{name}.{surname}", f"{surname}.{name}",
        f"{name}{birth}", f"{surname}{birth}", f"{name}{surname}{birth}",
        f"{name}{company}", f"{surname}{company}",
        f"{company}{birth}", f"{name}{company}{birth}",
        name[:1] + surname, name + surname[:1],
        name + str(datetime.now().year), surname + str(datetime.now().year)
    ]
    return list(set(combos))

# Şifre kombinasyonları

def generate_passwords(basic_words, count=1000):
    passwords = set()
    for word in basic_words:
        for _ in range(3):
            pw = word
            pw += random.choice(string.digits)
            pw += random.choice(SPECIAL_CHARS)
            pw += random.choice(string.ascii_letters)
            passwords.add(pw)

    while len(passwords) < count:
        rand_pw = ''.join(random.choices(string.ascii_letters + string.digits + SPECIAL_CHARS, k=random.randint(8, 14)))
        passwords.add(rand_pw)

    return list(passwords)

# Kaydet

def save_list(data, filename):
    with open(filename, 'w') as f:
        for item in data:
            f.write(item + '\n')
    print(f"[✓] Yazıldı: {filename} ({len(data)} satır)")

# Ana fonksiyon

def main():
    parser = argparse.ArgumentParser(description="🔐 Gelişmiş Username ve Password Üretici")
    parser.add_argument('--name', required=True)
    parser.add_argument('--surname', required=True)
    parser.add_argument('--birth', required=True)
    parser.add_argument('--company', required=True)
    parser.add_argument('--count', type=int, default=1000, help="Şifre sayısı")
    args = parser.parse_args()

    os.makedirs("lists", exist_ok=True)

    basic = generate_basic_words(args.name, args.surname, args.birth, args.company)
    passwords = generate_passwords(basic, args.count)

    save_list(basic, "lists/advanced_usernames.txt")
    save_list(passwords, "lists/advanced_passwords.txt")

if __name__ == "__main__":
    main()

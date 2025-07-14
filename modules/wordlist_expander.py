import os
import random
import string
from datetime import datetime

SPECIAL_CHARS = "!@#$%^&*()-_=+.,?/"

def load_wordlist(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_list(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        for item in data:
            f.write(item + "\n")
    print(f"[✓] Yazıldı: {filename} ({len(data)} satır)")

def generate_basic_combinations(names, surnames, births, companies):
    combos = set()
    for name in names:
        for surname in surnames:
            for birth in births:
                for company in companies:
                    combos.update([
                        name, surname,
                        f"{name}{surname}", f"{surname}{name}",
                        f"{name}_{surname}", f"{surname}_{name}",
                        f"{name}.{surname}", f"{surname}.{name}",
                        f"{name}{birth}", f"{surname}{birth}",
                        f"{name}{surname}{birth}",
                        f"{name}{company}", f"{surname}{company}",
                        f"{company}{birth}", f"{name}{company}{birth}",
                        name[:1] + surname,
                        name + surname[:1],
                        name + str(datetime.now().year),
                        surname + str(datetime.now().year)
                    ])
    return list(combos)

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

def expand_wordlists_from_data():
    usernames = load_wordlist("data/username.txt")
    passwords = load_wordlist("data/password.txt")
    emails = load_wordlist("data/emails.txt")

    # Örnek olarak email domainlerinden şirket ismi çıkarmaya çalış
    companies = []
    for email in emails:
        parts = email.split("@")
        if len(parts) == 2:
            domain = parts[1].split(".")[0]
            if domain and domain not in companies:
                companies.append(domain)

    # Basit doğum yılı tahmini olarak '1990' varsayabilir veya boş liste bırakabiliriz
    # Eğer doğum yılı verileri varsa onlar da alınabilir.
    births = ["1990", "1991", "1992", "2000"]

    combos = generate_basic_combinations(usernames, usernames, births, companies)
    passwords_expanded = generate_passwords(combos, count=2000)

    save_list(list(set(combos)), "data/advanced_usernames.txt")
    save_list(passwords_expanded, "data/advanced_passwords.txt")

# tools/wordlist_generator.py

import argparse
from datetime import datetime

def generate_usernames(name, surname, birth, company):
    usernames = set()

    basics = [
        name, surname, name+surname, surname+name,
        f"{name}_{surname}", f"{surname}_{name}",
        f"{name}.{surname}", f"{surname}.{name}",
        name[:1] + surname, name + surname[:1],
        name + str(datetime.now().year),
        "admin", "sysadmin", "root"
    ]

    combos = [
        f"{name}{birth}", f"{surname}{birth}", f"{name}_{birth}",
        f"{surname}_{birth}", f"{name}{company}", f"{surname}{company}",
        f"{name}_{company}", f"{surname}_{company}",
        f"{name}{surname}{birth}", f"{surname}{name}{birth}",
        f"{name}{surname}_{company}", f"{company}{name}{birth}",
        f"{company}_{name}", f"{company}_{surname}"
    ]

    for item in basics + combos:
        usernames.add(item.lower())

    return list(usernames)

def generate_passwords(name, surname, birth, company):
    passwords = set()
    base = [name, surname, company, "admin", "root", "pass", "password"]

    for word in base:
        passwords.update([
            f"{word}{birth}",
            f"{birth}{word}",
            f"{word}{birth}!",
            f"{word}@123",
            f"{word}123",
            f"{word}1234",
            f"{word}321",
            f"{word.capitalize()}{birth}",
            f"{word.capitalize()}123",
            f"{word}2024", f"{word}2025",
            f"{word}@{birth}", f"{word}!{birth}",
            f"{word}007", f"{word}01", f"{word}02", f"{word}03"
        ])

    return list(passwords)

def write_to_file(filename, items):
    with open(filename, "w") as f:
        for item in sorted(items):
            f.write(item + "\n")
    print(f"[✓] Yazıldı: {filename} ({len(items)} satır)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--surname", required=True)
    parser.add_argument("--birth", required=True)
    parser.add_argument("--company", required=True)

    args = parser.parse_args()

    usernames = generate_usernames(args.name, args.surname, args.birth, args.company)
    passwords = generate_passwords(args.name, args.surname, args.birth, args.company)

    write_to_file("lists/custom_usernames.txt", usernames)
    write_to_file("lists/custom_passwords.txt", passwords)

if __name__ == "__main__":
    main()

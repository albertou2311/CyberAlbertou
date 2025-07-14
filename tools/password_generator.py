# tools/password_generator.py

import itertools

def generate_passwords():
    names = ["admin", "root", "albertou", "test"]
    years = ["123", "1234", "2024", "2025"]
    symbols = ["", "!", "@", "#"]
    extras = ["", "123", "321", "01", "pass", "pwd"]

    passwords = set()

    for name in names:
        for combo in itertools.product(years, symbols, extras):
            pw = name + ''.join(combo)
            passwords.add(pw)

    with open("lists/passwords.txt", "w") as f:
        for pw in sorted(passwords):
            f.write(pw + "\n")

    print(f"[✓] {len(passwords)} parola oluşturuldu → lists/passwords.txt")

if __name__ == "__main__":
    generate_passwords()

# tools/ai_suggestions.py

import random

common_usernames = [
    "admin", "root", "user", "test", "guest", "info", "sysadmin", "administrator",
    "support", "webmaster"
]

common_passwords = [
    "123456", "password", "admin123", "root", "1234", "test123", "passw0rd", "qwerty",
    "letmein", "welcome"
]

vulnerability_suggestions = [
    "SQL Injection",
    "Cross-Site Scripting (XSS)",
    "Remote Code Execution (RCE)",
    "Directory Traversal",
    "Insecure Deserialization",
    "Open Redirect",
]

def suggest_usernames():
    return random.sample(common_usernames, 5)

def suggest_passwords():
    return random.sample(common_passwords, 5)

def suggest_attacks(report):
    suggestions = []

    if report.get("open_ports"):
        suggestions.append("Port taraması sonucu açık portları hedefleyin.")

    if report.get("admin_login_result") is None:
        suggestions.append("Admin panel brute-force saldırısı deneyin.")

    suggestions += vulnerability_suggestions

    return suggestions

def generate_credentials():
    usernames = suggest_usernames()
    passwords = suggest_passwords()
    return list(zip(usernames, passwords))

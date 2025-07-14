# modules/utils/logger.py

import datetime
import os

from colorama import Fore, Style, init
init(autoreset=True)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "activity.log")

def write_log_to_file(level, message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{now}] [{level}] {message}\n")

def log_error(message, exception=None):
    msg = f"{message} → {str(exception)}" if exception else message
    print(Fore.RED + f"[ERROR] {msg}")
    write_log_to_file("ERROR", msg)

def log_info(message):
    print(Fore.BLUE + f"[INFO] {message}")
    write_log_to_file("INFO", message)

def log_success(message):
    print(Fore.GREEN + f"[OK] {message}")
    write_log_to_file("SUCCESS", message)

def log_warning(message):
    print(Fore.YELLOW + f"[WARN] {message}")
    write_log_to_file("WARNING", message)

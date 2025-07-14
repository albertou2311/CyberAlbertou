#!/usr/bin/env python3
import argparse
import sys
import os
import subprocess

# Modüller (modüller dosya yapına göre değişebilir)
from modules.bruteforce_ssh import start_bruteforce
from modules.scanner import scan as start_payload_scan
from modules.exploit import run_exploits
from modules.ai_suggestions import run_ai_analysis
from modules.updater import update_script  # Bu modül güncelleme için olmalı, eğer yoksa basit fonksiyon yaz

def main():
    parser = argparse.ArgumentParser(description="Albertou Otomatik Tarama Aracı")
    parser.add_argument("-t", "--target", required=True, help="Hedef IP veya URL")
    parser.add_argument("-b", "--bruteforce", action="store_true", help="SSH Brute-force modu")
    parser.add_argument("-p", "--payload", action="store_true", help="Payload (zafiyet) taraması")
    parser.add_argument("-e", "--exploit", action="store_true", help="Exploit modüllerini çalıştır")
    parser.add_argument("-a", "--ai", action="store_true", help="AI öneri ve analiz modülü (PRO mod)")
    parser.add_argument("-u", "--update", action="store_true", help="Script güncelleme modülü")
    parser.add_argument("-f", "--full", action="store_true", help="Tüm modülleri çalıştır (PRO mod ile AI dahil)")

    args = parser.parse_args()

    if args.update:
        print("[*] Güncelleme işlemi başlatılıyor...")
        update_script()
        sys.exit(0)

    if args.full:
        args.bruteforce = True
        args.payload = True
        args.exploit = True
        args.ai = True

    print(f"[*] Hedef: {args.target}")
    if args.bruteforce:
        print("[*] SSH Brute-force başlatılıyor...")
        start_bruteforce(args.target)

    if args.payload:
        print("[*] Payload taraması başlatılıyor...")
        # Payload modülün async olabilir, async çalıştırma örneği:
        import asyncio
        asyncio.run(start_payload_scan(args.target))

    if args.exploit:
        print("[*] Exploit modülleri çalıştırılıyor...")
        run_exploits(args.target)

    if args.ai:
        print("[*] AI analiz ve öneri modülü çalıştırılıyor...")
        run_ai_analysis(args.target)

if __name__ == "__main__":
    main()

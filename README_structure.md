# CyberAlbertou - Klasör ve Dosya Rehberi

## 📁 Ana Dosyalar
- `albertou_auto_scan.py` → Otomatik sızma testi başlatıcı.
- `main.py` → Ana kontrol dosyası. GUI veya CLI'den tetiklenebilir.
- `test_runner.py` → Tüm modüllerin otomatik testini yapar.
- `cyberalbertou.sh` → Linux shell script ile otomatik başlatıcı.

## 📁 modules/
CyberAlbertou'nun tüm iç modülleri burada:

- `bruteforce_ssh.py` → SSH brute-force saldırı modülü.
- `exploit.py` → Exploit uygulama ve test modülü.
- `scanner.py` → Hedef sistemde zafiyet tarayıcı.
- `ai_suggestions.py` → AI ile saldırı sonrası öneriler üretir.
- `analyzer.py` → Otomatik sonuç analiz modülü.
- `osint.py` → Hedef hakkında açık kaynak bilgi toplar.
- `param_detector.py` → Web parametreleri üzerinde analiz yapar.
- `auth.py` → Giriş sistemi, kimlik doğrulama.
- `updater.py` → Modül güncelleyici.
- `wordlist_expander.py` → Kelime listelerini genişletir.
- `bruteforce_utils.py` → Brute-force yardımcı araçlar.

## 📁 tools/
- `password_generator.py` → AI tabanlı parola üretici.
- `nmap_scanner.py` → Nmap çıktısını işleyen Python aracı.
- `php-revshell.php` → Geri bağlantı (reverse shell) için PHP shell dosyası.
- `listener.sh` → Geri bağlantı beklemek için dinleyici scripti.
- `wordlist_generator.py` → Wordlist üretici (v1).
- `wordlist_generator_v2.py` → Daha gelişmiş wordlist üretici.
- `wordlist_updater.py` → Wordlist güncelleme aracı.

## 📁 data/
- `ssh_targets.txt` → Brute-force için IP adresleri.
- `ips.txt` → Taranacak IP listesi.
- `urls.txt` → Tarama yapılacak URL listesi.

## 📁 loot/
Hedef sistemlerden elde edilen veriler:

- `hedefsite.com/` → Her hedef için klasör açılır.
  - `nmap.txt`, `dns.txt`, `waf.txt`, `whois.txt`, vs...

## 📁 wordlists/
Önceden hazırlanmış kelime listeleri:

- `usernames.txt` → Kullanıcı adları listesi.
- `passwords.txt` → Parolalar.
- `users.txt` → Hedef sistemde kullanılabilecek kullanıcı adları.
- `payloads.txt` → Exploit denemeleri için payloadlar.

## 📁 logs/
- `activity.log` → Tüm oturumların günlük kaydı (otomatik yazılır).

## 📁 scripts/
- `tetikle.py` → Başka bir scripti tetiklemek için kullanılır.

## 📁 venv/
Python sanal ortamı.

---

> 💡 **Not:** Her dosyanın içindeki kritik fonksiyonlara da docstring yorumları ekleyerek geliştiricilerin daha rahat anlamasını sağlayabiliriz.

---

## ✅ 3. Sonraki Adımlar:

🔁 **Yapılacaklar sırası:**
1. `bruteforce_ssh.py` içindeki fonksiyonu kontrol et ve `run_brute_force()` olarak düzenle.
2. Tekrar `python3 test_runner.py` komutunu çalıştır.
3. Yeni çıktıları buraya yapıştır.
4. Ardından sana test sonuçlarını **log dosyasına** yazan sistemi kuralım.
5. GUI ve raporlama sistemini ekleyerek ilerleriz.

Hazırsan tekrar test edip gönder, devam edelim! 💪

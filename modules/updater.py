def update_script():
    import subprocess
    try:
        print("[*] Git repository güncelleniyor...")
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            print("[✓] Güncelleme başarılı.")
        else:
            print("[X] Güncelleme başarısız.")
    except Exception as e:
        print(f"[X] Güncelleme sırasında hata: {e}")

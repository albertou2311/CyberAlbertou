# modules/ai_suggestions.py

def run_ai_analysis(scan_results=None, brute_result=None, exploit_result=None):
    print("\n[🤖] Yapay Zeka Asistan Önerisi:")

    suggestions = []

    if scan_results:
        if "open" in scan_results.lower():
            suggestions.append("– Açık portlar bulundu. Versiyon bilgisi alınarak zafiyet araştırılabilir.")
        if "filtered" in scan_results.lower():
            suggestions.append("– Tüm portlar filtrelenmiş görünüyor. Güvenlik duvarı veya IDS olabilir.")
    
    if brute_result:
        if "başarısız" in brute_result.lower():
            suggestions.append("– Brute force denemeleri başarısız. Parola listesi güncellenebilir veya başka yöntem denenebilir.")
        if "başarılı" in brute_result.lower():
            suggestions.append("– Brute-force başarılı! Erişim test edilebilir.")
    
    if exploit_result:
        if "XSS" in exploit_result:
            suggestions.append("– XSS açığı bulundu. Cookie çalma, redirect gibi saldırılar denenebilir.")
        if "SQL" in exploit_result:
            suggestions.append("– SQL Injection açığı bulundu. Dump denenebilir.")
        if "LFI" in exploit_result:
            suggestions.append("– LFI açığı bulundu. /etc/passwd ve log poisoning gibi teknikler uygulanabilir.")
    
    if not suggestions:
        print("– Şu anlık özel öneri bulunamadı.")
    else:
        for s in suggestions:
            print(s)

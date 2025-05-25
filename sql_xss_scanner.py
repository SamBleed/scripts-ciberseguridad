import requests

url = input("Ingresa la URL para probar (ej: http://example.com/page.php?id=1): ")

# Payloads simples
payloads = ["'", "\"", "<script>alert('XSS')</script>", "' OR '1'='1"]

for p in payloads:
    test_url = url + p
    try:
        r = requests.get(test_url, timeout=5)
        if "sql" in r.text.lower() or "syntax" in r.text.lower():
            print(f"[!] Posible vulnerabilidad SQLi detectada con payload: {p}")
        elif "<script>alert('xss')</script>" in r.text.lower():
            print(f"[!] Posible vulnerabilidad XSS detectada con payload: {p}")
    except requests.exceptions.RequestException:
        print("[!] Error al conectar")

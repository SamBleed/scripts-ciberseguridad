import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"[+] Puerto {port} abierto")
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass


def main():
    print("#" * 50)
    print("  Escáner simple de puertos | by SamBleed")
    print("#" * 50)

    target = input("\nIngresa la dirección IP a escanear: ").strip()

    try:
        socket.inet_aton(target)
    except socket.error:
        print("❌ Dirección IP no válida.")
        return

    start_time = datetime.now()
    print(f"\n[~] Escaneando {target} de puertos 1 al 1024...\n")

    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            for port in range(1, 1025):
                executor.submit(scan_port, target, port)
    except KeyboardInterrupt:
        print("\n⛔ Escaneo cancelado por el usuario.")
        return

    duration = datetime.now() - start_time
    print(f"\n✔️ Escaneo completado en {duration}")


if __name__ == "__main__":
    main()

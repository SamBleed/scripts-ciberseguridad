import socket
from datetime import datetime

# Encabezado
print("#" * 50)
print("  Escáner simple de puertos | by SamBleed")
print("#" * 50)

# Ingresar IP
target = input("\nIngresa la dirección IP a escanear: ").strip()

# Validación básica de IP
try:
    socket.inet_aton(target)
except socket.error:
    print("❌ Dirección IP no válida.")
    exit()

# Tiempo de inicio
start_time =

import csv
import sys

def get_color(temp):
    # Mapeo simple de colores ANSI para gradiente térmico
    if temp < 40: return "\033[38;5;45m"    # Cyan (Frío/Seguro)
    if temp < 100: return "\033[38;5;82m"   # Verde
    if temp < 400: return "\033[38;5;226m"  # Amarillo
    if temp < 800: return "\033[38;5;208m"  # Naranja
    if temp < 1200: return "\033[38;5;196m" # Rojo
    return "\033[38;5;201m"                 # Magenta (Calor Extremo)

try:
    with open('telemetria_escudo.csv', 'r') as f:
        rows = list(csv.reader(f))
        last_row = rows[-1]
        t_final = last_row[0]
        nodes = [float(x) for x in last_row[1:]]

    print(f"\nGRADIENTE TÉRMICO FINAL (t={t_final}s):")
    print("EXTERIOR ", end="")
    for temp in nodes:
        print(f"{get_color(temp)}█", end="")
    print("\033[0m CABINA\n")

except Exception as e:
    print(f"Error procesando telemetría: {e}")
    sys.exit(1)

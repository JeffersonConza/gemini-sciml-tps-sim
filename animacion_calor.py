import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection

# --- PARÁMETROS FÍSICOS ---
L, nx, alpha, dt = 1.0, 20, 0.005, 0.1
dx = L / (nx - 1)
r = alpha * dt / (dx**2)

# --- CARGA OPTIMIZADA (DECIMACIÓN TEMPORAL) ---
time_steps = []
temp_matrix = []

try:
    with open('telemetria_escudo.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        # Cargamos todos pero aplicamos slice [::10] inmediatamente
        rows = list(reader)[::10] 
        for row in rows:
            time_steps.append(float(row[0]))
            temp_matrix.append([float(x) for x in row[1:]])
except FileNotFoundError:
    print("Error: Ejecuta la simulación física primero.")
    exit()

# --- CONFIGURACIÓN DE ESCENA SciML ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 7), dpi=80) # DPI reducido para evitar OOM

x = np.linspace(0, L, nx)
ax.set_xlim(0, L)
ax.set_ylim(0, 1600)
ax.set_xlabel('Profundidad del Escudo (m)', color='gray')
ax.set_ylabel('Temperatura (°C)', color='gray')

# Contexto Aeroespacial
ax.axvspan(0, 0.1, color='red', alpha=0.1)
ax.text(0.02, 1500, 'EXTERIOR:\nPlasma', color='#ff4500', fontweight='bold', fontsize=9)
ax.axvspan(0.9, 1.0, color='blue', alpha=0.1)
ax.text(0.91, 1500, 'INTERIOR:\nCabina', color='#00bfff', fontweight='bold', fontsize=9)

# Ecuación en LaTeX
ax.text(0.05, 0.85, r'$\frac{\partial T}{\partial t} = \alpha \frac{\partial^2 T}{\partial x^2}$', 
        transform=ax.transAxes, fontsize=20, color='white', alpha=0.6)

# HUD
hud_box = dict(boxstyle='round', facecolor='black', alpha=0.5, edgecolor='gray')
hud_text = ax.text(0.65, 0.70, '', transform=ax.transAxes, fontsize=10, family='monospace', bbox=hud_box)

# LineCollection para estela termodinámica
lc = LineCollection([], cmap='inferno', norm=plt.Normalize(0, 1500), lw=3)
ax.add_collection(lc)

def animate(i):
    temps = np.array(temp_matrix[i])
    cabin_t = temps[-1]
    
    # Reconstrucción de segmentos térmicos
    points = np.array([x, temps]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc.set_segments(segments)
    lc.set_array(temps)
    
    # Lógica HUD
    h_color = '#ff3333' if cabin_t > 40 else 'white'
    status = "CRÍTICO" if cabin_t > 40 else "ESTABLE"
    
    hud_text.set_text(
        f"--- TELEMETRÍA (DECIMADA) ---\n"
        f"Tiempo: {time_steps[i]:>6.1f}s\n"
        f"T-Max:  {np.max(temps):>6.1f}°C\n"
        f"T-Cab:  {cabin_t:>6.1f}°C\n"
        f"Num. r: {r:>6.4f}\n"
        f"STATUS: {status}"
    )
    hud_text.set_color(h_color)
    return lc, hud_text

# Sincronización para 10 segundos (100 frames aprox)
total_frames = len(temp_matrix)
duration_ms = 10000
calc_interval = duration_ms / total_frames

print(f"Renderizando {total_frames} frames (Stride 10x)...")
ani = FuncAnimation(fig, animate, frames=total_frames, interval=calc_interval, blit=True)

ani.save('validacion_termica_sciml.gif', writer='pillow', fps=int(total_frames/10))
print("Optimización exitosa: validacion_termica_sciml.gif generado.")

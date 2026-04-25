import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from scipy.interpolate import make_interp_spline
import gc

# --- CARGA CON SLICING DINÁMICO ---
time_steps = []
temp_matrix = []

try:
    with open('telemetria_multicapa.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        all_rows = list(reader)
        stride = max(1, len(all_rows) // 100) # Apuntamos a ~100 frames para fluidez
        for row in all_rows[::stride]:
            time_steps.append(float(row[0]))
            temp_matrix.append([float(val) for val in row[1:]])
        del all_rows
        gc.collect()
except FileNotFoundError:
    print("Error: No se encontró telemetria_multicapa.csv.")
    exit()

# --- CONFIGURACIÓN DE LA ESCENA ---
L, nx = 1.0, 20
x = np.linspace(0, L, nx)
x_smooth = np.linspace(0, L, 200) # Malla fina para suavizado (Spline)

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 7), dpi=100)
fig.subplots_adjust(top=0.88, bottom=0.12, left=0.1, right=0.95)

ax.set_xlim(0, L)
ax.set_ylim(-50, 1650)
ax.set_xlabel('Profundidad del Escudo (m)', color='#AAAAAA', fontsize=11)
ax.set_ylabel('Temperatura (°C)', color='#AAAAAA', fontsize=11)
ax.grid(True, linestyle=':', alpha=0.2)

# Elementos Visuales Estáticos
x_border = 0.526 # Nodo 10 aprox
ax.axvline(x=x_border, color='#FFFFFF', linestyle='--', alpha=0.4, lw=1)
ax.fill_between([0, x_border], -50, 1650, color='#FF0000', alpha=0.05)
ax.fill_between([x_border, L], -50, 1650, color='#0000FF', alpha=0.05)

# Títulos y Ecuación
fig.text(0.5, 0.95, 'NASA TPS DIGITAL TWIN: ANÁLISIS MULTICAPA', 
         color='white', fontsize=15, fontweight='bold', ha='center')
ax.text(0.02, 0.96, r'$\frac{\partial T}{\partial t} = \alpha(x) \nabla^2 T$', 
        transform=ax.transAxes, fontsize=22, color='#00FFCC', alpha=0.8, va='top')

# HUD Config
hud_box = dict(boxstyle='round,pad=0.6', facecolor='#111111', alpha=0.9, edgecolor='#444444')
hud_text = ax.text(0.98, 0.96, '', transform=ax.transAxes, fontsize=10, 
                    family='monospace', bbox=hud_box, ha='right', va='top')

# LineCollection para Gradiente Térmico Suavizado
lc = LineCollection([], cmap='magma', norm=plt.Normalize(0, 1500), lw=4, alpha=0.9)
ax.add_collection(lc)

# Sombra/Glow para la línea
glow_lc = LineCollection([], cmap='magma', norm=plt.Normalize(0, 1500), lw=8, alpha=0.2)
ax.add_collection(glow_lc)

def animate(i):
    y = np.array(temp_matrix[i])
    
    # Suavizado por Spline
    spline = make_interp_spline(x, y, k=3)
    y_smooth = spline(x_smooth)
    y_smooth = np.clip(y_smooth, 25, 1500) # Evitar artefactos del spline
    
    points = np.array([x_smooth, y_smooth]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    lc.set_segments(segments)
    lc.set_array(y_smooth)
    
    glow_lc.set_segments(segments)
    glow_lc.set_array(y_smooth)
    
    t_cab = y[-1]
    status = "CRÍTICO" if t_cab > 40 else "NOMINAL"
    status_color = "#FF3333" if t_cab > 40 else "#00FF00"
    
    hud_text.set_text(
        f"TIME ELAPSED : {time_steps[i]:>6.1f} s\n"
        f"MAX TEMP     : {np.max(y):>6.1f} °C\n"
        f"CABIN TEMP   : {t_cab:>6.1f} °C\n"
        f"MISSION STAT : {status}"
    )
    hud_text.set_color(status_color)
    
    return lc, glow_lc, hud_text

ani = FuncAnimation(fig, animate, frames=len(temp_matrix), interval=60, blit=True)
print(f"Generando validacion_multicapa.gif ({len(temp_matrix)} frames)...")
ani.save('validacion_multicapa.gif', writer='pillow', fps=15)
plt.close()
gc.collect()
print("¡Actualización de 1D completada!")

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
import gc # Garbage Collector para control de RAM

# --- CARGA CON SLICING DINÁMICO (~80 FRAMES) ---
time_steps = []
temp_matrix = []

try:
    with open('telemetria_multicapa.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        all_rows = list(reader)
        
        target_frames = 80
        stride = max(1, len(all_rows) // target_frames)
        
        selected_rows = all_rows[::stride]
        for row in selected_rows:
            time_steps.append(float(row[0]))
            temp_matrix.append([float(val) for val in row[1:]])
        
        del all_rows
        gc.collect()
except FileNotFoundError:
    print("Error: No se encontró telemetria_multicapa.csv.")
    exit()

# --- CONFIGURACIÓN DE LA ESCENA SciML (LAYOUT PROFESIONAL) ---
L, nx = 1.0, 20
x = np.linspace(0, L, nx)
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 7), dpi=90)

# Ajuste de márgenes: liberamos el 15% superior para HUD y Ecuación
fig.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.95)

ax.set_xlim(0, L)
ax.set_ylim(0, 1600)
ax.set_xlabel('Profundidad del Escudo (m)', color='#888888', fontsize=11)
ax.set_ylabel('Temperatura (°C)', color='#888888', fontsize=11)
fig.suptitle('ESTUDIO DE DIFUSIÓN TÉRMICA: ESCUDO MULTICAPA', color='white', 
             fontsize=14, fontweight='bold', y=0.96)

# Visuales Multicapa (Zonas de materiales)
x_border = x[10]
ax.axvline(x=x_border, color='white', linestyle='--', alpha=0.3)
ax.axvspan(0, x_border, color='#440000', alpha=0.2)
ax.axvspan(x_border, L, color='#000044', alpha=0.2)
ax.text(x_border/2, 50, 'CAPA ABLATIVA', color='#ff6666', ha='center', fontsize=9, alpha=0.8)
ax.text(x_border + (L-x_border)/2, 50, 'AISLANTE TÉRMICO', color='#6666ff', ha='center', fontsize=9, alpha=0.8)

# Ecuación en LaTeX (Anclada en la esquina superior izquierda interna)
ax.text(0.02, 0.95, r'$\frac{\partial T}{\partial t} = \alpha(x) \nabla^2 T$', 
        transform=ax.transAxes, fontsize=20, color='white', alpha=0.7, va='top', ha='left')

# HUD Dinámico (Anclado en la esquina superior derecha interna)
hud_box = dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.8, edgecolor='#444444')
hud_text = ax.text(0.98, 0.95, '', transform=ax.transAxes, fontsize=10, 
                    family='monospace', bbox=hud_box, ha='right', va='top')

# Estela Térmica (LineCollection)
lc = LineCollection([], cmap='inferno', norm=plt.Normalize(0, 1500), lw=3.5)
ax.add_collection(lc)

def animate(i):
    temps = np.array(temp_matrix[i])
    points = np.array([x, temps]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc.set_segments(segments)
    lc.set_array(temps)
    
    t_cab = temps[-1]
    h_color = '#ff3333' if t_cab > 40 else '#00ff00'
    status = "CRÍTICO" if t_cab > 40 else "ESTABLE"
    
    hud_text.set_text(
        f"TIME:  {time_steps[i]:>6.1f}s\n"
        f"T-MAX: {np.max(temps):>6.1f}°C\n"
        f"T-CAB: {t_cab:>6.1f}°C\n"
        f"MISSION: {status}"
    )
    hud_text.set_color(h_color)
    return lc, hud_text

# --- RENDERIZADO ---
total_frames = len(temp_matrix)
print(f"Renderizando {total_frames} fotogramas a 10 FPS...")

ani = FuncAnimation(fig, animate, frames=total_frames, interval=100, blit=True)

ani.save('validacion_multicapa.gif', writer='pillow', fps=10)

plt.close(fig)
gc.collect()

print("Layout corregido. 'validacion_multicapa.gif' generado con éxito.")

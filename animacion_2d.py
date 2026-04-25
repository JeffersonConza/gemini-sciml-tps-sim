import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import gc

# --- CARGA DE DATOS ---
try:
    frames = np.load('telemetria_2d.npy')
except FileNotFoundError:
    print("Error: No se encontró telemetria_2d.npy.")
    exit()

# --- CONFIGURACIÓN DE LA ESCENA ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)

# Imagen con interpolación para suavizado de píxeles
im = ax.imshow(frames[0], cmap='afmhot', interpolation='bicubic', 
               origin='upper', extent=[0, 1, 0, 1], vmin=25, vmax=1500)

# Contornos para resaltar el frente de calor
contours = ax.contour(frames[0], levels=[100, 300, 700, 1000], 
                     extent=[0, 1, 0, 1], colors='cyan', alpha=0.3, linewidths=0.8)

cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Temperatura (°C)', color='#AAAAAA')

ax.set_title('MAPA TERMOGRÁFICO 2D: REENTRADA HIPERSÓNICA', fontweight='bold', pad=20)
ax.set_xlabel('Ancho del Escudo (m)', color='#888888')
ax.set_ylabel('Profundidad del Escudo (m)', color='#888888')

# Elementos de Contexto
ax.axhline(y=0.625, color='white', linestyle='--', alpha=0.2)
ax.text(0.5, 0.85, 'ESCUDO ABLATIVO', color='white', ha='center', fontsize=10, alpha=0.4, fontweight='bold')
ax.text(0.5, 0.15, 'AISLANTE TÉRMICO', color='white', ha='center', fontsize=10, alpha=0.4, fontweight='bold')

# HUD Dinámico
hud_box = dict(boxstyle='square,pad=0.5', facecolor='black', alpha=0.7, edgecolor='#333333')
hud_text = ax.text(0.05, 0.05, '', transform=ax.transAxes, color='#00FF00', 
                    family='monospace', fontsize=9, bbox=hud_box)

def animate(i):
    global contours
    im.set_array(frames[i])
    
    # Actualizar contornos (eliminando los anteriores)
    for c in contours.collections:
        c.remove()
    contours = ax.contour(frames[i], levels=[100, 300, 700, 1000], 
                         extent=[0, 1, 0, 1], colors='cyan', alpha=0.3, linewidths=0.8)
    
    t_max = np.max(frames[i])
    t_cab = np.mean(frames[i][-1, :]) # Promedio en la base de la cabina
    
    status = "NOMINAL"
    h_color = "#00FF00"
    if t_cab > 40:
        status = "ALERTA"
        h_color = "#FF3333"

    hud_text.set_text(
        f"DATA FRAME : {i:03d}\n"
        f"MAX TEMP   : {t_max:>6.1f} °C\n"
        f"AVG CABIN  : {t_cab:>6.1f} °C\n"
        f"MISSION    : {status}"
    )
    hud_text.set_color(h_color)
    
    return im, hud_text

print(f"Renderizando validacion_2d.gif ({len(frames)} frames)...")
ani = FuncAnimation(fig, animate, frames=len(frames), interval=50, blit=False) # Blit False para contornos

ani.save('validacion_2d.gif', writer='pillow', fps=20)
plt.close()
gc.collect()
print("¡Actualización de 2D completada!")

import numpy as np
import csv

# --- CONFIGURACIÓN DE LA MALLA 2D ---
nx, ny = 40, 40 # Resolución de la sección transversal
L = 1.0
dx = dy = L / (nx - 1)

# Materiales (Zonas 2D)
alpha_ablativo = 0.005
alpha_aislante = 0.0005

# Crear mapa de difusividad (Capa superior ablativa, inferior aislante)
alpha_map = np.zeros((ny, nx))
alpha_map[:15, :] = alpha_ablativo
alpha_map[15:, :] = alpha_aislante

# Estabilidad CFL 2D: dt <= dx^2 / (4 * alpha)
dt = 0.005
nt = 500

# Inicialización
u = np.full((ny, nx), 25.0)

print(f"Iniciando Simulación Térmica 2D ({nx}x{ny})...")

# --- BUCLE TEMPORAL ---
# Guardaremos estados seleccionados en un archivo binario comprimido para la animación
frames = []

for n in range(nt):
    # Fronteras (BCs)
    u[0, :] = 1500.0   # Borde Exterior (Plasma)
    u[-1, :] = 25.0    # Borde Interior (Cabina)
    u[:, 0] = u[:, 1]  # Lados aislados (Adiabáticos)
    u[:, -1] = u[:, -2]

    # Esquema de Diferencias Finitas 2D
    u_new = u.copy()
    
    # Vectorización acelerada con NumPy
    laplacian = (
        (u[2:, 1:-1] - 2*u[1:-1, 1:-1] + u[:-2, 1:-1]) / dx**2 +
        (u[1:-1, 2:] - 2*u[1:-1, 1:-1] + u[1:-1, :-2]) / dy**2
    )
    
    u_new[1:-1, 1:-1] = u[1:-1, 1:-1] + alpha_map[1:-1, 1:-1] * dt * laplacian
    u = u_new

    if n % 5 == 0:
        frames.append(u.copy())

# Guardar datos para el visualizador
np.save('telemetria_2d.npy', np.array(frames))
print("Simulación 2D completada. Datos guardados en 'telemetria_2d.npy'.")

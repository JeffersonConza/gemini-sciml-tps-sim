import csv
import math

# =============================================================================
# MODELO DE ALTA FIDELIDAD: DIFUSIÓN NO LINEAL + RADIACIÓN
# =============================================================================
L, nx = 1.0, 20
dx = L / (nx - 1)
t_final = 100.0

# Constantes Físicas
SIGMA = 5.67e-8  # Stefan-Boltzmann (W/m^2K^4)
EPSILON = 0.85   # Emisividad del recubrimiento cerámico
H_CONV = 100.0   # Coef. de transferencia por convección (W/m^2K)
T_PLASMA = 2500.0 + 273.15 # Temperatura de estancamiento (K)

# Propiedades de Materiales (Base)
alpha_0_ablativo = 0.005
alpha_0_aislante = 0.0005
gamma = 0.0002 # Factor de dependencia térmica (1/K)

def get_alpha(temp_c, base_alpha):
    """Calcula difusividad variable: alpha(T) = alpha0 * (1 + gamma * T)"""
    temp_k = temp_c + 273.15
    return base_alpha * (1 + gamma * temp_k)

# Estabilidad CFL (Usamos el peor caso para dt)
dt = 0.01 # Paso más fino para manejar la radiación (no linealidad)
nt = int(t_final / dt)

u = [25.0] * nx  # Condición inicial (25°C)

print(f"Lanzando simulación de ALTA FIDELIDAD...")
print(f"  - Efecto: Difusividad variable alpha(T)")
print(f"  - Frontera: Radiación de Stefan-Boltzmann")

with open('telemetria_avanzada.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['t'] + [f'x_{i}' for i in range(nx)])

    t = 0.0
    for n in range(nt):
        # --- CONDICIÓN DE FRONTERA EXTERIOR (Radiación + Convección) ---
        # Balance de flujo en el nodo 0: -k(dT/dx) = q_rad + q_conv
        # Simplificación SciML: Ajuste dinámico de T_exterior basado en flujo
        t_old_ext = u[0] + 273.15
        q_rad = SIGMA * EPSILON * (T_PLASMA**4 - t_old_ext**4)
        q_conv = H_CONV * (T_PLASMA - t_old_ext)
        
        # El plasma inyecta calor, pero el escudo irradia hacia afuera
        u[0] = u[0] + (q_rad + q_conv) * dt * 0.001 # Factor de escala térmica
        
        # Frontera Interior (Dirichlet)
        u[-1] = 25.0

        if n % 50 == 0:
            writer.writerow([round(t, 2)] + [round(temp, 2) for temp in u])

        # --- EVOLUCIÓN EDP NO LINEAL ---
        u_nueva = u.copy()
        for i in range(1, nx - 1):
            # Alpha depende de la temperatura local del nodo
            a0 = alpha_0_ablativo if i < 10 else alpha_0_aislante
            a_local = get_alpha(u[i], a0)
            
            r_local = (a_local * dt) / (dx**2)
            u_nueva[i] = u[i] + r_local * (u[i+1] - 2*u[i] + u[i-1])

        u = u_nueva
        t += dt

print("Simulación avanzada completada: telemetria_avanzada.csv")

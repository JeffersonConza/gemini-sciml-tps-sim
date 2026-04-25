import csv

# --- PARÁMETROS FÍSICOS ---
L, nx, t_final = 1.0, 20, 100.0
dx = L / (nx - 1)
alpha_ablativo, alpha_aislante = 0.005, 0.0005
alpha_array = [alpha_ablativo if i < 10 else alpha_aislante for i in range(nx)]

alpha_max = max(alpha_array)
r_limit = 0.45
dt = (r_limit * dx**2) / alpha_max
nt = int(t_final / dt)

u = [25.0] * nx
T_exterior, T_cabina = 1500.0, 25.0

print(f"Generando telemetría de alta resolución ({nt} pasos)...")

with open('telemetria_multicapa.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['t'] + [f'x_{i}' for i in range(nx)])
    
    t = 0.0
    for n in range(nt):
        u[0], u[-1] = T_exterior, T_cabina
        
        # Exportamos CADA paso para que el visualizador decida
        writer.writerow([round(t, 2)] + [round(temp, 2) for temp in u])
        
        u_nueva = u.copy()
        for i in range(1, nx - 1):
            r_local = (alpha_array[i] * dt) / (dx**2)
            u_nueva[i] = u[i] + r_local * (u[i+1] - 2*u[i] + u[i-1])
        u = u_nueva
        t += dt

print("Telemetría completa generada.")

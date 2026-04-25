import csv

# Parámetros físicos y espaciales del escudo
L = 1.0           # Grosor del escudo unidimensional (m)
nx = 20           # Número de nodos espaciales discretos
dx = L / (nx - 1) # Distancia entre nodos (Delta x)
alpha = 0.005     # Difusividad térmica del material espacial

# Parámetros temporales
dt = 0.1          # Paso de tiempo (Delta t)
t_final = 100.0   # Segundos totales de reentrada simulados
nt = int(t_final / dt)

# Cálculo de la constante mágica y Condición de Courant
r = alpha * dt / (dx**2)
print(f"Iniciando simulación. Número de Courant (r) = {round(r, 4)}")
if r > 0.5:
    print("¡PELIGRO! r > 0.5. La simulación matemática explotará.")
    exit()

# Condiciones iniciales y de frontera de Dirichlet
u = [25.0] * nx   # El escudo arranca a 25°C
T_exterior = 1500.0 # Calor constante por fricción hipersónica
T_cabina = 25.0     # Control térmico de la cabina

with open('telemetria_escudo.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Encabezados: Tiempo + Nodos
    headers = ['t'] + [f'x_{i}' for i in range(nx)]
    writer.writerow(headers)

    t = 0.0
    # Bucle de integración temporal
    for n in range(nt):
        # Aplicamos Fronteras de Dirichlet obligatorias
        u[0] = T_exterior
        u[-1] = T_cabina

        writer.writerow([round(t, 2)] + [round(temp, 2) for temp in u])

        # Bucle de diferencias finitas en el espacio (FTCS)
        u_nueva = u.copy()
        for i in range(1, nx - 1):
            u_nueva[i] = u[i] + r * (u[i+1] - 2*u[i] + u[i-1])

        u = u_nueva
        t += dt

print("Simulación de EDP exitosa. Datos exportados a 'telemetria_escudo.csv'.")

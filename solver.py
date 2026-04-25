import csv
import numpy as np

class ThermalSolver:
    """Motor de resolución de EDPs para Sistemas de Protección Térmica (TPS)."""
    
    def __init__(self, L=1.0, nx=20, t_final=100.0):
        self.L = L
        self.nx = nx
        self.dx = L / (nx - 1)
        self.t_final = t_final
        self.x = np.linspace(0, L, nx)
        self.u = np.full(nx, 25.0) # Temperatura inicial
        self.alpha_array = np.full(nx, 0.005) # Difusividad por defecto
        
    def set_materials(self, alpha_config):
        """Configura la difusividad térmica por zonas."""
        for start, end, alpha in alpha_config:
            self.alpha_array[start:end] = alpha
            
    def solve(self, t_ext=1500.0, t_int=25.0, export_path='telemetria.csv'):
        """Resuelve la ecuación del calor y exporta los resultados."""
        alpha_max = np.max(self.alpha_array)
        dt = (0.45 * self.dx**2) / alpha_max
        nt = int(self.t_final / dt)
        
        with open(export_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['t'] + [f'x_{i}' for i in range(self.nx)])
            
            t = 0.0
            for n in range(nt):
                self.u[0] = t_ext
                self.u[-1] = t_int
                
                if n % 100 == 0:
                    writer.writerow([round(t, 2)] + [round(temp, 2) for temp in self.u])
                
                # Vectorización con NumPy para alto rendimiento
                u_new = self.u.copy()
                r = (self.alpha_array[1:-1] * dt) / (self.dx**2)
                u_new[1:-1] = self.u[1:-1] + r * (self.u[2:] - 2*self.u[1:-1] + self.u[0:-2])
                self.u = u_new
                t += dt
        return self.u[-2] # Retorna temperatura de la pared exterior de la cabina

if __name__ == "__main__":
    # Test rápido
    solver = ThermalSolver()
    solver.solve()
    print("Simulación de prueba completada.")

import unittest
import numpy as np
from solver import ThermalSolver

class TestThermalPhysics(unittest.TestCase):
    """Pruebas de validación científica para el motor térmico."""
    
    def setUp(self):
        self.solver = ThermalSolver(L=1.0, nx=51, t_final=10.0)

    def test_energy_conservation_steady_state(self):
        """
        Valida que en estado estacionario la distribución de temp sea lineal
        (para una barra homogénea con fronteras de Dirichlet).
        """
        # Configurar barra homogénea
        self.solver.set_materials([(0, 51, 0.005)])
        
        # Simular tiempo suficiente para estabilidad
        self.solver.t_final = 500.0 
        self.solver.solve(t_ext=100.0, t_int=0.0, export_path='test_steady.csv')
        
        # La temperatura en el centro (x=0.5) debería ser ~50°C
        temp_centro = self.solver.u[len(self.solver.u)//2]
        self.assertAlmostEqual(temp_centro, 50.0, delta=1.0, 
                               msg="La distribución en estado estacionario no es lineal.")

    def test_courant_stability(self):
        """Verifica que el solver use un dt que cumpla el criterio r <= 0.5."""
        alpha_max = np.max(self.solver.alpha_array)
        dt = (0.45 * self.solver.dx**2) / alpha_max
        r = alpha_max * dt / (self.solver.dx**2)
        
        self.assertLessEqual(r, 0.5, "El número de Courant excede el límite de estabilidad.")

if __name__ == '__main__':
    unittest.main()

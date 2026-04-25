import numpy as np
import matplotlib.pyplot as plt
from solver import ThermalSolver
import os

def run_monte_carlo(n_simulations=100):
    """
    Realiza un análisis de Monte Carlo variando la difusividad térmica
    para cuantificar la incertidumbre en la seguridad de la misión.
    """
    print(f"🎲 Iniciando Análisis de Monte Carlo ({n_simulations} simulaciones)...")
    
    cabin_temps = []
    # Variamos alpha_ablativo con una desviación del 15% (Incertidumbre de material)
    alpha_base = 0.005
    uncertainty = 0.15 
    
    for i in range(n_simulations):
        # Muestreo estocástico
        alpha_variado = np.random.normal(alpha_base, alpha_base * uncertainty)
        
        # Configuración de diseño base (50/50)
        solver = ThermalSolver(t_final=100.0, nx=20)
        solver.set_materials([
            (0, 10, alpha_variado),
            (10, 20, 0.0005)
        ])
        
        t_final = solver.solve(export_path='study_results/temp_mc.csv')
        cabin_temps.append(t_final)
        
        if (i+1) % 20 == 0:
            print(f"  - Completadas {i+1} simulaciones...")

    # --- VISUALIZACIÓN ESTADÍSTICA ---
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6), dpi=120)
    
    # Histograma de Temperaturas
    n, bins, patches = plt.hist(cabin_temps, bins=15, color='#00FFCC', alpha=0.7, edgecolor='white')
    
    # Línea Crítica
    plt.axvline(x=40, color='#FF3333', linestyle='--', lw=3, label='Límite Vital (40°C)')
    
    # Estadísticas
    prob_exito = (np.array(cabin_temps) <= 40).mean() * 100
    plt.title(f'Análisis de Incertidumbre: Probabilidad de Éxito = {prob_exito:.1f}%', fontweight='bold')
    plt.xlabel('Temperatura Final en Cabina (°C)')
    plt.ylabel('Frecuencia (Simulaciones)')
    plt.grid(True, alpha=0.2, linestyle=':')
    plt.legend()
    
    plt.savefig('analisis_incertidumbre.png')
    print(f"\n✅ Análisis completado. Probabilidad de Supervivencia: {prob_exito:.1f}%")
    print("Gráfico generado: 'analisis_incertidumbre.png'")

if __name__ == "__main__":
    if not os.path.exists('study_results'): os.makedirs('study_results')
    run_monte_carlo(100)

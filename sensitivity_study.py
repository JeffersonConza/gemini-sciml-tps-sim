from solver import ThermalSolver
import matplotlib.pyplot as plt
import os

def run_dataops_study():
    """Ejecuta un estudio de sensibilidad sobre el espesor del aislante."""
    print("🚀 Iniciando Pipeline de DataOps: Optimización de Diseño...")
    
    insulation_ratios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] # Porcentaje de aislante
    final_temps = []
    
    if not os.path.exists('study_results'):
        os.makedirs('study_results')

    for ratio in insulation_ratios:
        split_node = int(20 * (1 - ratio))
        config = [
            (0, split_node, 0.005),   # Ablativo
            (split_node, 20, 0.0005)  # Aislante
        ]
        
        solver = ThermalSolver(t_final=120.0)
        solver.set_materials(config)
        
        csv_name = f'study_results/sim_ratio_{ratio}.csv'
        t_cabina = solver.solve(export_path=csv_name)
        final_temps.append(t_cabina)
        
        print(f"  - Ratio {ratio*100}%: Temp Cabina = {t_cabina:.2f}°C")

    # Visualización de resultados de ingeniería
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
    
    ratios_pct = [r*100 for r in insulation_ratios]
    
    # Zonas de seguridad
    ax.axhspan(0, 40, color='#00ff00', alpha=0.15, label='Zona Segura (<= 40°C)')
    ax.axhspan(40, max(final_temps)+10 if final_temps else 100, color='#ff0000', alpha=0.15, label='Zona Crítica (> 40°C)')
    
    ax.plot(ratios_pct, final_temps, marker='o', markersize=8, color='#00ffcc', lw=2.5, zorder=3)
    ax.axhline(y=40, color='red', linestyle='--', linewidth=2, zorder=2)
    
    # Anotaciones
    for i, txt in enumerate(final_temps):
        ax.annotate(f"{txt:.1f}°C", (ratios_pct[i], final_temps[i]), 
                    textcoords="offset points", xytext=(0, 10), ha='center', color='white', fontsize=9)

    ax.set_title('NASA SciML: Optimización de Aislante vs Temperatura en Cabina', fontweight='bold', fontsize=14, pad=15)
    ax.set_xlabel('Proporción de Aislante Térmico (%)', fontsize=12)
    ax.set_ylabel('Temperatura Final en Cabina (°C)', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('optimizacion_diseno.png', dpi=150)
    plt.close()
    print("\n✅ Reporte de optimización generado: 'optimizacion_diseno.png'")

if __name__ == "__main__":
    run_dataops_study()

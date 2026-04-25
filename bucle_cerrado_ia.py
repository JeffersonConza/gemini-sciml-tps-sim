import os
import subprocess
from solver import ThermalSolver

# --- CONFIGURACIÓN DEL BUCLE CERRADO ---
LIMITE_VITAL = 40.0 # °C
RATIO_INICIAL = 0.2 # Empezamos con poco aislante
MAX_INTENTOS = 5

def consultar_ia(csv_path, ratio_actual):
    """Invoca a Gemini CLI para auditar la telemetría y sugerir cambios."""
    prompt = (
        f"Actúa como un Auditor de Seguridad de la NASA. Analiza la telemetría en {csv_path}. "
        f"El diseño actual tiene un {ratio_actual*100}% de aislante térmico. "
        "1. ¿La temperatura final de la cabina (último nodo) es menor a 40°C? "
        "2. Si es mayor, responde ESTRICTAMENTE con la palabra 'REDISÉÑESE'. "
        "3. Si es menor, responde ESTRICTAMENTE con la palabra 'MISIÓN_SEGURA'. "
        "Acompaña tu veredicto con una breve explicación técnica."
    )
    
    # Ejecución del comando de sistema para Gemini CLI
    try:
        # Nota: Usamos shell=True para capturar la salida del comando gemini
        result = subprocess.run(['gemini', prompt], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error de conexión con IA: {e}"

def optimizacion_cerrada():
    print("🛰️ Iniciando Bucle de Optimización de Diseño asistido por IA...")
    
    ratio_aislante = RATIO_INICIAL
    
    for intento in range(1, MAX_INTENTOS + 1):
        print(f"\n--- CICLO DE DISEÑO #{intento} (Aislante: {ratio_aislante*100}%) ---")
        
        # 1. EJECUCIÓN DE LA SIMULACIÓN FÍSICA
        split_node = int(20 * (1 - ratio_aislante))
        config = [
            (0, split_node, 0.005),   # Capa Ablativa
            (split_node, 20, 0.0005)  # Capa Aislante
        ]
        
        solver = ThermalSolver(t_final=60.0) # Reentrada de 60s
        solver.set_materials(config)
        csv_path = 'telemetria_optimizacion.csv'
        t_cabina = solver.solve(export_path=csv_path)
        
        print(f"  [Simulación] Finalizada. T-Cabina: {t_cabina:.2f}°C")
        
        # 2. AUDITORÍA DE IA (Closed-Loop Feedback)
        print("  [IA] Consultando veredicto de seguridad...")
        veredicto_ia = consultar_ia(csv_path, ratio_aislante)
        
        print(f"  [Veredicto IA]: {veredicto_ia.strip().split('.')[0]}...") # Mostrar solo el inicio

        # 3. LÓGICA DE DECISIÓN BASADA EN IA
        if "MISIÓN_SEGURA" in veredicto_ia:
            print(f"\n✅ DISEÑO VALIDADO POR IA en el intento {intento}.")
            print(f"El diseño final óptimo requiere un {ratio_aislante*100}% de aislante.")
            with open("reporte_final_ia.md", "w") as f:
                f.write(f"# Reporte de Misión Validado\n\n{veredicto_ia}")
            break
        else:
            print("  [Acción] La IA sugiere rediseño. Aumentando espesor del aislante (+15%)...")
            ratio_aislante += 0.15 # Ajuste paramétrico sugerido por el fallo
            
        if intento == MAX_INTENTOS:
            print("\n❌ Se alcanzó el máximo de intentos sin validación de seguridad.")

if __name__ == "__main__":
    optimizacion_cerrada()

# 🛡️ AeroShield-SciML: Simulación de Reentrada Atmosférica y Difusión Térmica Multicapa

[![SciML](https://img.shields.io/badge/Specialty-SciML-blueviolet)](https://github.com/topics/sciml)
[![NASA-Inspired](https://img.shields.io/badge/Sector-Aerospace-blue)](https://www.nasa.gov/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este repositorio contiene un framework de **Scientific Machine Learning (SciML)** y computación científica diseñado para simular la degradación térmica de un escudo de reentrada aeroespacial. Utiliza una arquitectura de materiales compuestos (Ablativo + Aislante) y un flujo de trabajo de **DataOps** automatizado para la toma de decisiones críticas asistida por IA.

---

## 🔬 Física y Matemática del Sistema

El núcleo del simulador resuelve la **Ecuación del Calor en 1D** para un medio heterogéneo, donde las propiedades termofísicas varían en función de la profundidad del material $x$.

### Ecuación de Gobierno
La evolución de la temperatura $T$ en el tiempo $t$ está definida por:

$$\frac{\partial T}{\partial t} = \alpha(x) \frac{\partial^2 T}{\partial x^2}$$

Donde $\alpha(x)$ es la **difusividad térmica**, definida de forma seccionada para el diseño multicapa.

### Discretización Numérica (FTCS)
Implementamos el esquema de **Diferencias Finitas** de tipo *Forward-Time Central-Space* (FTCS). La aproximación de la temperatura en el nodo $i$ para el tiempo $n+1$ se calcula como:

$$T_{i}^{n+1} = T_{i}^{n} + \frac{\alpha_i \Delta t}{\Delta x^2} \left( T_{i+1}^{n} - 2T_{i}^{n} + T_{i-1}^{n} \right)$$

Para garantizar la estabilidad numérica de la solución, el simulador calcula automáticamente el paso de tiempo $\Delta t$ respetando el **Criterio de Estabilidad de Von Neumann**:

$$r = \frac{\alpha_{max} \Delta t}{\Delta x^2} \leq 0.5$$

---

## 🛡️ Diseño del Escudo Compuesto

El sistema modela un escudo de 1 metro de espesor con una estrategia de protección dual:

1.  **Capa Ablativa (0.0m - 0.5m):**
    *   **Difusividad ($\alpha$):** $0.005$
    *   **Función:** Disipar la carga térmica extrema inicial ($1500^\circ\text{C}$) mediante la absorción de energía.
2.  **Aislante Térmico (0.5m - 1.0m):**
    *   **Difusividad ($\alpha$):** $0.0005$ (10 veces menor)
    *   **Función:** Actuar como barrera pasiva para asegurar que la temperatura en la interfaz de la cabina no comprometa la integridad estructural o humana.

---

## 🏗️ Arquitectura del Flujo DataOps

El proyecto implementa un pipeline de ingeniería de datos y simulación orquestado por un motor de automatización en Bash (`pipeline_reentrada.sh`):

1.  **Simulación Física (`escudo_multicapa.py`):** Motor numérico que genera telemetría de alta resolución en formato CSV.
2.  **Visualización SciML (`animacion_multicapa.py`):** Generador de assets visuales que renderiza la difusión térmica, incluyendo un HUD dinámico y la representación de la EDP en tiempo real.
3.  **Auditoría de Seguridad IA (Gemini CLI):** Un agente de IA actúa como Oficial de Seguridad de la NASA, analizando los datos generados para emitir un veredicto de "Misión Segura" o "Falla Crítica" basado en los umbrales térmicos de la cabina ($<40^\circ\text{C}$).

---

## 🚀 Ejecución en Linux

### Requisitos Previos
Asegúrate de tener instalado Python 3 y las dependencias necesarias:
```bash
pip install numpy matplotlib
```

### Lanzar el Pipeline Completo
El orquestador gestiona la ejecución secuencial, la validación de errores y la auditoría final:

```bash
# Otorgar permisos de ejecución
chmod +x pipeline_reentrada.sh

# Ejecutar el sistema de monitoreo
./pipeline_reentrada.sh
```

### Resultados Generados
*   `telemetria_multicapa.csv`: Datos crudos de la evolución térmica.
*   `validacion_multicapa.gif`: Animación profesional de la simulación.
*   `reporte_supervivencia.md`: Análisis técnico y veredicto emitido por la IA.

---

> **Nota del Ingeniero:** Este sistema demuestra cómo la integración de métodos numéricos tradicionales con orquestación moderna y Large Language Models permite crear gemelos digitales robustos para entornos de misión crítica.

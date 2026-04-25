# 🛰️ ReentryFlow: SciML Digital Twin para Escudos Térmicos Multicapa

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SciML](https://img.shields.io/badge/Physics-Informed-orange.svg)]()
[![Automation](https://img.shields.io/badge/Bash-v2.0-green.svg)]()

Sistema de simulación de alta fidelidad y pipeline de **DataOps** para el análisis transitorio de la difusión de calor en escudos de protección térmica (TPS). Este Digital Twin permite predecir fallos críticos y optimizar materiales antes de la fabricación.

## 📊 Visualización de Ingeniería

### Perfil Térmico 1D (Estela Dinámica y Monitoreo HUD)
Animación suavizada mediante splines que muestra la penetración del calor. La capa exterior ablativa disipa energía mientras que el aislante protege el núcleo.
<p align="center">
  <img src="validacion_multicapa.gif" alt="Validación Multicapa 1D" width="800"/>
</p>

### Mapa de Calor Termográfico 2D
Simulación de campo bidimensional con isotermas dinámicas para análisis de efectos de borde y distribución lateral de temperatura.
<p align="center">
  <img src="validacion_2d.gif" alt="Validación 2D" width="600"/>
</p>

### Gestión de Riesgos y Optimización
| Optimización de Diseño | Cuantificación de Incertidumbre |
| :---: | :---: |
| ![Optimización](optimizacion_diseno.png) | ![Monte Carlo](analisis_incertidumbre.png) |
| *Búsqueda del espesor mínimo seguro.* | *Análisis estocástico de Monte Carlo (100 runs).* |

---

## 🔬 Física y Matemática

### Ecuación Diferencial Parcial (EDP)
$$\frac{\partial T}{\partial t} = \alpha(x, T) \nabla^2 T$$

Donde $\alpha(x, T)$ es la difusividad térmica, que en este modelo es tanto **espacialmente heterogénea** (multicapa) como **térmicamente no lineal** (variable con $T$ en el motor avanzado).

### Esquema Numérico
Se utiliza el método **FTCS (Forward-Time Central-Space)** con un paso de tiempo $\Delta t$ controlado por el criterio de estabilidad de Courant:
$$r = \frac{\alpha_{max} \Delta t}{\Delta x^2} \le 0.45$$

---

## 🏗️ Flujo de Operaciones (DataOps)

```mermaid
graph TD
    A[escudo_multicapa.py] -->|Simulación EDP| B(telemetria_multicapa.csv)
    B --> C{Pipeline Orchestrator}
    C --> D[animacion_multicapa.py]
    C --> E[bucle_cerrado_ia.py]
    D -->|Renderizado| F[validacion_multicapa.gif]
    E -->|Analítica IA| G[Gemini Pro Auditor]
    G -->|Veredicto Técnico| H[reporte_supervivencia.md]
    H -->|Retroalimentación| A
```

---

## 🚀 Ejecución

### Orquestador Avanzado (`pipeline_reentrada.sh`)
El script de Bash v2.0 automatiza todo el flujo con manejo de errores y limpieza selectiva:

```bash
# Ejecución estándar (Simulación + Animación + Auditoría IA)
./pipeline_reentrada.sh

# Limpieza de datos antiguos y salto de IA
./pipeline_reentrada.sh --clean --skip-ia
```

### Requisitos
```bash
pip install matplotlib numpy pillow scipy
```

---

## 📂 Estructura del Proyecto
*   `escudo_multicapa.py`: Motor físico 1D.
*   `escudo_2d.py`: Motor físico 2D para análisis de campo.
*   `escudo_avanzado.py`: Física de radiación y $\alpha(T)$ no lineal.
*   `sensitivity_study.py`: Algoritmo de optimización de diseño.
*   `monte_carlo_analysis.py`: Cuantificación de incertidumbre.
*   `animacion_*.py`: Generadores de visualización profesional.
*   `bucle_cerrado_ia.py`: Optimizador autónomo guiado por IA.

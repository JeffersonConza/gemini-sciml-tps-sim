# 🛰️ ReentryFlow: SciML Digital Twin para Escudos Térmicos Multicapa

Sistema de simulación de alta fidelidad y pipeline de **DataOps** para el análisis transitorio de la difusión de calor en escudos de protección térmica (TPS) durante la reentrada atmosférica hipersónica.

![Visualización Térmica](validacion_multicapa.gif)

## 🔬 Física y Matemática del Modelo

El núcleo del motor físico resuelve la **Ecuación del Calor Parcial Unidimensional** con difusividad térmica espacialmente heterogénea $\alpha(x)$. Este modelo predice cómo el frente de plasma penetra a través de los materiales compuestos del escudo.

### Ecuación Diferencial Parcial (EDP)
$$\frac{\partial T}{\partial t} = \alpha(x) \nabla^2 T$$

Donde:
*   $T$: Temperatura en función del tiempo ($t$) y la posición ($x$).
*   $\alpha(x)$: Difusividad térmica local del material ($m^2/s$).

### Discretización Numérica (Esquema FTCS)
Para la integración temporal, implementamos el método **Forward-Time Central-Space (FTCS)**, transformando la EDP en un algoritmo iterativo:

$$T_{i}^{n+1} = T_{i}^{n} + \frac{\alpha_i \Delta t}{\Delta x^2} (T_{i+1}^{n} - 2T_{i}^{n} + T_{i-1}^{n})$$

### Criterio de Estabilidad (CFL)
Para garantizar la convergencia matemática y evitar divergencias numéricas, el paso de tiempo $\Delta t$ se calcula dinámicamente basándose en el **Número de Courant ($r$)** máximo permitido:

$$r = \frac{\alpha_{max} \Delta t}{\Delta x^2} \le 0.45$$

## 🛡️ Diseño del Escudo Compuesto

A diferencia de los modelos monolíticos, este simulador implementa una arquitectura **Multicapa (Dual-Zone)**:

1.  **Capa Ablativa Exterior (Nodos 0-9):** Diseñada para disipar energía inicial.
    *   $\alpha = 0.005 \, m^2/s$ (Alta conductividad transitoria).
2.  **Aislante Térmico Avanzado (Nodos 10-19):** Núcleo de protección de la cabina.
    *   $\alpha = 0.0005 \, m^2/s$ (Baja difusividad para bloqueo térmico).

La interfaz en el **nodo 10** actúa como una barrera física donde se observa el cambio de gradiente térmico en tiempo real.

## 🏗️ Arquitectura del Flujo DataOps

El proyecto está orquestado por un pipeline de automatización que integra simulación física, post-procesamiento visual y auditoría inteligente:

1.  **Simulación Física (`escudo_multicapa.py`):** Motor de cálculo en Python puro que genera telemetría transitoria en formato CSV.
2.  **Visualización SciML (`animacion_multicapa.py`):** Generador de animaciones de alta fidelidad con estela termodinámica (colormap `inferno`), HUD dinámico y renderizado de ecuaciones en LaTeX.
3.  **Auditoría de Seguridad (Gemini CLI):** Agente de IA que analiza los datos de telemetría finales para emitir un veredicto de supervivencia basado en los límites vitales de la tripulación (< 40°C).

## 🚀 Ejecución en Linux

Asegúrate de tener instaladas las dependencias de visualización:
```bash
pip install matplotlib numpy pillow
```

Para lanzar el pipeline completo (Simulación + Animación + Reporte IA):
```bash
chmod +x pipeline_reentrada.sh
./pipeline_reentrada.sh
```

### Artefactos Generados:
*   `telemetria_multicapa.csv`: Datos brutos de la simulación.
*   `validacion_multicapa.gif`: Animación profesional del perfil térmico.
*   `reporte_supervivencia.md`: Informe técnico y veredicto final emitido por la IA.

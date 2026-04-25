#!/bin/bash

# Colores para la terminal
VERDE='\033[0;32m'
ROJO='\033[0;31m'
AZUL='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${AZUL}=== SISTEMA DE MONITOREO DE REENTRADA: ESCUDO MULTICAPA ===${NC}"

# PASO 1: Ejecutar la Simulación Numérica de la EDP
echo -e "\n[1/3] Lanzando motor físico FTCS..."
python3 escudo_multicapa.py

if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Telemetría generada con éxito.${NC}"
else
    echo -e "${ROJO}✘ Error en la simulación física.${NC}"
    exit 1
fi

# PASO 2: Generar la Visualización SciML
echo -e "\n[2/3] Renderizando animación de alta fidelidad..."
python3 animacion_multicapa.py

if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Animación 'validacion_multicapa.gif' lista.${NC}"
else
    echo -e "${ROJO}✘ Error en el renderizado visual.${NC}"
fi

# PASO 3: Auditoría de Seguridad con Gemini CLI
echo -e "\n[3/3] Iniciando auditoría con IA (Gemini Pro)..."

PROMPT="Actúa como un oficial de seguridad de la NASA. Analiza el archivo @telemetria_multicapa.csv adjunto. 
Concéntrate en la última columna (nodo de la cabina). 
1. ¿La temperatura en la cabina superó los 40°C en algún punto? 
2. Evalúa si el diseño multicapa (ablativo + aislante) fue efectivo.
3. Da un veredicto final: MISION SEGURA o MISION FALLIDA. 
Responde en formato Markdown técnico."

# Ejecutar Gemini CLI y guardar el reporte
gemini -p "$PROMPT" > reporte_supervivencia.md

if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Reporte 'reporte_supervivencia.md' generado.${NC}"
    echo -e "\n${AZUL}=== VEREDICTO DE LA IA ===${NC}"
    cat reporte_supervivencia.md
else
    echo -e "${ROJO}✘ Fallo en la conexión con Gemini CLI.${NC}"
fi

echo -e "\n${VERDE}Pipeline completado. Analiza los resultados antes de la próxima misión.${NC}"

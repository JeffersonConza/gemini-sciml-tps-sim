#!/bin/bash

# =============================================================================
# REENTRYFLOW ORCHESTRATOR - SCIENTIFIC DATAOPS PIPELINE
# =============================================================================

# Configuración de Colores
AZUL='\033[1;34m'
VERDE='\033[1;32m'
AMARILLO='\033[1;33m'
ROJO='\033[1;31m'
NC='\033[0m' # No Color

LOG_FILE="pipeline.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo -e "${AZUL}------------------------------------------------------------${NC}"
echo -e "${AZUL}    🛰️  SISTEMA DE CONTROL DE REENTRADA - NASA SciML v2.0    ${NC}"
echo -e "${AZUL}------------------------------------------------------------${NC}"

# --- 1. VERIFICACIÓN DE DEPENDENCIAS ---
echo -e "\n${AMARILLO}[1/5] Verificando entorno de ingeniería...${NC}"

check_dep() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${ROJO}✘ ERROR: $1 no está instalado.${NC}"
        exit 1
    fi
}

check_python_pkg() {
    python3 -c "import $1" &> /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${ROJO}✘ ERROR: Paquete Python '$1' no detectado.${NC}"
        exit 1
    fi
}

check_dep "python3"
check_dep "git"
check_python_pkg "matplotlib"
check_python_pkg "numpy"
check_python_pkg "scipy"

echo -e "${VERDE}✔ Entorno validado.${NC}"

# --- 2. LIMPIEZA DE ARTEFACTOS PREVIOS ---
if [[ "$*" == *"--clean"* ]]; then
    echo -e "\n${AMARILLO}[2/5] Limpiando datos antiguos...${NC}"
    rm -f *.csv *.log study_results/*.csv
    echo -e "${VERDE}✔ Workspace limpio.${NC}"
else
    echo -e "\n${AMARILLO}[2/5] Saltando limpieza (Usa --clean para purgar).${NC}"
fi

# --- 3. EJECUCIÓN DEL MOTOR FÍSICO ---
echo -e "\n${AMARILLO}[3/5] Lanzando Simulación de Diferencias Finitas...${NC}"
python3 escudo_multicapa.py
if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Simulación exitosa. Telemetría lista.${NC}"
else
    echo -e "${ROJO}✘ Fallo crítico en el motor físico.${NC}"
    exit 1
fi

# --- 4. RENDERIZADO DE ALTA FIDELIDAD ---
echo -e "\n${AMARILLO}[4/5] Generando Visualización SciML...${NC}"
python3 animacion_multicapa.py
if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Animación 'validacion_multicapa.gif' generada.${NC}"
else
    echo -e "${AMARILLO}⚠ Aviso: Error en el renderizado, continuando...${NC}"
fi

# --- 5. AUDITORÍA DE SEGURIDAD CON IA ---
if [[ "$*" == *"--skip-ia"* ]]; then
    echo -e "\n${AMARILLO}[5/5] IA Audit saltada por el usuario.${NC}"
else
    echo -e "\n${AMARILLO}[5/5] Consultando Auditoría de Seguridad a la IA...${NC}"
    if command -v gemini &> /dev/null; then
        PROMPT="Analiza telemetria_multicapa.csv. El nodo final es la cabina. Veredicto de supervivencia (umbral 40C). Markdown."
        gemini -p "$PROMPT" > reporte_supervivencia.md
        echo -e "${VERDE}✔ Veredicto recibido.${NC}"
        echo -e "${AZUL}--- RESUMEN DE LA IA ---${NC}"
        head -n 5 reporte_supervivencia.md
    else
        echo -e "${AMARILLO}⚠ Gemini CLI no detectado. Saltando paso de IA.${NC}"
    fi
fi

echo -e "\n${VERDE}============================================================${NC}"
echo -e "${VERDE}    🚀 PIPELINE COMPLETADO EXITOSAMENTE${NC}"
echo -e "${VERDE}============================================================${NC}\n"

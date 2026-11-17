#!/usr/bin/env bash
# Script para iniciar PyBioLearn
cd "$(dirname "$0")"

echo "🧬 Preparando PyBioLearn..."

# 1. Verificar si el entorno virtual existente funciona
VENV_OK=0
if [ -f "venv/bin/streamlit" ]; then
    if ./venv/bin/python3 -c "import streamlit, Bio" >/dev/null 2>&1; then
        VENV_OK=1
    fi
fi

# 2. Si venv no es válido (por ejemplo, copiado de otro equipo/ruta), recrearlo
if [ $VENV_OK -eq 0 ]; then
    if [ -d "venv" ]; then
        echo "⚠️  Detectado entorno 'venv' no válido (copiado de otro equipo o ruta anterior). Recreando..."
        rm -rf venv
    fi

    # Determinar qué python3 usar
    PYTHON_CMD=""
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    fi

    if [ -z "$PYTHON_CMD" ]; then
        echo "❌ No se encontró Python 3 instalado en tu sistema."
        echo "Por favor, instala Python 3 (3.10 o superior) y vuelve a intentarlo."
        exit 1
    fi

    echo "📦 Creando nuevo entorno virtual con $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv
    
    echo "⬇️  Instalando dependencias desde requirements.txt (Streamlit, Biopython, Pandas, Matplotlib)..."
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
fi

echo "🚀 Iniciando PyBioLearn en el navegador..."
./venv/bin/streamlit run app.py

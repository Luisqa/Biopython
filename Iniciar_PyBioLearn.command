#!/usr/bin/env bash
# Acceso directo para iniciar PyBioLearn con doble clic en macOS

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="/Users/imac/Downloads/agente python copia"

if [ -f "$DIR/app.py" ]; then
    cd "$DIR"
elif [ -f "$PROJECT_DIR/app.py" ]; then
    cd "$PROJECT_DIR"
else
    echo "❌ No se encontró la carpeta del proyecto PyBioLearn."
    read -p "Presiona Enter para salir..."
    exit 1
fi

./run_app.sh


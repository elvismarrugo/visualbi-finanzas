#!/bin/bash
# Script para instalar las dependencias del backend

echo "🔧 Instalando dependencias del backend de Siigo App..."

# Verificar si python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 no está instalado"
    exit 1
fi

# Intentar instalar pip si no está disponible
if ! python3 -m pip --version &> /dev/null; then
    echo "⚠️  pip no está disponible. Intentando instalar..."
    echo "Por favor ejecuta: sudo apt install python3-pip"
    exit 1
fi

# Instalar dependencias
echo "📦 Instalando paquetes de Python..."
python3 -m pip install --user fastapi 'uvicorn[standard]' python-dotenv httpx pydantic pydantic-settings python-multipart

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas correctamente"
    echo ""
    echo "Para iniciar el backend, ejecuta:"
    echo "  cd backend"
    echo "  python3 main.py"
else
    echo "❌ Error al instalar dependencias"
    exit 1
fi


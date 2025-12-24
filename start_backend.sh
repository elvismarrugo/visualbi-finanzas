#!/bin/bash
# Script para iniciar el backend de Siigo App

echo "🚀 Iniciando Backend de Siigo App..."
echo ""

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar si estamos en el directorio correcto
if [ ! -f "backend/main.py" ]; then
    echo -e "${RED}❌ Error: Este script debe ejecutarse desde la raíz del proyecto${NC}"
    exit 1
fi

cd backend

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: python3 no está instalado${NC}"
    exit 1
fi

# Verificar si las dependencias están instaladas
echo "🔍 Verificando dependencias..."
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Las dependencias de Python no están instaladas${NC}"
    echo ""
    echo "Por favor ejecuta primero:"
    echo "  sudo apt install -y python3-pip"
    echo "  pip3 install fastapi 'uvicorn[standard]' python-dotenv httpx pydantic pydantic-settings python-multipart"
    echo ""
    echo "O si prefieres usar un entorno virtual:"
    echo "  sudo apt install -y python3-pip python3-venv"
    echo "  cd backend"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Verificar que el archivo .env existe
if [ ! -f "../.env" ]; then
    echo -e "${YELLOW}⚠️  Advertencia: El archivo .env no existe${NC}"
    echo "Asegúrate de tener configuradas las credenciales de Siigo"
fi

echo -e "${GREEN}✅ Todas las dependencias están instaladas${NC}"
echo ""
echo "🌐 Iniciando servidor backend en http://localhost:8000"
echo "📚 Documentación disponible en http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar el servidor
python3 main.py


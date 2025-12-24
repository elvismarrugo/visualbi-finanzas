#!/bin/bash
# Script para configurar SQLite temporalmente (no requiere instalación)
# Esto permite probar el sistema mientras se configura PostgreSQL

echo "🔧 Configurando SQLite temporal para pruebas..."
echo ""

cd "$(dirname "$0")/backend"
source venv/bin/activate

echo "📊 Inicializando base de datos SQLite..."
python init_db.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SQLite configurado exitosamente"
    echo ""
    echo "📁 Archivo de base de datos: $(pwd)/../siigo_data.db"
    echo ""
    echo "⚠️  NOTA: Esto es temporal. Para producción, configura PostgreSQL:"
    echo "   bash instalar_postgresql.sh"
    echo ""
    echo "🚀 Ahora puedes iniciar el backend:"
    echo "   cd backend && source venv/bin/activate && python main.py"
else
    echo "❌ Error al configurar SQLite"
    exit 1
fi


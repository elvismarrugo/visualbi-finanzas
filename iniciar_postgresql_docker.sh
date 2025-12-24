#!/bin/bash
# Script para iniciar PostgreSQL con Docker (no requiere sudo para docker)
# Ejecutar con: bash iniciar_postgresql_docker.sh

echo "🐳 Iniciando PostgreSQL con Docker..."
echo ""

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    echo "Instala Docker con: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
    exit 1
fi

# Verificar si docker-compose está disponible
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ docker-compose no está disponible"
    exit 1
fi

# Iniciar PostgreSQL
echo "🚀 Iniciando contenedor de PostgreSQL..."
cd "$(dirname "$0")"
$COMPOSE_CMD up -d postgres

if [ $? -eq 0 ]; then
    echo "✅ PostgreSQL iniciado en Docker"
    echo ""
    echo "⏳ Esperando que PostgreSQL esté listo..."
    sleep 5
    
    # Esperar a que PostgreSQL esté listo
    for i in {1..30}; do
        if docker exec siigo_postgres pg_isready -U siigo_user -d siigo_db &> /dev/null; then
            echo "✅ PostgreSQL está listo!"
            break
        fi
        echo "   Esperando... ($i/30)"
        sleep 2
    done
    
    # Inicializar tablas
    echo ""
    echo "📊 Inicializando tablas..."
    cd backend
    source venv/bin/activate
    python init_db.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Tablas inicializadas"
    else
        echo "⚠️  Error al inicializar tablas (puede que PostgreSQL aún no esté listo)"
    fi
    
    echo ""
    echo "🎉 PostgreSQL está corriendo en Docker!"
    echo ""
    echo "Para detener: docker-compose down"
    echo "Para ver logs: docker-compose logs -f postgres"
else
    echo "❌ Error al iniciar PostgreSQL"
    exit 1
fi


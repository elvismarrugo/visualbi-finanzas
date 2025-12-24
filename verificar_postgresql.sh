#!/bin/bash
# Script para verificar el estado de PostgreSQL
# Ejecutar con: bash verificar_postgresql.sh

echo "🔍 Verificando estado de PostgreSQL..."
echo ""

# Verificar si PostgreSQL está instalado
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL está instalado"
    PSQL_VERSION=$(psql --version | head -1)
    echo "   Versión: $PSQL_VERSION"
else
    echo "❌ PostgreSQL NO está instalado"
    echo "   Ejecuta: bash instalar_postgresql.sh"
    exit 1
fi

echo ""

# Verificar si el servicio está corriendo
if systemctl is-active --quiet postgresql 2>/dev/null || pg_isready -h localhost -p 5432 &>/dev/null; then
    echo "✅ PostgreSQL está corriendo"
    
    # Intentar conectar
    echo ""
    echo "🔌 Verificando conexión..."
    cd "$(dirname "$0")/backend"
    source venv/bin/activate
    
    python3 << 'PYTHON_EOF'
try:
    from database import get_db_engine
    engine = get_db_engine()
    with engine.connect() as conn:
        result = conn.execute("SELECT version();")
        version = result.fetchone()[0]
        print(f"✅ Conexión exitosa")
        print(f"   {version[:50]}...")
        
        # Verificar si las tablas existen
        from database import Base
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if 'balance_reports' in tables:
            print(f"✅ Tabla 'balance_reports' existe")
            
            # Contar registros
            result = conn.execute("SELECT COUNT(*) FROM balance_reports;")
            count = result.fetchone()[0]
            print(f"   Registros: {count}")
        else:
            print("⚠️  Tabla 'balance_reports' NO existe")
            print("   Ejecuta: python init_db.py")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("   Verifica las credenciales en .env")
PYTHON_EOF

else
    echo "❌ PostgreSQL NO está corriendo"
    echo ""
    echo "Para iniciarlo:"
    echo "  sudo systemctl start postgresql"
    echo "  sudo systemctl enable postgresql"
    echo ""
    echo "O usa Docker:"
    echo "  bash iniciar_postgresql_docker.sh"
fi

echo ""
echo "📋 Variables de entorno configuradas:"
cd "$(dirname "$0")"
if [ -f .env ]; then
    grep -E "^DB_|^POSTGRES" .env | sed 's/=.*/=***/' || echo "  (no encontradas)"
else
    echo "  ⚠️  .env no existe"
fi


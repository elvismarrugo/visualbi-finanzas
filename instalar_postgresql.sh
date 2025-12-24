#!/bin/bash
# Script para instalar y configurar PostgreSQL
# Ejecutar con: bash instalar_postgresql.sh

echo "🚀 Instalando y configurando PostgreSQL..."
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paso 1: Instalar PostgreSQL
echo "📦 Paso 1: Instalando PostgreSQL..."
sudo apt update
sudo apt install -y postgresql postgresql-contrib

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PostgreSQL instalado${NC}"
else
    echo -e "${YELLOW}⚠️  Error al instalar PostgreSQL${NC}"
    exit 1
fi

# Paso 2: Iniciar PostgreSQL
echo ""
echo "🔄 Paso 2: Iniciando PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PostgreSQL iniciado${NC}"
else
    echo -e "${YELLOW}⚠️  Error al iniciar PostgreSQL${NC}"
    exit 1
fi

# Paso 3: Crear base de datos y usuario
echo ""
echo "🗄️  Paso 3: Creando base de datos y usuario..."

sudo -u postgres psql << 'EOF'
-- Crear base de datos si no existe
SELECT 'CREATE DATABASE siigo_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'siigo_db')\gexec

-- Crear usuario si no existe
DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'siigo_user') THEN
      CREATE USER siigo_user WITH PASSWORD 'siigo_password';
   END IF;
END
\$\$;

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE siigo_db TO siigo_user;

-- Conectar a la base de datos y dar permisos en el schema
\c siigo_db
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO siigo_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO siigo_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO siigo_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO siigo_user;

\q
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de datos y usuario creados${NC}"
else
    echo -e "${YELLOW}⚠️  Error al crear base de datos${NC}"
    exit 1
fi

# Paso 4: Inicializar tablas
echo ""
echo "📊 Paso 4: Inicializando tablas..."

cd "$(dirname "$0")/backend"
source venv/bin/activate
python init_db.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Tablas inicializadas${NC}"
else
    echo -e "${YELLOW}⚠️  Error al inicializar tablas${NC}"
    exit 1
fi

# Paso 5: Verificar
echo ""
echo "🔍 Paso 5: Verificando configuración..."

sudo -u postgres psql -d siigo_db -c "\dt" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de datos verificada${NC}"
    echo ""
    echo "📋 Tablas creadas:"
    sudo -u postgres psql -d siigo_db -c "\dt"
else
    echo -e "${YELLOW}⚠️  Error al verificar${NC}"
fi

echo ""
echo -e "${GREEN}🎉 PostgreSQL configurado correctamente!${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Reinicia el backend: cd backend && source venv/bin/activate && python main.py"
echo "2. Procesa datos: POST http://localhost:8000/api/etl/process-year"
echo "3. Consulta datos: GET http://localhost:8000/api/powerbi/balance-reports"


# 🗄️ Soluciones para Configurar PostgreSQL

Tienes **3 opciones** para configurar PostgreSQL. Elige la que prefieras:

## 🎯 Opción 1: Script Automatizado (Recomendado - Más Fácil)

Ejecuta este comando (necesitarás tu contraseña de sudo):

```bash
cd /home/elvix/siigo-app
bash instalar_postgresql.sh
```

Este script hace todo automáticamente.

---

## 🐳 Opción 2: Docker (No Requiere sudo para Docker)

Si tienes Docker instalado y tu usuario tiene permisos:

```bash
cd /home/elvix/siigo-app
bash iniciar_postgresql_docker.sh
```

O manualmente:

```bash
cd /home/elvix/siigo-app
docker-compose up -d postgres

# Esperar unos segundos
sleep 5

# Inicializar tablas
cd backend
source venv/bin/activate
python init_db.py
```

**Ventajas:**
- No requiere sudo (si Docker está configurado)
- Fácil de iniciar/detener
- Aislado del sistema

---

## 📝 Opción 3: Manual (Paso a Paso)

### 1. Instalar PostgreSQL

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Crear Base de Datos

```bash
sudo -u postgres psql
```

Dentro de PostgreSQL:

```sql
CREATE DATABASE siigo_db;
CREATE USER siigo_user WITH PASSWORD 'siigo_password';
GRANT ALL PRIVILEGES ON DATABASE siigo_db TO siigo_user;
\c siigo_db
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO siigo_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO siigo_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO siigo_user;
\q
```

### 3. Inicializar Tablas

```bash
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python init_db.py
```

### 4. Reiniciar Backend

```bash
# Detén el backend actual (Ctrl+C)
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

---

## ✅ Verificación

Después de cualquier opción, verifica:

```bash
# Verificar que PostgreSQL está corriendo
sudo systemctl status postgresql  # Para instalación normal
# O
docker ps | grep postgres  # Para Docker

# Verificar conexión
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python -c "from database import init_db; init_db(); print('✅ Conexión exitosa')"
```

---

## 🚀 Una Vez Configurado

### Procesar Datos:

1. Abre: `http://localhost:8000/docs`
2. Busca: `POST /api/etl/process-year`
3. Ejecuta con:
```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 12,
  "includes_tax_diff": false,
  "clear_existing": true
}
```

### Ver Datos:

```bash
# Desde PostgreSQL
sudo -u postgres psql -d siigo_db -c "SELECT COUNT(*) FROM balance_reports;"

# Desde API
curl http://localhost:8000/api/powerbi/stats
```

---

## 🆘 Solución de Problemas

### Error: "connection refused"
- Verifica que PostgreSQL esté corriendo
- Verifica las credenciales en `.env`

### Error: "permission denied"
- Verifica los permisos del usuario en PostgreSQL
- Ejecuta los comandos GRANT nuevamente

### Error: "database does not exist"
- Crea la base de datos manualmente
- Verifica el nombre en `.env`

---

## 📋 Resumen de Archivos

- `instalar_postgresql.sh` - Instalación automática (requiere sudo)
- `iniciar_postgresql_docker.sh` - Inicio con Docker
- `docker-compose.yml` - Configuración de Docker
- `INSTRUCCIONES_COMPLETAS.md` - Guía detallada

**Recomendación:** Empieza con la Opción 1 (script automatizado) si puedes usar sudo.


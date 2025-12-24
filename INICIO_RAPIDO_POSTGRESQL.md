# 🚀 Inicio Rápido: Configurar PostgreSQL

## ✅ Estado Actual

- ✅ Código ETL implementado
- ✅ Modelo de base de datos creado
- ✅ Variables de entorno configuradas en `.env`
- ❌ PostgreSQL no está corriendo

## 🎯 Solución en 3 Pasos

### Paso 1: Instalar/Iniciar PostgreSQL

**Opción A - Script Automatizado (Recomendado):**
```bash
cd /home/elvix/siigo-app
bash instalar_postgresql.sh
```

**Opción B - Docker (Si tienes Docker):**
```bash
cd /home/elvix/siigo-app
bash iniciar_postgresql_docker.sh
```

**Opción C - Manual:**
```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear base de datos
sudo -u postgres psql << 'EOF'
CREATE DATABASE siigo_db;
CREATE USER siigo_user WITH PASSWORD 'siigo_password';
GRANT ALL PRIVILEGES ON DATABASE siigo_db TO siigo_user;
\c siigo_db
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO siigo_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO siigo_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO siigo_user;
\q
EOF
```

### Paso 2: Inicializar Tablas

```bash
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python init_db.py
```

Deberías ver: `✅ Tablas creadas exitosamente`

### Paso 3: Reiniciar Backend

```bash
# Detén el backend actual (Ctrl+C si está corriendo)
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

Deberías ver: `✅ Base de datos inicializada`

---

## ✅ Verificar que Todo Funciona

```bash
cd /home/elvix/siigo-app
bash verificar_postgresql.sh
```

---

## 🎉 Procesar Datos

Una vez que PostgreSQL esté corriendo:

1. **Abre Swagger UI:**
   ```
   http://localhost:8000/docs
   ```

2. **Busca el endpoint:**
   ```
   POST /api/etl/process-year
   ```

3. **Ejecuta con estos parámetros:**
   ```json
   {
     "year": 2024,
     "month_start": 1,
     "month_end": 12,
     "includes_tax_diff": false,
     "clear_existing": true
   }
   ```

4. **El sistema automáticamente:**
   - ✅ Obtiene token de Siigo
   - ✅ Descarga Excel de cada mes
   - ✅ Procesa y transforma los datos
   - ✅ Guarda todo en PostgreSQL

---

## 📊 Ver los Datos

### Desde la API:

```bash
# Estadísticas
curl http://localhost:8000/api/powerbi/stats

# Datos completos
curl "http://localhost:8000/api/powerbi/balance-reports?year=2024&month=1"
```

### Desde PostgreSQL:

```bash
sudo -u postgres psql -d siigo_db -c "SELECT COUNT(*) FROM balance_reports;"
sudo -u postgres psql -d siigo_db -c "SELECT * FROM balance_reports LIMIT 5;"
```

---

## 🆘 Problemas Comunes

### Error: "Connection refused"
- PostgreSQL no está corriendo
- Solución: `sudo systemctl start postgresql`

### Error: "database does not exist"
- La base de datos no fue creada
- Solución: Ejecuta los comandos CREATE DATABASE del Paso 1

### Error: "permission denied"
- El usuario no tiene permisos
- Solución: Ejecuta los comandos GRANT del Paso 1

---

## 📚 Más Información

- `SOLUCION_POSTGRESQL.md` - Todas las opciones disponibles
- `INSTRUCCIONES_COMPLETAS.md` - Guía detallada paso a paso
- `README_ETL.md` - Documentación del sistema ETL


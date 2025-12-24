# 🚀 Instrucciones Completas: Configurar Todo el Sistema

## ✅ Lo que Necesitas Hacer

Como no puedo ejecutar comandos con `sudo` (requiere tu contraseña), aquí están los pasos que debes ejecutar manualmente:

## 📋 Pasos a Seguir

### Paso 1: Instalar PostgreSQL

Ejecuta este comando en tu terminal:

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Paso 2: Crear Base de Datos

Ejecuta estos comandos:

```bash
sudo -u postgres psql
```

Dentro de PostgreSQL, ejecuta:

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

### Paso 3: Inicializar Tablas

```bash
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python init_db.py
```

Deberías ver: `✅ Base de datos inicializada correctamente`

### Paso 4: Reiniciar Backend

```bash
# Detén el backend actual (Ctrl+C)
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

### Paso 5: Procesar Datos

Abre en tu navegador: `http://localhost:8000/docs`

Busca el endpoint: `POST /api/etl/process-year`

Ejecuta con este JSON:
```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 12,
  "includes_tax_diff": false,
  "clear_existing": true
}
```

## 🎯 Script Automatizado

He creado un script que hace todo automáticamente. Ejecuta:

```bash
cd /home/elvix/siigo-app
bash instalar_postgresql.sh
```

Este script:
- ✅ Instala PostgreSQL
- ✅ Crea la base de datos
- ✅ Crea el usuario
- ✅ Inicializa las tablas
- ✅ Verifica que todo funcione

## ✅ Verificación

Después de ejecutar los pasos, verifica:

```bash
# Verificar que PostgreSQL está corriendo
sudo systemctl status postgresql

# Verificar que la base de datos existe
sudo -u postgres psql -l | grep siigo_db

# Verificar que las tablas están creadas
sudo -u postgres psql -d siigo_db -c "\dt"
```

## 🎉 Una Vez Configurado

Podrás:
- ✅ Procesar todos los periodos automáticamente
- ✅ Ver datos en PostgreSQL
- ✅ Consultar desde Power BI
- ✅ Hacer análisis históricos

## 📝 Resumen

1. **Ejecuta:** `bash instalar_postgresql.sh`
2. **O sigue los pasos manualmente** arriba
3. **Reinicia el backend**
4. **Procesa datos** desde Swagger UI

¡Todo está listo para funcionar! 🚀


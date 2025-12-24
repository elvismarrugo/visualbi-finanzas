# 🗄️ Configurar PostgreSQL para Guardar Datos de Excel

## ✅ Buenas Noticias

El sistema **YA está implementado** para guardar todos los datos de Excel en PostgreSQL. Solo necesitas configurar la base de datos.

## 🚀 Pasos para Configurar

### Paso 1: Instalar PostgreSQL

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Paso 2: Crear Base de Datos y Usuario

```bash
# Entrar a PostgreSQL como superusuario
sudo -u postgres psql

# Dentro de PostgreSQL, ejecuta:
CREATE DATABASE siigo_db;
CREATE USER siigo_user WITH PASSWORD 'tu_password_segura';
GRANT ALL PRIVILEGES ON DATABASE siigo_db TO siigo_user;
\q
```

**Nota:** Cambia `tu_password_segura` por una contraseña segura.

### Paso 3: Configurar Variables de Entorno

Edita el archivo `.env` en la raíz del proyecto y agrega:

```env
# Configuración de PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=siigo_db
DB_USER=siigo_user
DB_PASSWORD=tu_password_segura
```

**Ejemplo completo del .env:**
```env
# Credenciales de Siigo API
SIIGO_ACCESS_KEY=OTc3YjU3YTYtOGY2Ni00ZDMxLWE4NTEtOGY5Y2VhMjJhZDMwOn5iYTg4fnE4MUI=
SIIGO_PARTNER_ID=SiigoApiCoomulgar
SIIGO_BASE_URL=https://api.siigo.com
SIIGO_USERNAME=coomulgar@hotmail.com
BACKEND_PORT=8000

# Configuración de PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=siigo_db
DB_USER=siigo_user
DB_PASSWORD=tu_password_segura
```

### Paso 4: Inicializar la Base de Datos

```bash
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python init_db.py
```

Deberías ver: `✅ Base de datos inicializada correctamente`

### Paso 5: Reiniciar el Backend

```bash
# Detén el backend actual (Ctrl+C)
# Luego reinícialo:
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

## 📊 Cómo Usar el Sistema ETL

### Opción 1: Desde Swagger UI (Recomendado)

1. Abre: `http://localhost:8000/docs`
2. Busca el endpoint: `POST /api/etl/process-year`
3. Haz clic en "Try it out"
4. Completa el JSON:
```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 12,
  "includes_tax_diff": false,
  "clear_existing": true
}
```
5. Haz clic en "Execute"
6. El sistema descargará y procesará todos los meses automáticamente

### Opción 2: Desde la Terminal (curl)

```bash
curl -X POST http://localhost:8000/api/etl/process-year \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2024,
    "month_start": 1,
    "month_end": 12,
    "includes_tax_diff": false,
    "clear_existing": true
  }'
```

### Opción 3: Desde Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/etl/process-year",
    json={
        "year": 2024,
        "month_start": 1,
        "month_end": 12,
        "includes_tax_diff": False,
        "clear_existing": True
    }
)

print(response.json())
```

## 🔍 Qué Hace el Sistema

1. **Obtiene token de Siigo** (una sola vez)
2. **Para cada mes** (1-12):
   - Solicita reporte a Siigo
   - Descarga el archivo Excel
   - Procesa el Excel:
     - Detecta encabezados
     - Filtra por Transaccional = "Sí"
     - Calcula campos (Movimiento, Cod Relacional, Periodo, Fecha)
     - Normaliza tipos de datos
   - **Guarda en PostgreSQL** (tabla `balance_reports`)
3. **Retorna estadísticas** del procesamiento

## 📋 Estructura de la Tabla

La tabla `balance_reports` contiene:

- **Datos de cuenta:** código, nombre, código relacional
- **Datos de tercero:** identificación, sucursal, nombre
- **Valores contables:** saldo inicial, débito, crédito, movimiento, saldo final
- **Dimensiones temporales:** fecha, año, periodo (AAAAMM)
- **Metadatos:** created_at, updated_at

## ✅ Verificar que los Datos se Guardaron

### Desde PostgreSQL:

```bash
sudo -u postgres psql -d siigo_db

# Contar registros
SELECT COUNT(*) FROM balance_reports;

# Ver algunos registros
SELECT * FROM balance_reports LIMIT 10;

# Ver por año
SELECT año, COUNT(*) FROM balance_reports GROUP BY año;

# Ver por periodo
SELECT periodo, COUNT(*) FROM balance_reports GROUP BY periodo ORDER BY periodo;
```

### Desde la API:

```bash
# Ver estadísticas
curl http://localhost:8000/api/powerbi/stats

# Ver datos
curl "http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=10"
```

## 🎯 Procesar Múltiples Años

### Año Actual:
```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 12
}
```

### Año Anterior:
```json
{
  "year_base": 2024
}
```
(Esto procesará el año 2023 completo)

## ⚠️ Notas Importantes

1. **El procesamiento puede tardar** varios minutos dependiendo de los meses
2. **Los datos se procesan mes por mes** (como en PowerQuery)
3. **Si `clear_existing: true`**, se eliminan datos existentes del mismo año antes de insertar
4. **El token se reutiliza** para todas las peticiones del mismo proceso

## 🆘 Solución de Problemas

### Error: "connection refused"
- Verifica que PostgreSQL esté corriendo: `sudo systemctl status postgresql`
- Verifica las credenciales en `.env`

### Error: "database does not exist"
- Crea la base de datos: `CREATE DATABASE siigo_db;`

### Error: "permission denied"
- Verifica los permisos del usuario: `GRANT ALL PRIVILEGES ON DATABASE siigo_db TO siigo_user;`

## 🎉 Una Vez Configurado

Podrás:
- ✅ Procesar todos los meses de un año automáticamente
- ✅ Ver todos los datos en PostgreSQL
- ✅ Consultar desde Power BI usando la API
- ✅ Hacer análisis históricos de múltiples años


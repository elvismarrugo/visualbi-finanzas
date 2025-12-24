# 🗄️ Guía Completa: Guardar Datos de Excel en PostgreSQL

## ✅ Lo que Ya Está Implementado

El sistema **YA está listo** para:
- ✅ Descargar Excel de todos los periodos de Siigo
- ✅ Procesar cada archivo Excel con transformaciones ETL
- ✅ Guardar todos los datos en PostgreSQL automáticamente
- ✅ Consultar los datos desde Power BI

## 🚀 Configuración Paso a Paso

### Paso 1: Instalar PostgreSQL

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Paso 2: Crear Base de Datos

```bash
# Entrar a PostgreSQL
sudo -u postgres psql

# Ejecutar estos comandos dentro de PostgreSQL:
CREATE DATABASE siigo_db;
CREATE USER siigo_user WITH PASSWORD 'siigo_password_123';
GRANT ALL PRIVILEGES ON DATABASE siigo_db TO siigo_user;
\q
```

**⚠️ Importante:** Cambia `siigo_password_123` por una contraseña segura.

### Paso 3: Verificar Variables en .env

El archivo `.env` ya tiene las variables de PostgreSQL. Verifica que sean correctas:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=siigo_db
DB_USER=siigo_user
DB_PASSWORD=siigo_password_123
```

**Cambia la contraseña** si usaste una diferente en el Paso 2.

### Paso 4: Inicializar la Base de Datos

```bash
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python init_db.py
```

Deberías ver: `✅ Base de datos inicializada correctamente`

### Paso 5: Reiniciar el Backend

```bash
# Detén el backend actual (Ctrl+C si está corriendo)
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

## 📊 Cómo Procesar y Guardar Todos los Periodos

### Método 1: Desde Swagger UI (Más Fácil)

1. Abre: `http://localhost:8000/docs`
2. Busca: `POST /api/etl/process-year`
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
6. **El sistema automáticamente:**
   - Descargará Excel de cada mes (1-12)
   - Procesará cada archivo
   - Guardará todos los datos en PostgreSQL

### Método 2: Desde Terminal

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

### Respuesta Esperada:

```json
{
  "year": 2024,
  "months_processed": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  "total_rows": 15000,
  "errors": [],
  "success": true
}
```

## 🔍 Verificar que los Datos se Guardaron

### Opción 1: Desde PostgreSQL

```bash
sudo -u postgres psql -d siigo_db

# Ver cuántos registros hay
SELECT COUNT(*) FROM balance_reports;

# Ver algunos registros
SELECT * FROM balance_reports LIMIT 10;

# Ver por año
SELECT año, COUNT(*) as registros 
FROM balance_reports 
GROUP BY año 
ORDER BY año;

# Ver por periodo
SELECT periodo, COUNT(*) as registros 
FROM balance_reports 
GROUP BY periodo 
ORDER BY periodo;
```

### Opción 2: Desde la API

```bash
# Ver estadísticas
curl http://localhost:8000/api/powerbi/stats

# Ver datos (primeros 10 registros)
curl "http://localhost:8000/api/powerbi/balance-reports?limit=10"

# Ver datos de un año específico
curl "http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=100"
```

## 📋 Qué Datos se Guardan

Cada registro en PostgreSQL contiene:

| Campo | Descripción |
|-------|-------------|
| `codigo_cuenta_contable` | Código de la cuenta |
| `nombre_cuenta_contable` | Nombre de la cuenta |
| `cod_relacional` | Primeros 6 caracteres del código |
| `identificacion` | ID del tercero |
| `sucursal` | Sucursal |
| `nombre_tercero` | Nombre del tercero |
| `saldo_inicial` | Saldo inicial del periodo |
| `movimiento_debito` | Movimientos débito |
| `movimiento_credito` | Movimientos crédito |
| `movimiento` | Débito - Crédito |
| `saldo_final` | Saldo final |
| `fecha` | Fecha del reporte (último día del mes) |
| `año` | Año del reporte |
| `periodo` | Periodo en formato AAAAMM (ej: 202401) |

## 🎯 Procesar Múltiples Años

### Procesar Año 2024:
```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 12
}
```

### Procesar Año 2023:
```json
{
  "year": 2023,
  "month_start": 1,
  "month_end": 12
}
```

### Procesar Año Anterior Automáticamente:
```json
{
  "year_base": 2024
}
```
(Esto procesará el año 2023 completo)

## ⚡ Procesamiento Automático

El sistema procesa **mes por mes automáticamente**:

1. **Mes 1:** Descarga Excel → Procesa → Guarda en PostgreSQL
2. **Mes 2:** Descarga Excel → Procesa → Guarda en PostgreSQL
3. **Mes 3:** Descarga Excel → Procesa → Guarda en PostgreSQL
4. ... y así hasta el mes 12

**Todo en una sola petición!** 🚀

## 🔗 Consultar desde Power BI

Una vez que los datos estén en PostgreSQL:

1. Abre Power BI Desktop
2. Obtener datos > Web
3. URL: `http://localhost:8000/api/powerbi/balance-reports`
4. Agregar parámetros según necesites:
   - `?año=2024` - Filtrar por año
   - `&limit=10000` - Límite de registros
   - `&periodo=202401` - Filtrar por periodo específico

## ✅ Checklist de Configuración

- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `siigo_db` creada
- [ ] Usuario `siigo_user` creado con permisos
- [ ] Variables de PostgreSQL en `.env` configuradas
- [ ] Base de datos inicializada (`python init_db.py`)
- [ ] Backend reiniciado
- [ ] Procesamiento ETL ejecutado exitosamente
- [ ] Datos verificados en PostgreSQL

## 🆘 Solución de Problemas

### Error: "connection refused"
```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql

# Si no está corriendo:
sudo systemctl start postgresql
```

### Error: "database does not exist"
```bash
sudo -u postgres psql
CREATE DATABASE siigo_db;
```

### Error: "permission denied"
```bash
sudo -u postgres psql -d siigo_db
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO siigo_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO siigo_user;
```

## 🎉 Resultado Final

Una vez configurado, tendrás:
- ✅ Todos los datos de Excel guardados en PostgreSQL
- ✅ Consultas rápidas desde Power BI
- ✅ Análisis históricos de múltiples años
- ✅ Datos estructurados y normalizados


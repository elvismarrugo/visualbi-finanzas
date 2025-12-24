# 📊 Sistema ETL para Siigo - Documentación

## 🎯 Descripción

Este sistema replica la lógica de PowerQuery para:
1. Descargar reportes de Siigo mes por mes
2. Procesar archivos Excel con transformaciones ETL
3. Guardar datos en PostgreSQL
4. Exponer API para Power BI

## 🏗️ Arquitectura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   Siigo     │ --> │  ETL Service │ --> │ PostgreSQL  │ <-- │  Power BI   │
│    API      │     │  (Backend)   │     │  Database   │     │     API     │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
```

## 📋 Componentes

### 1. `database.py`
- Modelo de datos `BalanceReport`
- Configuración de conexión PostgreSQL
- Funciones para inicializar BD

### 2. `excel_processor.py`
- Descarga archivos Excel desde URLs de Siigo
- Procesa Excel con lógica ETL:
  - Detecta fila de encabezados
  - Filtra por Transaccional = "Sí"
  - Calcula campos derivados (Movimiento, Cod Relacional, Periodo)
  - Normaliza tipos de datos

### 3. `etl_service.py`
- Procesa reportes mes por mes
- Maneja año actual y año anterior
- Guarda datos en PostgreSQL

### 4. Endpoints API (`main.py`)
- `/api/etl/process-year` - Procesa año actual
- `/api/etl/process-previous-year` - Procesa año anterior
- `/api/powerbi/balance-reports` - Consulta datos para Power BI
- `/api/powerbi/stats` - Estadísticas agregadas

## 🚀 Configuración

### 1. Instalar PostgreSQL

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Crear Base de Datos

```bash
sudo -u postgres psql
CREATE DATABASE siigo_db;
CREATE USER siigo_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE siigo_db TO siigo_user;
\q
```

### 3. Configurar Variables de Entorno

Agregar al archivo `.env`:

```env
# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=siigo_db
DB_USER=siigo_user
DB_PASSWORD=tu_password
```

### 4. Instalar Dependencias

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Inicializar Base de Datos

```bash
python init_db.py
```

## 📝 Uso

### Procesar Año Actual

```bash
POST /api/etl/process-year
{
  "year": 2024,
  "month_start": 1,
  "month_end": 12,
  "includes_tax_diff": false,
  "clear_existing": true
}
```

### Procesar Año Anterior

```bash
POST /api/etl/process-previous-year
{
  "year_base": 2024,
  "includes_tax_diff": false,
  "clear_existing": true
}
```

### Consultar Datos para Power BI

```bash
GET /api/powerbi/balance-reports?año=2024&limit=1000&offset=0
```

## 🔍 Estructura de Datos

### Tabla: `balance_reports`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID único |
| codigo_cuenta_contable | Integer | Código de cuenta |
| nombre_cuenta_contable | Text | Nombre de cuenta |
| cod_relacional | String(10) | Primeros 6 caracteres del código |
| identificacion | String(50) | ID del tercero |
| sucursal | String(100) | Sucursal |
| nombre_tercero | Text | Nombre del tercero |
| saldo_inicial | Numeric(18,2) | Saldo inicial |
| movimiento_debito | Numeric(18,2) | Movimiento débito |
| movimiento_credito | Numeric(18,2) | Movimiento crédito |
| movimiento | Numeric(18,2) | Débito - Crédito |
| saldo_final | Numeric(18,2) | Saldo final |
| fecha | Date | Fecha del reporte |
| año | Integer | Año |
| periodo | Integer | Periodo (AAAAMM) |

## 🔗 Conexión desde Power BI

1. En Power BI Desktop, ve a **Obtener datos** > **Web**
2. URL base: `http://localhost:8000/api/powerbi/balance-reports`
3. Agregar parámetros según necesites
4. Configurar autenticación si es necesario

## ⚠️ Notas Importantes

- Los reportes se procesan mes por mes (como en PowerQuery)
- El token de Siigo se obtiene una sola vez y se reutiliza
- Los datos se pueden limpiar antes de insertar (`clear_existing: true`)
- El procesamiento puede tardar varios minutos dependiendo de los meses

## 🐛 Troubleshooting

### Error de conexión a PostgreSQL
- Verificar que PostgreSQL esté corriendo: `sudo systemctl status postgresql`
- Verificar credenciales en `.env`
- Verificar que la base de datos exista

### Error procesando Excel
- Verificar que el formato del Excel sea el esperado
- Revisar logs del backend para ver errores específicos

### Rate Limit de Siigo
- Esperar entre peticiones
- Procesar menos meses a la vez


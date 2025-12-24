# 📊 Dónde Ver los Datos Guardados

## 🗄️ Dónde se Guardan los Datos

### Ubicación Física:
```
/home/elvix/siigo-app/siigo_data.db
```

**Tipo:** Base de datos SQLite (archivo local)

**Tabla:** `balance_reports`

---

## 👀 Cómo Ver los Datos

### Opción 1: Desde el Frontend (Más Fácil) ⭐

1. **Abre el frontend:**
   ```
   http://localhost:5177
   ```

2. **Ve a la sección "📊 Ver Datos Procesados"**

3. **Verás automáticamente:**
   - Total de registros
   - Saldo final total
   - Años disponibles
   - Periodos disponibles

4. **Para ver los datos detallados:**
   - Opcional: Filtra por año o periodo
   - Haz clic en "🔍 Consultar Datos"
   - Verás una tabla con todos los campos

---

### Opción 2: Desde Swagger UI (Interfaz Visual)

1. **Abre Swagger:**
   ```
   http://localhost:8000/docs
   ```

2. **Ver Estadísticas:**
   - Busca: `GET /api/powerbi/stats`
   - Haz clic en "Try it out" → "Execute"
   - Verás: total de registros, años, periodos

3. **Ver Datos Completos:**
   - Busca: `GET /api/powerbi/balance-reports`
   - Haz clic en "Try it out"
   - Configura filtros (opcional):
     - `año`: 2024
     - `periodo`: 202401
     - `limit`: 100
   - Haz clic en "Execute"
   - Verás los registros en formato JSON

---

### Opción 3: Desde la Terminal (curl)

#### Ver Estadísticas:
```bash
curl http://localhost:8000/api/powerbi/stats
```

#### Ver Datos (primeros 10):
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?limit=10"
```

#### Ver Datos de un Año Específico:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=10"
```

#### Ver Datos de un Periodo Específico:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?periodo=202401&limit=10"
```

#### Ver Datos con Filtros Múltiples:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?año=2024&periodo=202401&limit=100"
```

---

### Opción 4: Desde SQLite Directamente

#### Abrir la Base de Datos:
```bash
cd /home/elvix/siigo-app
sqlite3 siigo_data.db
```

#### Consultas Útiles:

**Ver total de registros:**
```sql
SELECT COUNT(*) FROM balance_reports;
```

**Ver primeros 10 registros:**
```sql
SELECT * FROM balance_reports LIMIT 10;
```

**Ver resumen por año:**
```sql
SELECT año, COUNT(*) as registros, COUNT(DISTINCT periodo) as periodos
FROM balance_reports
GROUP BY año;
```

**Ver resumen por periodo:**
```sql
SELECT periodo, COUNT(*) as registros
FROM balance_reports
GROUP BY periodo
ORDER BY periodo;
```

**Ver datos de un periodo específico:**
```sql
SELECT * FROM balance_reports WHERE periodo = 202401 LIMIT 10;
```

**Ver datos de un año:**
```sql
SELECT * FROM balance_reports WHERE año = 2024 LIMIT 10;
```

**Salir de SQLite:**
```sql
.quit
```

---

## 📋 Campos Disponibles en los Datos

Cada registro tiene estos campos:

- `id` - ID único del registro
- `codigo_cuenta_contable` - Código de la cuenta
- `nombre_cuenta_contable` - Nombre de la cuenta
- `cod_relacional` - Código relacional (primeros 6 dígitos)
- `identificacion` - Identificación del tercero
- `sucursal` - Sucursal
- `nombre_tercero` - Nombre del tercero
- `saldo_inicial` - Saldo inicial
- `movimiento_debito` - Movimiento débito
- `movimiento_credito` - Movimiento crédito
- `movimiento` - Movimiento neto (débito - crédito)
- `saldo_final` - Saldo final
- `fecha` - Fecha del periodo
- `año` - Año
- `periodo` - Periodo (formato AAAAMM, ej: 202401)
- `created_at` - Fecha de creación
- `updated_at` - Fecha de actualización

---

## 🔍 Ejemplos de Consultas Útiles

### Ver cuántos registros hay:
```bash
curl http://localhost:8000/api/powerbi/stats
```

### Ver datos de enero 2024:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?periodo=202401&limit=100"
```

### Ver datos de todo 2024:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=1000"
```

### Ver datos de una cuenta específica:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?codigo_cuenta=110505&limit=100"
```

### Ver datos de un tercero específico:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?identificacion=123456789&limit=100"
```

---

## 📊 Para Power BI

### URL del Endpoint:
```
http://localhost:8000/api/powerbi/balance-reports
```

### Parámetros Disponibles:
- `año` - Filtrar por año (ej: 2024)
- `periodo` - Filtrar por periodo AAAAMM (ej: 202401)
- `codigo_cuenta` - Filtrar por código de cuenta
- `cod_relacional` - Filtrar por código relacional
- `identificacion` - Filtrar por identificación
- `limit` - Límite de registros (1-10000, default: 1000)
- `offset` - Offset para paginación (default: 0)

### Ejemplo para Power BI:
```
http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=10000
```

---

## 💾 Respaldo de Datos

### Copiar la Base de Datos:
```bash
cp /home/elvix/siigo-app/siigo_data.db /ruta/de/respaldo/siigo_data_backup.db
```

### Ver Tamaño de la Base de Datos:
```bash
ls -lh /home/elvix/siigo-app/siigo_data.db
```

---

## 🔄 Migrar a PostgreSQL (Opcional)

Si quieres usar PostgreSQL en lugar de SQLite:

1. Configura PostgreSQL (ver `CONFIGURAR_POSTGRESQL.md`)
2. Actualiza el archivo `.env` con las credenciales
3. Los datos se guardarán en PostgreSQL en lugar de SQLite

---

## ✅ Resumen Rápido

| Método | URL/Comando | Cuándo Usar |
|--------|-------------|-------------|
| **Frontend** | `http://localhost:5177` | Interfaz visual fácil |
| **Swagger** | `http://localhost:8000/docs` | Probar endpoints |
| **curl** | `curl http://localhost:8000/api/powerbi/stats` | Desde terminal |
| **SQLite** | `sqlite3 siigo_data.db` | Consultas SQL directas |
| **Power BI** | `http://localhost:8000/api/powerbi/balance-reports` | Conectar Power BI |

---

**💡 Recomendación:** Empieza con el **Frontend** (`http://localhost:5177`) - es la forma más fácil de ver los datos.


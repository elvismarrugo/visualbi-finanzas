# 🚀 Cómo Usar la API - Guía Paso a Paso

## 📍 Paso 1: Abrir Swagger UI (Interfaz Visual)

Abre en tu navegador:
```
http://localhost:8000/docs
```

Verás una interfaz con todos los endpoints disponibles.

---

## 🎯 Paso 2: Procesar Datos (ETL)

### Endpoint: `POST /api/etl/process-year`

Este endpoint descarga y procesa los datos de Siigo automáticamente.

**Cómo usarlo:**

1. En Swagger UI, busca: `POST /api/etl/process-year`
2. Haz clic en el endpoint para expandirlo
3. Haz clic en **"Try it out"**
4. Modifica el JSON con tus parámetros:

```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 3,
  "includes_tax_diff": false,
  "clear_existing": true
}
```

**Parámetros:**
- `year`: Año a procesar (ej: 2024)
- `month_start`: Mes inicial (1-13, donde 13 = cierre)
- `month_end`: Mes final (1-13)
- `includes_tax_diff`: true/false
- `clear_existing`: true = borra datos existentes antes de insertar

5. Haz clic en **"Execute"**

**Respuesta esperada:**
```json
{
  "year": 2024,
  "months_processed": [1, 2, 3],
  "total_rows": 1500,
  "errors": [],
  "success": true
}
```

**⚠️ IMPORTANTE:** Este proceso puede tardar varios minutos porque:
- Descarga Excel de cada mes
- Procesa y transforma los datos
- Guarda todo en la base de datos

---

## 📊 Paso 3: Ver los Datos Procesados

### Opción A: Ver Estadísticas

**Endpoint:** `GET /api/powerbi/stats`

1. Busca en Swagger: `GET /api/powerbi/stats`
2. Haz clic en "Try it out"
3. Opcional: agrega `año=2024` como parámetro
4. Haz clic en "Execute"

**Respuesta:**
```json
{
  "total_records": 1500,
  "total_saldo_final": 1234567.89,
  "years": [2024],
  "periods": [202401, 202402, 202403]
}
```

### Opción B: Ver Datos Completos

**Endpoint:** `GET /api/powerbi/balance-reports`

1. Busca en Swagger: `GET /api/powerbi/balance-reports`
2. Haz clic en "Try it out"
3. Configura los filtros (opcionales):
   - `año`: 2024
   - `periodo`: 202401 (formato AAAAMM)
   - `limit`: 1000 (máximo de registros)
   - `offset`: 0 (para paginación)
4. Haz clic en "Execute"

**Respuesta:**
```json
{
  "data": [
    {
      "id": 1,
      "codigo_cuenta_contable": 110505,
      "nombre_cuenta_contable": "Bancos",
      "cod_relacional": "110505",
      "identificacion": "123456789",
      "sucursal": "Principal",
      "nombre_tercero": "Cliente ABC",
      "saldo_inicial": 1000.00,
      "movimiento_debito": 500.00,
      "movimiento_credito": 200.00,
      "movimiento": 300.00,
      "saldo_final": 1300.00,
      "fecha": "2024-01-31",
      "año": 2024,
      "periodo": 202401
    },
    ...
  ],
  "total": 1500,
  "limit": 1000,
  "offset": 0,
  "has_more": true
}
```

---

## 🔧 Paso 4: Usar desde Línea de Comandos (curl)

### Procesar Datos:
```bash
curl -X POST "http://localhost:8000/api/etl/process-year" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2024,
    "month_start": 1,
    "month_end": 3,
    "includes_tax_diff": false,
    "clear_existing": true
  }'
```

### Ver Estadísticas:
```bash
curl "http://localhost:8000/api/powerbi/stats?año=2024"
```

### Ver Datos:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=10"
```

---

## 🐍 Paso 5: Usar desde Python

```python
import requests

# 1. Procesar datos
response = requests.post(
    "http://localhost:8000/api/etl/process-year",
    json={
        "year": 2024,
        "month_start": 1,
        "month_end": 3,
        "includes_tax_diff": False,
        "clear_existing": True
    }
)
print(response.json())

# 2. Ver estadísticas
stats = requests.get("http://localhost:8000/api/powerbi/stats?año=2024")
print(stats.json())

# 3. Ver datos
data = requests.get("http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=100")
print(data.json())
```

---

## 📋 Flujo Completo de Trabajo

1. **Procesar datos por primera vez:**
   ```
   POST /api/etl/process-year
   {
     "year": 2024,
     "month_start": 1,
     "month_end": 12,
     "clear_existing": true
   }
   ```

2. **Verificar que se guardaron:**
   ```
   GET /api/powerbi/stats
   ```

3. **Consultar datos específicos:**
   ```
   GET /api/powerbi/balance-reports?año=2024&periodo=202401
   ```

4. **Actualizar datos (agregar más meses):**
   ```
   POST /api/etl/process-year
   {
     "year": 2024,
     "month_start": 4,
     "month_end": 6,
     "clear_existing": false  // No borra lo existente
   }
   ```

---

## ⚠️ Problemas Comunes

### "Servicio ETL no disponible"
- **Causa:** Base de datos no está configurada
- **Solución:** Verifica que SQLite esté funcionando o configura PostgreSQL

### "Error de autenticación con Siigo"
- **Causa:** Credenciales incorrectas en `.env`
- **Solución:** Verifica `SIIGO_ACCESS_KEY` y `SIIGO_USERNAME`

### "No se recibió file_url"
- **Causa:** Siigo no generó el reporte
- **Solución:** Verifica los parámetros (año, meses válidos)

### No veo datos después de procesar
- **Verifica:** Usa `GET /api/powerbi/stats` para ver si hay registros
- **Verifica:** Los filtros en `balance-reports` pueden estar ocultando datos

---

## 🎯 Ejemplo Práctico Completo

```bash
# 1. Procesar enero 2024
curl -X POST "http://localhost:8000/api/etl/process-year" \
  -H "Content-Type: application/json" \
  -d '{"year": 2024, "month_start": 1, "month_end": 1, "clear_existing": true}'

# 2. Esperar respuesta (puede tardar 1-2 minutos)

# 3. Verificar estadísticas
curl "http://localhost:8000/api/powerbi/stats"

# 4. Ver los primeros 10 registros
curl "http://localhost:8000/api/powerbi/balance-reports?limit=10"
```

---

## 📚 Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/etl/process-year` | POST | Procesa datos de un año |
| `/api/etl/process-previous-year` | POST | Procesa año anterior |
| `/api/powerbi/balance-reports` | GET | Obtiene datos con filtros |
| `/api/powerbi/stats` | GET | Estadísticas agregadas |
| `/api/balance-report-by-thirdparty` | POST | Descarga Excel directo (sin guardar) |

---

**💡 Tip:** Empieza con pocos meses (1-3) para probar que todo funciona antes de procesar un año completo.


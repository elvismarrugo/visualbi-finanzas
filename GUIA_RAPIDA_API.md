# ⚡ Guía Rápida: Cómo Usar la API

## 🎯 El Problema

**"No veo que traiga los datos"** - Esto es normal porque **primero debes procesar los datos**.

La API tiene 2 tipos de endpoints:
1. **ETL (Procesar)**: Descarga y guarda datos de Siigo
2. **Consultar**: Muestra los datos ya guardados

---

## 🚀 Solución Rápida (3 Pasos)

### Paso 1: Abre Swagger UI
```
http://localhost:8000/docs
```

### Paso 2: Procesa los Datos

1. Busca: **`POST /api/etl/process-year`**
2. Haz clic en el endpoint
3. Haz clic en **"Try it out"**
4. Ingresa esto:
```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 1,
  "includes_tax_diff": false,
  "clear_existing": true
}
```
5. Haz clic en **"Execute"**
6. ⏳ **Espera 1-2 minutos** (descarga y procesa el Excel)

### Paso 3: Ver los Datos

1. Busca: **`GET /api/powerbi/stats`**
2. Haz clic en "Try it out" → "Execute"
3. Verás: `"total_records": X` (donde X > 0 si hay datos)

4. Para ver los datos completos:
   - Busca: **`GET /api/powerbi/balance-reports`**
   - Haz clic en "Try it out"
   - Deja los parámetros por defecto
   - Haz clic en "Execute"

---

## 📊 ¿Qué Hace Cada Endpoint?

### `POST /api/etl/process-year`
- **Qué hace:** Descarga Excel de Siigo, lo procesa y guarda en la base de datos
- **Cuándo usar:** La primera vez, o cuando quieres actualizar datos
- **Tiempo:** 1-2 minutos por mes
- **Resultado:** Los datos quedan guardados en la base de datos

### `GET /api/powerbi/stats`
- **Qué hace:** Muestra estadísticas de los datos guardados
- **Cuándo usar:** Para verificar cuántos registros hay
- **Tiempo:** Instantáneo
- **Resultado:** Números agregados (total de registros, años, periodos)

### `GET /api/powerbi/balance-reports`
- **Qué hace:** Muestra los datos guardados con filtros
- **Cuándo usar:** Para ver los datos detallados
- **Tiempo:** Instantáneo
- **Resultado:** Lista de registros con todos los campos

---

## 🔍 Verificación Rápida

### ¿Tengo datos guardados?

Ejecuta esto en tu terminal:
```bash
curl http://localhost:8000/api/powerbi/stats
```

**Si ves:**
```json
{
  "total_records": 0,
  "years": [],
  "periods": []
}
```
→ **No hay datos.** Necesitas procesar primero con `POST /api/etl/process-year`

**Si ves:**
```json
{
  "total_records": 1500,
  "years": [2024],
  "periods": [202401]
}
```
→ **¡Hay datos!** Puedes consultarlos con `GET /api/powerbi/balance-reports`

---

## 🎬 Ejemplo Visual

```
1. Abres: http://localhost:8000/docs
   ↓
2. Buscas: POST /api/etl/process-year
   ↓
3. "Try it out" → Ingresas JSON → "Execute"
   ↓
4. Esperas 1-2 minutos
   ↓
5. Respuesta: {"total_rows": 500, "success": true}
   ↓
6. Ahora SÍ puedes ver datos:
   GET /api/powerbi/stats → {"total_records": 500}
   GET /api/powerbi/balance-reports → [datos...]
```

---

## ⚠️ Errores Comunes

### "Servicio ETL no disponible"
- **Causa:** Base de datos no configurada
- **Solución:** Ya está configurada (SQLite), pero verifica que el backend esté corriendo

### "Error de autenticación con Siigo"
- **Causa:** Credenciales incorrectas
- **Solución:** Verifica `.env` (SIIGO_ACCESS_KEY debe terminar con `=`)

### "total_records: 0" después de procesar
- **Causa:** El procesamiento falló silenciosamente
- **Solución:** Revisa la respuesta del ETL, busca en "errors"

---

## 🧪 Probar Automáticamente

Ejecuta el script de prueba:
```bash
bash probar_api.sh
```

Este script:
1. Verifica que el backend esté corriendo
2. Muestra estadísticas actuales
3. Te pregunta si quieres procesar datos
4. Muestra los resultados

---

## 📚 Más Información

- **Guía completa:** `COMO_USAR_LA_API.md`
- **Estado del sistema:** `ESTADO_ACTUAL.md`

---

**💡 Recuerda:** Los datos no aparecen mágicamente. Primero debes **procesarlos** con el endpoint ETL, y luego puedes **consultarlos**.


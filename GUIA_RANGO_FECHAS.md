# 📅 Guía: Procesar por Rango de Fechas

## 🎯 ¿Qué hace esta funcionalidad?

Permite procesar automáticamente todos los periodos desde **31/01/2024** hasta una fecha que tú indiques.

**Ejemplo:** Si ingresas `30/09/2025`, el sistema procesará:
- 2024: meses 1-12 (enero a diciembre)
- 2025: meses 1-9 (enero a septiembre)
- **Total: 21 periodos**

---

## 🚀 Cómo Usar

### Opción 1: Desde el Frontend (Recomendado)

1. **Abre el frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Verás el nuevo componente** "📅 Procesar por Rango de Fechas" arriba del formulario anterior

3. **Ingresa la fecha de fin:**
   - Formato: DD/MM/YYYY o usa el selector de fecha
   - Ejemplo: `30/09/2025`

4. **Configura opciones:**
   - ☑️ Incluir diferencia de impuestos (opcional)
   - ☑️ Limpiar datos existentes (recomendado)

5. **Haz clic en "🚀 Procesar Rango de Fechas"**

6. **Espera el procesamiento:**
   - Puede tardar varios minutos (1-2 min por mes)
   - Verás el progreso en tiempo real

7. **Verifica los resultados:**
   - Total de periodos procesados
   - Total de registros guardados
   - Lista de periodos procesados
   - Errores (si los hay)

### Opción 2: Desde Swagger UI

1. **Abre Swagger:**
   ```
   http://localhost:8000/docs
   ```

2. **Busca:** `POST /api/etl/process-date-range`

3. **Haz clic en "Try it out"**

4. **Ingresa el JSON:**
   ```json
   {
     "fecha_fin": "2025-09-30",
     "includes_tax_diff": false,
     "clear_existing": true
   }
   ```

5. **Haz clic en "Execute"**

### Opción 3: Desde Línea de Comandos

```bash
curl -X POST "http://localhost:8000/api/etl/process-date-range" \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_fin": "2025-09-30",
    "includes_tax_diff": false,
    "clear_existing": true
  }'
```

---

## 📊 Respuesta del Endpoint

```json
{
  "fecha_inicio": "2024-01-31",
  "fecha_fin": "2025-09-30",
  "periodos_procesados": [
    "2024-01",
    "2024-02",
    "2024-03",
    ...
    "2025-09"
  ],
  "total_periodos": 21,
  "total_rows": 158000,
  "errors": [],
  "success": true
}
```

---

## ⚙️ Parámetros

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fecha_fin` | string | ✅ Sí | Fecha de fin en formato YYYY-MM-DD |
| `includes_tax_diff` | boolean | ❌ No | Incluir diferencia de impuestos (default: false) |
| `clear_existing` | boolean | ❌ No | Limpiar datos existentes antes (default: true) |
| `account_start` | string | ❌ No | Código de cuenta inicial (opcional) |
| `account_end` | string | ❌ No | Código de cuenta final (opcional) |

---

## 🔍 Verificar Datos Procesados

### Ver Estadísticas:
```bash
curl http://localhost:8000/api/powerbi/stats
```

### Ver Datos:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?limit=10"
```

### Desde Swagger:
- `GET /api/powerbi/stats`
- `GET /api/powerbi/balance-reports`

---

## ⚠️ Consideraciones

1. **Tiempo de procesamiento:**
   - Aproximadamente 1-2 minutos por mes
   - Para 21 periodos: ~20-40 minutos

2. **Rate Limit de Siigo:**
   - El sistema maneja automáticamente los rate limits
   - Espera automáticamente si hay límite de peticiones

3. **Datos existentes:**
   - Si `clear_existing: true`, se eliminan los datos del rango antes de procesar
   - Si `clear_existing: false`, se agregan sin eliminar

4. **Errores:**
   - Si un periodo falla, el sistema continúa con los siguientes
   - Todos los errores se reportan al final

---

## 🆘 Solución de Problemas

### Error: "Formato de fecha inválido"
- **Causa:** La fecha no está en formato YYYY-MM-DD
- **Solución:** Usa formato `2025-09-30` (no `30/09/2025`)

### Error: "La fecha de fin debe ser posterior a 2024-01-31"
- **Causa:** La fecha es anterior a la fecha inicio
- **Solución:** Usa una fecha posterior a 2024-01-31

### Error: "Rate limit is exceeded"
- **Causa:** Demasiadas peticiones a Siigo
- **Solución:** El sistema espera automáticamente, pero puedes esperar unos minutos y reintentar

### No se procesan todos los periodos
- **Causa:** Puede haber errores en algunos periodos
- **Solución:** Revisa la lista de errores en la respuesta

---

## 📚 Ejemplos

### Procesar hasta fin de 2024:
```json
{
  "fecha_fin": "2024-12-31",
  "clear_existing": true
}
```
**Resultado:** Procesa 12 periodos (2024-01 a 2024-12)

### Procesar hasta fin de 2025:
```json
{
  "fecha_fin": "2025-12-31",
  "clear_existing": true
}
```
**Resultado:** Procesa 24 periodos (2024-01 a 2025-12)

### Procesar solo hasta septiembre 2025:
```json
{
  "fecha_fin": "2025-09-30",
  "clear_existing": true
}
```
**Resultado:** Procesa 21 periodos (2024-01 a 2025-09)

---

## 🎯 Comparación con PowerQuery

Esta funcionalidad replica exactamente la lógica de PowerQuery:

**PowerQuery:**
```m
pYear = 2025
pMonthStart = 1
pMonthEnd = 9
// Procesa desde 2024-01 hasta 2025-09
```

**API:**
```json
{
  "fecha_fin": "2025-09-30"
}
// Procesa automáticamente desde 2024-01-31 hasta 2025-09-30
```

---

**✅ La funcionalidad está lista para usar!**


# 📝 Ejemplo de Uso con curl

## ✅ Comando Correcto

El comando que ejecutaste funcionó, pero necesitas usar una **fecha real** en lugar de `"string"`.

### ❌ Incorrecto:
```bash
curl -X POST 'http://localhost:8000/api/etl/process-date-range' \
  -H 'Content-Type: application/json' \
  -d '{
    "fecha_fin": "string",  # ❌ Esto no funciona
    ...
  }'
```

### ✅ Correcto:
```bash
curl -X POST 'http://localhost:8000/api/etl/process-date-range' \
  -H 'Content-Type: application/json' \
  -d '{
    "fecha_fin": "2025-09-30",  # ✅ Fecha en formato YYYY-MM-DD
    "includes_tax_diff": false,
    "clear_existing": true
  }'
```

---

## 🎯 Ejemplos de Uso

### Procesar hasta septiembre 2025:
```bash
curl -X POST 'http://localhost:8000/api/etl/process-date-range' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "fecha_fin": "2025-09-30",
    "includes_tax_diff": false,
    "clear_existing": true
  }'
```

**Resultado:** Procesa 21 periodos (2024-01 a 2025-09)

### Procesar hasta fin de 2024:
```bash
curl -X POST 'http://localhost:8000/api/etl/process-date-range' \
  -H 'Content-Type: application/json' \
  -d '{
    "fecha_fin": "2024-12-31",
    "clear_existing": true
  }'
```

**Resultado:** Procesa 12 periodos (2024-01 a 2024-12)

### Procesar hasta fin de 2025:
```bash
curl -X POST 'http://localhost:8000/api/etl/process-date-range' \
  -H 'Content-Type: application/json' \
  -d '{
    "fecha_fin": "2025-12-31",
    "clear_existing": true
  }'
```

**Resultado:** Procesa 24 periodos (2024-01 a 2025-12)

### Con filtros de cuenta:
```bash
curl -X POST 'http://localhost:8000/api/etl/process-date-range' \
  -H 'Content-Type: application/json' \
  -d '{
    "fecha_fin": "2025-09-30",
    "account_start": "1105",
    "account_end": "1199",
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
  "total_rows": 166803,
  "errors": [],
  "success": true
}
```

---

## ⚠️ Notas Importantes

1. **Formato de fecha:** Debe ser `YYYY-MM-DD` (no `DD/MM/YYYY`)
2. **Tiempo de procesamiento:** Aproximadamente 1-2 minutos por mes
3. **Rate limits:** El sistema maneja automáticamente los límites de Siigo
4. **Parámetros opcionales:** `account_start`, `account_end` son opcionales

---

## 🔍 Verificar Resultados

### Ver estadísticas:
```bash
curl http://localhost:8000/api/powerbi/stats
```

### Ver datos:
```bash
curl "http://localhost:8000/api/powerbi/balance-reports?limit=10"
```

---

**✅ El comando funcionó perfectamente! Procesó 21 periodos y guardó 166,803 registros.**


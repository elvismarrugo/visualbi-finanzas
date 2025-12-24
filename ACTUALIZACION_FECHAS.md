# 📅 Actualización: Sistema Ahora Pide Ambas Fechas

## ✅ Cambios Realizados

El sistema ahora permite ingresar **ambas fechas** (inicio y fin) en lugar de usar una fecha fija.

### Antes:
- ❌ Solo pedía fecha de fin
- ❌ Fecha de inicio fija: 2024-01-31

### Ahora:
- ✅ Pide fecha de inicio
- ✅ Pide fecha de fin
- ✅ Validación: fecha_fin >= fecha_inicio

---

## 🎯 Cómo Usar

### Desde el Frontend:

1. **Abre el frontend** (si no está corriendo):
   ```bash
   cd frontend
   npm run dev
   ```

2. **Verás el formulario actualizado** con dos campos:
   - **Fecha de Inicio** (ej: 2024-01-31)
   - **Fecha de Fin** (ej: 2025-09-30)

3. **Ingresa ambas fechas** y haz clic en "Procesar Rango de Fechas"

### Desde Swagger UI:

1. Abre: `http://localhost:8000/docs`
2. Busca: `POST /api/etl/process-date-range`
3. Ingresa el JSON:
```json
{
  "fecha_inicio": "2024-01-31",
  "fecha_fin": "2025-09-30",
  "includes_tax_diff": false,
  "clear_existing": true
}
```

### Desde curl:

```bash
curl -X POST 'http://localhost:8000/api/etl/process-date-range' \
  -H 'Content-Type: application/json' \
  -d '{
    "fecha_inicio": "2024-01-31",
    "fecha_fin": "2025-09-30",
    "includes_tax_diff": false,
    "clear_existing": true
  }'
```

---

## 📋 Ejemplos

### Procesar solo 2024:
```json
{
  "fecha_inicio": "2024-01-31",
  "fecha_fin": "2024-12-31"
}
```
**Resultado:** Procesa 12 periodos (2024-01 a 2024-12)

### Procesar solo algunos meses de 2024:
```json
{
  "fecha_inicio": "2024-06-30",
  "fecha_fin": "2024-09-30"
}
```
**Resultado:** Procesa 4 periodos (2024-06 a 2024-09)

### Procesar desde 2024 hasta 2025:
```json
{
  "fecha_inicio": "2024-01-31",
  "fecha_fin": "2025-09-30"
}
```
**Resultado:** Procesa 21 periodos (2024-01 a 2025-09)

---

## ⚠️ Validaciones

1. **Formato de fecha:** Debe ser `YYYY-MM-DD`
2. **Fecha fin >= Fecha inicio:** La fecha de fin debe ser posterior o igual a la fecha de inicio
3. **Campos requeridos:** Ambos campos son obligatorios

---

## 🔄 Archivos Modificados

- ✅ `backend/models.py` - Modelo actualizado
- ✅ `backend/etl_service.py` - Lógica actualizada
- ✅ `backend/main.py` - Endpoint actualizado
- ✅ `frontend/src/components/DateRangeProcessor.jsx` - Interfaz actualizada

---

**✅ El sistema ahora es más flexible y permite procesar cualquier rango de fechas!**


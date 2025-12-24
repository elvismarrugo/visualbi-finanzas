# 📅 Mes 13: Cierre Anual en Siigo API

## 🎯 Concepto Importante

En la **Siigo API**, el valor **13** se utiliza específicamente para representar el **mes de cierre anual** de la empresa.

### ¿Qué es el Mes 13?

El mes 13 es el **epílogo o cierre contable** que ocurre al finalizar el año fiscal. Incluye:
- ✅ Ajustes contables finales
- ✅ Saldos definitivos del proceso de cierre
- ✅ Balance cuadrado para el cierre anual

**Visualización:** Imagina que el año contable es un libro con 12 capítulos (meses 1-12); el mes 13 funciona como el epílogo donde se resumen todas las historias y se ajustan los detalles finales.

---

## 📋 Reglas de la API

1. **Rango válido:** `month_start` y `month_end` aceptan valores de **1 a 13**
2. **Validación:** Valores fuera de este rango retornan error `invalid_range`
3. **Lógica:** `month_start` no puede ser mayor a `month_end`
4. **Año completo con cierre:** Para ver todo el año incluyendo el cierre, usar:
   - `month_start = 1`
   - `month_end = 13`

---

## 🔧 Cómo Funciona en Nuestro Sistema

### Procesamiento Automático

El sistema **automáticamente incluye el mes 13** cuando:

1. **Fecha de fin es 31 de diciembre:**
   - Si procesas hasta `2024-12-31`, incluirá el mes 13 de 2024
   - Ejemplo: `fecha_inicio: "2024-01-31"`, `fecha_fin: "2024-12-31"`
   - **Resultado:** Procesa meses 1-12 y mes 13 (cierre)

2. **Años intermedios:**
   - Si procesas múltiples años, cada año completo incluye su mes 13
   - Ejemplo: `fecha_inicio: "2024-01-31"`, `fecha_fin: "2025-12-31"`
   - **Resultado:** 
     - 2024: meses 1-12 y mes 13
     - 2025: meses 1-12 y mes 13

### Procesamiento Manual

También puedes especificar el mes 13 directamente:

```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 13,
  "includes_tax_diff": false
}
```

**Resultado:** Procesa meses 1-12 y mes 13 (cierre) de 2024

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Año completo con cierre
```json
{
  "fecha_inicio": "2024-01-31",
  "fecha_fin": "2024-12-31"
}
```
**Periodos procesados:** 2024-01, 2024-02, ..., 2024-12, **2024-13** (cierre)

### Ejemplo 2: Hasta septiembre (sin cierre)
```json
{
  "fecha_inicio": "2024-01-31",
  "fecha_fin": "2024-09-30"
}
```
**Periodos procesados:** 2024-01, 2024-02, ..., 2024-09 (sin mes 13)

### Ejemplo 3: Múltiples años con cierres
```json
{
  "fecha_inicio": "2024-01-31",
  "fecha_fin": "2025-12-31"
}
```
**Periodos procesados:**
- 2024: 01-12, **13** (cierre)
- 2025: 01-12, **13** (cierre)

### Ejemplo 4: Especificar mes 13 manualmente
```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 13
}
```
**Periodos procesados:** 2024-01, 2024-02, ..., 2024-12, **2024-13** (cierre)

---

## 🔍 Cómo se Procesa el Mes 13

### En el Excel Processor:

```python
if month == 13:
    # Mes 13 = cierre = 31 de diciembre
    fecha = date(year, 12, 31)
```

- **Fecha asignada:** 31 de diciembre del año
- **Periodo:** `year * 100 + 13` (ej: 202413)
- **Datos:** Incluye ajustes de cierre contable

---

## ⚠️ Consideraciones Importantes

1. **El mes 13 solo existe al final del año:**
   - No puedes procesar mes 13 de enero o febrero
   - Solo tiene sentido al finalizar un año contable

2. **Incluir cierre es opcional:**
   - Si procesas hasta `2024-11-30`, NO incluirá el mes 13
   - Solo se incluye si la fecha de fin es `31 de diciembre`

3. **Datos del cierre:**
   - El mes 13 contiene ajustes y saldos finales
   - Es importante para tener el balance completo del año

---

## 📚 Referencias

- **Siigo API Documentation:** El mes 13 representa el cierre anual
- **Rango válido:** 1-13 para `month_start` y `month_end`
- **Error si fuera de rango:** `invalid_range`

---

## ✅ Resumen

| Escenario | Mes 13 Incluido? | Cómo |
|-----------|------------------|------|
| Fecha fin = 31/12 | ✅ Sí | Automático |
| Fecha fin < 31/12 | ❌ No | No se incluye |
| month_end = 13 | ✅ Sí | Manual |
| Múltiples años | ✅ Sí (cada año) | Automático si termina en 31/12 |

---

**💡 Tip:** Si necesitas el balance completo del año con todos los ajustes, asegúrate de procesar hasta el 31 de diciembre o especificar `month_end = 13`.


# 📍 Dónde Ver la Información

## 🚀 Formas de Acceder a la Información

### 1. **Documentación Interactiva de la API (Swagger UI)**

La forma más fácil de ver y probar todos los endpoints:

**URL:** `http://localhost:8000/docs`

**Qué puedes hacer:**
- ✅ Ver todos los endpoints disponibles
- ✅ Probar los endpoints directamente desde el navegador
- ✅ Ver los modelos de datos (schemas)
- ✅ Ver ejemplos de requests y responses

**Cómo acceder:**
1. Asegúrate de que el backend esté corriendo
2. Abre tu navegador
3. Ve a: `http://localhost:8000/docs`

---

### 2. **Documentación ReDoc (Alternativa)**

Una versión más limpia de la documentación:

**URL:** `http://localhost:8000/redoc`

---

### 3. **Endpoints de Consulta para Power BI**

#### Consultar Datos de Balance Reports

**URL:** `http://localhost:8000/api/powerbi/balance-reports`

**Parámetros disponibles:**
- `año` - Filtrar por año (ej: `?año=2024`)
- `periodo` - Filtrar por periodo AAAAMM (ej: `?periodo=202401`)
- `codigo_cuenta` - Filtrar por código de cuenta
- `cod_relacional` - Filtrar por código relacional
- `identificacion` - Filtrar por identificación
- `limit` - Límite de registros (default: 1000, max: 10000)
- `offset` - Para paginación (default: 0)

**Ejemplos:**
```
# Todos los datos del año 2024
http://localhost:8000/api/powerbi/balance-reports?año=2024

# Primeros 100 registros
http://localhost:8000/api/powerbi/balance-reports?limit=100

# Datos de un periodo específico
http://localhost:8000/api/powerbi/balance-reports?periodo=202401

# Con paginación
http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=1000&offset=0
```

#### Estadísticas Agregadas

**URL:** `http://localhost:8000/api/powerbi/stats`

**Parámetros:**
- `año` - Filtrar por año (opcional)

**Ejemplo:**
```
http://localhost:8000/api/powerbi/stats?año=2024
```

---

### 4. **Base de Datos PostgreSQL (Directo)**

Si tienes acceso a PostgreSQL, puedes consultar directamente:

```bash
# Conectar a PostgreSQL
psql -U siigo_user -d siigo_db

# Consultar datos
SELECT * FROM balance_reports LIMIT 10;

# Contar registros por año
SELECT año, COUNT(*) FROM balance_reports GROUP BY año;

# Ver estructura de la tabla
\d balance_reports
```

---

### 5. **Archivos de Documentación**

#### README Principal
**Archivo:** `README.md`
- Instrucciones generales
- Configuración
- Uso básico

#### Documentación ETL
**Archivo:** `README_ETL.md`
- Sistema ETL completo
- Configuración de PostgreSQL
- Endpoints ETL
- Estructura de datos

#### Soluciones a Problemas
- `SOLUCION_ACCESS_KEY.md` - Problemas de autenticación
- `ERRORES_EXTENSIONES_NAVEGADOR.md` - Errores del navegador
- `CORRECCIONES_APLICADAS.md` - Correcciones realizadas

---

### 6. **Frontend Web**

**URL:** `http://localhost:5173`

**Qué puedes hacer:**
- ✅ Ver formulario para solicitar reportes
- ✅ Descargar archivos Excel directamente
- ✅ Ver resultados en formato JSON

---

### 7. **Logs del Backend**

Para ver información de procesamiento y errores:

```bash
# Ver logs en tiempo real
cd backend
source venv/bin/activate
python main.py
```

Los logs mostrarán:
- ✅ Procesamiento de meses
- ✅ Errores si ocurren
- ✅ Estadísticas de inserción

---

## 📊 Flujo Recomendado para Ver Datos

### Paso 1: Procesar Datos (si no lo has hecho)

```bash
# Desde Swagger UI o con curl
POST http://localhost:8000/api/etl/process-year
{
  "year": 2024,
  "month_start": 1,
  "month_end": 12,
  "includes_tax_diff": false
}
```

### Paso 2: Ver Datos Procesados

**Opción A - Swagger UI (Recomendado):**
1. Ve a `http://localhost:8000/docs`
2. Busca el endpoint `GET /api/powerbi/balance-reports`
3. Haz clic en "Try it out"
4. Agrega parámetros si necesitas
5. Haz clic en "Execute"
6. Verás los datos en formato JSON

**Opción B - Navegador:**
1. Abre: `http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=10`
2. Verás los datos en formato JSON

**Opción C - Power BI:**
1. Abre Power BI Desktop
2. Obtener datos > Web
3. URL: `http://localhost:8000/api/powerbi/balance-reports`
4. Agregar parámetros según necesites

---

## 🔍 Verificación Rápida

### ¿Está el backend corriendo?
```bash
curl http://localhost:8000/health
```
Deberías recibir: `{"status":"healthy"}`

### ¿Hay datos en la base de datos?
```bash
curl http://localhost:8000/api/powerbi/stats
```
Verás estadísticas de los datos almacenados

### ¿Qué endpoints están disponibles?
```bash
curl http://localhost:8000/
```
Verás lista de endpoints disponibles

---

## 💡 Consejos

1. **Para desarrollo:** Usa Swagger UI (`/docs`) - es la forma más fácil
2. **Para Power BI:** Usa los endpoints `/api/powerbi/*`
3. **Para debugging:** Revisa los logs del backend
4. **Para consultas complejas:** Accede directamente a PostgreSQL

---

## 🆘 Si No Ves Datos

1. **Verifica que hayas procesado datos:**
   - Revisa si ejecutaste `/api/etl/process-year`
   - Revisa los logs para ver si hubo errores

2. **Verifica la base de datos:**
   - Asegúrate de que PostgreSQL esté corriendo
   - Verifica las credenciales en `.env`

3. **Verifica el backend:**
   - Asegúrate de que esté corriendo en el puerto 8000
   - Revisa los logs para errores


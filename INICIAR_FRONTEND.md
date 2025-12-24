# 🚀 Cómo Iniciar y Usar el Frontend

## 📋 Paso 1: Iniciar el Frontend

### Opción A: Desde la terminal

```bash
cd /home/elvix/siigo-app/frontend
npm run dev
```

### Opción B: Si no están instaladas las dependencias

```bash
cd /home/elvix/siigo-app/frontend
npm install
npm run dev
```

**El frontend se iniciará en:** `http://localhost:5173` (o el puerto que Vite asigne)

---

## 🎯 Paso 2: Usar la Interfaz

### 1. Abre el navegador

Ve a: `http://localhost:5173`

### 2. Verás dos secciones:

#### 📅 Sección 1: Procesar por Rango de Fechas (NUEVO)

**Campos:**
- **Fecha de Inicio:** Selecciona la fecha inicial (ej: 2024-01-31)
- **Fecha de Fin:** Selecciona la fecha final (ej: 2024-12-31)
- ☑️ **Incluir diferencia de impuestos:** Opcional
- ☑️ **Limpiar datos existentes:** Recomendado para evitar duplicados

**Ejemplo:**
```
Fecha de Inicio: 2024-01-31
Fecha de Fin: 2024-12-31
☑️ Limpiar datos existentes
```

**Resultado:** Procesará meses 1-12 + mes 13 (cierre anual) de 2024

#### 📊 Sección 2: Consultar Reporte de Balance (ORIGINAL)

Para descargar Excel directamente sin guardar en BD.

---

## 📝 Ejemplo Completo de Uso

### Escenario: Procesar año 2024 completo con cierre

1. **Abre:** `http://localhost:5173`

2. **En "Procesar por Rango de Fechas":**
   - Fecha de Inicio: `2024-01-31`
   - Fecha de Fin: `2024-12-31`
   - ☑️ Limpiar datos existentes

3. **Haz clic en:** "🚀 Procesar Rango de Fechas"

4. **Espera:** El procesamiento puede tardar varios minutos (1-2 min por mes)

5. **Verás el resultado:**
   - Total de periodos procesados
   - Total de registros guardados
   - Lista de periodos procesados
   - Errores (si los hay)

---

## 🔍 Ver los Datos Procesados

### Opción 1: Desde Swagger UI

1. Abre: `http://localhost:8000/docs`
2. Busca: `GET /api/powerbi/stats`
3. Haz clic en "Try it out" → "Execute"
4. Verás estadísticas de los datos

### Opción 2: Desde la API directamente

```bash
# Ver estadísticas
curl http://localhost:8000/api/powerbi/stats

# Ver datos (primeros 10 registros)
curl "http://localhost:8000/api/powerbi/balance-reports?limit=10"

# Ver datos de un periodo específico
curl "http://localhost:8000/api/powerbi/balance-reports?periodo=202401&limit=10"

# Ver datos de un año
curl "http://localhost:8000/api/powerbi/balance-reports?año=2024&limit=10"
```

### Opción 3: Desde Swagger UI - Ver Datos

1. Abre: `http://localhost:8000/docs`
2. Busca: `GET /api/powerbi/balance-reports`
3. Configura filtros:
   - `año`: 2024
   - `periodo`: 202401 (opcional)
   - `limit`: 100
4. Haz clic en "Execute"

---

## 🎯 Ejemplos de Parámetros

### Procesar solo algunos meses:
```
Fecha de Inicio: 2024-06-30
Fecha de Fin: 2024-09-30
```
**Resultado:** Procesa meses 6, 7, 8, 9 de 2024

### Procesar año completo con cierre:
```
Fecha de Inicio: 2024-01-31
Fecha de Fin: 2024-12-31
```
**Resultado:** Procesa meses 1-12 + mes 13 (cierre) de 2024

### Procesar múltiples años:
```
Fecha de Inicio: 2024-01-31
Fecha de Fin: 2025-12-31
```
**Resultado:** Procesa 2024 completo (con cierre) + 2025 completo (con cierre)

---

## ⚠️ Solución de Problemas

### Error: "No se pudo conectar con el servidor"
- **Causa:** El backend no está corriendo
- **Solución:** Inicia el backend:
  ```bash
  cd /home/elvix/siigo-app/backend
  source venv/bin/activate
  python main.py
  ```

### Error: "npm: command not found"
- **Causa:** Node.js no está instalado
- **Solución:** Instala Node.js y npm

### El frontend no se carga
- **Causa:** Dependencias no instaladas
- **Solución:**
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

### No veo el componente de rango de fechas
- **Causa:** El frontend no se recargó
- **Solución:** Recarga la página (F5) o reinicia el servidor de desarrollo

---

## 📊 Verificar que Todo Funciona

### 1. Verificar Backend:
```bash
curl http://localhost:8000/health
```
**Debería responder:** `{"status":"healthy"}`

### 2. Verificar Frontend:
Abre: `http://localhost:5173`
**Deberías ver:** El formulario de "Procesar por Rango de Fechas"

### 3. Probar Procesamiento:
- Ingresa fechas
- Haz clic en "Procesar"
- Espera el resultado

### 4. Verificar Datos:
```bash
curl http://localhost:8000/api/powerbi/stats
```
**Deberías ver:** Estadísticas con total de registros

---

## 🎉 ¡Listo para Usar!

Una vez que el frontend esté corriendo, podrás:
- ✅ Ingresar fechas fácilmente
- ✅ Procesar datos con un clic
- ✅ Ver resultados en tiempo real
- ✅ Consultar datos desde Swagger o API

---

**💡 Tip:** Mantén ambas terminales abiertas:
- Terminal 1: Backend (`python main.py`)
- Terminal 2: Frontend (`npm run dev`)


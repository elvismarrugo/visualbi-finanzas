# 🚀 Cómo Iniciar el Backend

## 📋 Método 1: Script Automatizado (Recomendado)

```bash
cd /home/elvix/siigo-app
bash start_backend.sh
```

---

## 📋 Método 2: Manual (Paso a Paso)

### Paso 1: Navegar al directorio del backend
```bash
cd /home/elvix/siigo-app/backend
```

### Paso 2: Activar el entorno virtual
```bash
source venv/bin/activate
```

Verás que el prompt cambia a `(venv)` indicando que el entorno está activo.

### Paso 3: Iniciar el servidor
```bash
python main.py
```

O si prefieres usar uvicorn directamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ✅ Verificar que Funciona

### Opción 1: Desde el navegador
Abre: `http://localhost:8000/docs`

Deberías ver la documentación interactiva de Swagger.

### Opción 2: Desde la terminal
```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{"status":"healthy"}
```

### Opción 3: Verificar endpoint raíz
```bash
curl http://localhost:8000/
```

**Respuesta esperada:**
```json
{
  "message": "Siigo API Integration",
  "version": "1.0.0",
  "endpoints": {
    "balance_report": "/api/balance-report-by-thirdparty",
    "docs": "/docs"
  }
}
```

---

## 🔍 Ver los Logs

El backend mostrará información en la consola:
- ✅ "Base de datos inicializada" - Si SQLite/PostgreSQL está configurado
- ✅ "Uvicorn running on http://0.0.0.0:8000" - Servidor iniciado
- ⚠️ Advertencias sobre PostgreSQL si no está configurado (normal si usas SQLite)

---

## ⚠️ Solución de Problemas

### Error: "No module named 'fastapi'"
**Causa:** Dependencias no instaladas

**Solución:**
```bash
cd /home/elvix/siigo-app/backend
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "venv/bin/activate: No such file or directory"
**Causa:** Entorno virtual no creado

**Solución:**
```bash
cd /home/elvix/siigo-app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Address already in use"
**Causa:** El puerto 8000 ya está en uso

**Solución:**
1. Encuentra el proceso:
   ```bash
   lsof -i :8000
   ```
2. Detén el proceso:
   ```bash
   kill <PID>
   ```
3. O cambia el puerto en `backend/config.py`

### Error: "PostgreSQL no disponible"
**Causa:** PostgreSQL no está configurado

**Solución:** 
- Es normal si usas SQLite (temporal)
- Para producción, configura PostgreSQL (ver `CONFIGURAR_POSTGRESQL.md`)

---

## 🎯 Comandos Rápidos

### Iniciar backend:
```bash
cd /home/elvix/siigo-app/backend && source venv/bin/activate && python main.py
```

### Detener backend:
Presiona `Ctrl + C` en la terminal donde está corriendo

### Verificar estado:
```bash
curl http://localhost:8000/health
```

### Ver documentación:
Abre: `http://localhost:8000/docs`

---

## 📊 Endpoints Disponibles

Una vez iniciado, tendrás acceso a:

- **Swagger UI:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`
- **Procesar por rango:** `POST /api/etl/process-date-range`
- **Ver estadísticas:** `GET /api/powerbi/stats`
- **Ver datos:** `GET /api/powerbi/balance-reports`

---

## 💡 Tips

1. **Mantén la terminal abierta:** El backend debe seguir corriendo
2. **Auto-reload activado:** Los cambios en el código se recargan automáticamente
3. **Logs en consola:** Verás todos los errores y mensajes en tiempo real
4. **Dos terminales:** Una para backend, otra para frontend

---

## 🎉 ¡Listo!

Una vez que veas:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

El backend está listo para recibir peticiones.

---

**📚 Más información:**
- `README.md` - Documentación general
- `COMO_INICIAR.md` - Guía de inicio rápido
- `DONDE_VER_INFORMACION.md` - Dónde encontrar información


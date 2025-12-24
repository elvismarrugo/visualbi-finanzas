# 🚀 Cómo Iniciar la Aplicación Siigo

## ✅ Estado Actual

- ✅ **Dependencias instaladas** en entorno virtual
- ✅ **Backend corriendo** en `http://localhost:8000`
- ✅ **Frontend corriendo** en `http://localhost:5173`

## 📝 Para Iniciar el Backend (si se detiene)

Abre una terminal y ejecuta:

```bash
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

**O usa el script de inicio:**

```bash
cd /home/elvix/siigo-app/backend
source venv/bin/activate
./start_backend.sh
```

## 🌐 URLs Disponibles

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## ✅ Verificación

Para verificar que el backend está corriendo:

```bash
curl http://localhost:8000/health
```

Deberías recibir: `{"status":"healthy"}`

## 🎯 Uso de la Aplicación

1. Abre tu navegador en `http://localhost:5173`
2. Completa el formulario con los parámetros:
   - **Año:** Ej: 2024
   - **Mes de Inicio:** 1-13
   - **Mes de Fin:** 1-13
   - **Código de Cuenta Inicial:** (Opcional)
   - **Código de Cuenta Final:** (Opcional)
   - **Incluir diferencia de impuestos:** ✓ o ✗
3. Haz clic en "Obtener Reporte"
4. Si es exitoso, verás un botón para descargar el Excel

## ⚠️ Notas Importantes

- **Siempre activa el entorno virtual** antes de ejecutar el backend:
  ```bash
  source venv/bin/activate
  ```

- Si cierras la terminal donde corre el backend, se detendrá. Necesitas iniciarlo de nuevo.

- El frontend y backend deben estar corriendo simultáneamente para que la aplicación funcione.


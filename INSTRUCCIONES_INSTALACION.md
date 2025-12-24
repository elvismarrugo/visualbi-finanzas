# 📋 Instrucciones de Instalación - Siigo App

## ⚠️ Error Actual: ERR_CONNECTION_REFUSED

El frontend está funcionando pero el backend no puede iniciarse porque faltan las dependencias de Python.

## 🔧 Solución Paso a Paso

### Paso 1: Instalar pip (Gestor de paquetes de Python)

Abre una terminal y ejecuta:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv
```

**Nota:** Necesitarás tu contraseña de administrador para ejecutar `sudo`.

### Paso 2: Instalar las Dependencias del Backend

Tienes dos opciones:

#### Opción A: Instalación Global (Más Rápida)

```bash
cd /home/elvix/siigo-app/backend
pip3 install fastapi 'uvicorn[standard]' python-dotenv httpx pydantic pydantic-settings python-multipart
```

#### Opción B: Entorno Virtual (Recomendado - Mejor Práctica)

```bash
cd /home/elvix/siigo-app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Paso 3: Iniciar el Backend

Una vez instaladas las dependencias, inicia el backend:

```bash
# Si usaste instalación global:
cd /home/elvix/siigo-app/backend
python3 main.py

# O si usaste entorno virtual (después de activarlo):
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

**O usa el script de inicio:**

```bash
cd /home/elvix/siigo-app
./start_backend.sh
```

### Paso 4: Verificar que Funciona

Deberías ver en la terminal:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Abre otra terminal y prueba:

```bash
curl http://localhost:8000/health
```

Deberías recibir: `{"status":"healthy"}`

## ✅ Estado Actual

- ✅ **Frontend:** Corriendo en `http://localhost:5173`
- ✅ **Archivo .env:** Configurado con tus credenciales
- ✅ **Código:** Listo y configurado para conectarse a Siigo API
- ❌ **Backend:** Necesita dependencias instaladas

## 🎯 Una Vez que el Backend Esté Corriendo

1. El error `ERR_CONNECTION_REFUSED` desaparecerá
2. Podrás usar el formulario en el frontend
3. Los datos se conectarán correctamente con la API de Siigo

## 📝 Notas Adicionales

- Los warnings de React Router en la consola son solo advertencias y no afectan la funcionalidad
- El mensaje "The message port closed" es de extensiones del navegador, no es un error de tu aplicación
- Una vez que el backend esté activo, todo funcionará correctamente

## 🆘 Si Tienes Problemas

1. Verifica que Python 3 esté instalado: `python3 --version`
2. Verifica que pip esté instalado: `pip3 --version`
3. Verifica que el puerto 8000 esté libre: `netstat -tuln | grep 8000`
4. Revisa los logs del backend para ver errores específicos


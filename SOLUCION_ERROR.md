# 🔧 Solución al Error: ERR_CONNECTION_REFUSED

## Problema
El frontend está intentando conectarse al backend en `http://localhost:8000`, pero el backend no está corriendo porque faltan las dependencias de Python.

## Error en la Consola
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
:8000/api/balance-report-by-thirdparty
```

## Solución Rápida

### Opción 1: Instalar pip y dependencias (Recomendado)

Abre una terminal y ejecuta estos comandos:

```bash
# 1. Instalar pip (necesitarás tu contraseña)
sudo apt update
sudo apt install -y python3-pip

# 2. Navegar al directorio del backend
cd /home/elvix/siigo-app/backend

# 3. Instalar las dependencias
pip3 install fastapi 'uvicorn[standard]' python-dotenv httpx pydantic pydantic-settings python-multipart

# 4. Iniciar el backend
python3 main.py
```

### Opción 2: Usar entorno virtual (Mejor práctica)

```bash
# 1. Instalar pip y venv
sudo apt update
sudo apt install -y python3-pip python3-venv

# 2. Crear entorno virtual
cd /home/elvix/siigo-app/backend
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Iniciar el backend
python main.py
```

## Verificación

Una vez que el backend esté corriendo, deberías ver:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Probar la Conexión

Abre otra terminal y prueba:

```bash
curl http://localhost:8000/health
```

Deberías recibir: `{"status":"healthy"}`

## Notas

- El frontend ya está corriendo en `http://localhost:5173`
- Una vez que el backend esté activo, el error `ERR_CONNECTION_REFUSED` desaparecerá
- Los otros warnings de React Router son solo advertencias y no afectan la funcionalidad


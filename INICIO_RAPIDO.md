# 🚀 Inicio Rápido - Siigo App

## ⚠️ Error Actual: Backend No Está Corriendo

Estás viendo el error `ERR_CONNECTION_REFUSED` porque el backend no está activo.

## ✅ Solución en 3 Pasos

### 1️⃣ Instalar pip (si no lo tienes)

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv
```

### 2️⃣ Instalar Dependencias del Backend

```bash
cd /home/elvix/siigo-app/backend
pip3 install fastapi 'uvicorn[standard]' python-dotenv httpx pydantic pydantic-settings python-multipart
```

**O usando entorno virtual (recomendado):**

```bash
cd /home/elvix/siigo-app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Iniciar el Backend

```bash
# Si instalaste globalmente:
cd /home/elvix/siigo-app/backend
python3 main.py

# O si usas entorno virtual:
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

## ✅ Verificación

Una vez iniciado, deberías ver:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Luego prueba en otra terminal:

```bash
curl http://localhost:8000/health
```

Deberías recibir: `{"status":"healthy"}`

## 🎯 Estado Actual

- ✅ Frontend: Corriendo en `http://localhost:5173`
- ❌ Backend: **Necesita iniciarse** (puerto 8000)

## 📝 Nota

El frontend ya está funcionando. Solo necesitas iniciar el backend y el error desaparecerá.


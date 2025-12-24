# ⚠️ Error: Invalid value: access_key

## Problema Identificado

El backend está recibiendo un error 400 de la API de Siigo indicando que el `access_key` no es válido:

```
{"status":400,"errors":[{"code":"invalid_value","message":"Invalid value: access_key"}]}
```

## Posibles Causas

1. **Access Key incorrecto o expirado**: El access_key proporcionado puede no ser válido
2. **Formato incorrecto**: El access_key puede necesitar ser procesado de alguna manera
3. **Credenciales incorrectas**: El access_key puede no corresponder al username proporcionado

## Solución

### Opción 1: Verificar las Credenciales en Siigo

1. Accede al portal de Siigo Nube
2. Ve a **Configuración > Alianzas e integraciones > Credenciales de integración**
3. Verifica que el `access_key` y `username` sean correctos
4. Si es necesario, genera nuevas credenciales

### Opción 2: Verificar el Formato del Access Key

El access_key debe ser una cadena alfanumérica. Asegúrate de que:
- No tenga espacios al inicio o final
- Esté completo (no cortado)
- Sea el access_key correcto para el username `coomulgar@hotmail.com`

### Opción 3: Verificar el Archivo .env

Asegúrate de que el archivo `.env` tenga el formato correcto:

```env
SIIGO_ACCESS_KEY=tu_access_key_completo_sin_espacios
SIIGO_PARTNER_ID=SiigoApiCoomulgar
SIIGO_BASE_URL=https://api.siigo.com
SIIGO_USERNAME=coomulgar@hotmail.com
BACKEND_PORT=8000
```

## Verificación

Una vez corregido el access_key, reinicia el backend:

```bash
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

Luego prueba nuevamente el formulario en el frontend.

## Nota

El error ahora se muestra claramente en el frontend gracias a las mejoras en el manejo de errores. El mensaje de error te indicará exactamente qué está fallando.


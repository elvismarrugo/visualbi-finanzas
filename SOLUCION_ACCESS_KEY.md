# 🔑 Solución: Error "Invalid value: access_key"

## Problema Identificado

El error `400 Bad Request` con el mensaje `"Invalid value: access_key"` indica que el `access_key` en tu archivo `.env` **no es válido** o **no corresponde** al `username` proporcionado.

## ✅ Solución Paso a Paso

### 1. Verificar Credenciales en Siigo Nube

1. Accede a **Siigo Nube** (https://siigonube.com)
2. Inicia sesión con tu cuenta
3. Ve a **Configuración** → **Alianzas e integraciones** → **Mi Credencial API**
4. Verifica que:
   - El **username** sea: `coomulgar@hotmail.com`
   - El **access_key** sea el correcto (copia el valor completo)
   - Las credenciales estén **activas** y **no expiradas**

### 2. Actualizar el Archivo .env

Abre el archivo `.env` en la raíz del proyecto y actualiza con las credenciales correctas:

```env
SIIGO_ACCESS_KEY=tu_access_key_correcto_aqui
SIIGO_PARTNER_ID=SiigoApiCoomulgar
SIIGO_BASE_URL=https://api.siigo.com
SIIGO_USERNAME=coomulgar@hotmail.com
BACKEND_PORT=8000
```

**⚠️ Importante:**
- No agregues espacios antes o después del `=`
- No uses comillas alrededor de los valores
- El `access_key` debe ser el valor completo sin cortar
- Asegúrate de que no haya caracteres especiales invisibles

### 3. Regenerar Credenciales (Si es Necesario)

Si las credenciales no funcionan:

1. En Siigo Nube, ve a **Mi Credencial API**
2. Haz clic en **Regenerar** o **Generar nueva credencial**
3. **Copia el nuevo `access_key`** inmediatamente (solo se muestra una vez)
4. Actualiza el archivo `.env` con el nuevo valor

### 4. Reiniciar el Backend

Después de actualizar el `.env`:

```bash
# Detén el backend actual (Ctrl+C)
# Luego reinícialo:
cd /home/elvix/siigo-app/backend
source venv/bin/activate
python main.py
```

### 5. Probar la Autenticación

Una vez reiniciado, prueba el formulario nuevamente. Si el `access_key` es correcto, deberías poder autenticarte exitosamente.

## 🔍 Verificación del Formato

El `access_key` debe:
- Ser una cadena alfanumérica
- No tener espacios
- Estar completo (no cortado)
- Corresponder al `username` especificado

## 📝 Notas Importantes

1. **El `access_key` NO es tu contraseña de Siigo Nube**
   - Es una credencial especial generada desde el menú de API
   - Se genera específicamente para integraciones

2. **El `access_key` puede expirar**
   - Si no funciona, puede que haya expirado
   - Regenera nuevas credenciales si es necesario

3. **El `Partner-Id` debe coincidir**
   - Verifica que `SiigoApiCoomulgar` sea el Partner-Id correcto
   - Este valor también se encuentra en Siigo Nube

## ✅ Una Vez Corregido

Cuando el `access_key` sea válido:
- La autenticación funcionará correctamente
- Podrás obtener tokens de acceso
- El formulario podrá consultar los reportes de Siigo


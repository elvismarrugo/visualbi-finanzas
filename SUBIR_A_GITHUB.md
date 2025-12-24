# 🚀 Cómo Subir el Código a GitHub - Guía Rápida

## ⚠️ Estado Actual

**El código AÚN NO está en GitHub.** Necesitas seguir estos pasos:

## 📋 Pasos para Subir a GitHub

### Paso 1: Crear el Repositorio en GitHub

1. **Abre tu navegador** y ve a: https://github.com
2. **Inicia sesión** en tu cuenta
3. **Crea el repositorio:**
   - Haz clic en el botón **"+"** (arriba derecha)
   - Selecciona **"New repository"**
   - **Nombre:** `visualbi-finanzas`
   - **Descripción:** "Sistema de reportes y ETL para Siigo"
   - **IMPORTANTE:** NO marques "Initialize with README" (ya tenemos uno)
   - Elige si será **público** o **privado**
   - Haz clic en **"Create repository"**

### Paso 2: Conectar tu Repositorio Local con GitHub

Después de crear el repositorio, GitHub te mostrará instrucciones. Ejecuta estos comandos:

```bash
cd /home/elvix/siigo-app

# Reemplaza TU_USUARIO con tu nombre de usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/visualbi-finanzas.git

# Verificar que se agregó correctamente
git remote -v
```

**Ejemplo:**
Si tu usuario es `elvix`, sería:
```bash
git remote add origin https://github.com/elvix/visualbi-finanzas.git
```

### Paso 3: Subir el Código

```bash
# Asegúrate de estar en la rama main
git branch -M main

# Subir el código a GitHub
git push -u origin main
```

### Paso 4: Verificar que se Subió

#### Opción A: Desde la Terminal
```bash
git status
```

**Deberías ver:**
```
Your branch is up to date with 'origin/main'
```

#### Opción B: Desde GitHub Web
1. Ve a: `https://github.com/TU_USUARIO/visualbi-finanzas`
2. Deberías ver todos tus archivos (README.md, backend/, frontend/, etc.)

## 🔐 Si GitHub Pide Autenticación

### Para HTTPS (recomendado):
GitHub ya no acepta contraseñas. Necesitas un **Personal Access Token**:

1. Ve a: https://github.com/settings/tokens
2. Haz clic en **"Generate new token"** → **"Generate new token (classic)"**
3. Dale un nombre (ej: "visualbi-finanzas")
4. Selecciona el scope **`repo`** (acceso completo a repositorios)
5. Haz clic en **"Generate token"**
6. **Copia el token** (solo se muestra una vez)
7. Cuando git pida contraseña, **pega el token** en lugar de la contraseña

### Para SSH (alternativa):
Si tienes SSH configurado, puedes usar:
```bash
git remote add origin git@github.com:TU_USUARIO/visualbi-finanzas.git
```

## ✅ Verificación Final

Después de hacer push, ejecuta:

```bash
cd /home/elvix/siigo-app

# Verificar remote
git remote -v

# Verificar estado
git status

# Verificar rama
git branch -vv
```

**Deberías ver:**
- ✅ Remote `origin` configurado
- ✅ Rama `main` conectada a `origin/main`
- ✅ Estado "up to date"

## 🆘 Solución de Problemas

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/visualbi-finanzas.git
```

### Error: "failed to push some refs"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: "authentication failed"
- Verifica que estés usando un Personal Access Token, no tu contraseña
- O configura SSH

## 📝 Comandos Rápidos (Copia y Pega)

```bash
cd /home/elvix/siigo-app

# 1. Agregar remote (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/visualbi-finanzas.git

# 2. Verificar
git remote -v

# 3. Subir
git push -u origin main

# 4. Verificar que se subió
git status
```

## 🎯 Resumen

1. ✅ **Código local:** Listo (2 commits)
2. ⏳ **Repositorio GitHub:** Necesitas crearlo
3. ⏳ **Conexión:** Necesitas hacer `git remote add`
4. ⏳ **Subir código:** Necesitas hacer `git push`

Una vez que completes estos pasos, tu código estará en GitHub! 🚀


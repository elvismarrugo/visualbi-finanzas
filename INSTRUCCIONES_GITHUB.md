# 🚀 Instrucciones para Subir a GitHub

## ✅ Pasos Completados

1. ✅ Repositorio git inicializado
2. ✅ Archivos agregados
3. ✅ Commit inicial creado

## 📋 Próximos Pasos

### Opción 1: Crear Repositorio desde GitHub Web (Recomendado)

1. **Ve a GitHub:**
   - Abre https://github.com
   - Inicia sesión en tu cuenta

2. **Crea el repositorio:**
   - Haz clic en el botón "+" (arriba derecha)
   - Selecciona "New repository"
   - Nombre: `visualbi-finanzas`
   - Descripción: "Sistema de reportes y ETL para Siigo"
   - **NO marques** "Initialize with README" (ya tenemos uno)
   - Elige si será público o privado
   - Haz clic en "Create repository"

3. **Conecta tu repositorio local:**
   ```bash
   cd /home/elvix/siigo-app
   git remote add origin https://github.com/TU_USUARIO/visualbi-finanzas.git
   git branch -M main
   git push -u origin main
   ```

   **Nota:** Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub

### Opción 2: Usar GitHub CLI (si lo tienes instalado)

```bash
cd /home/elvix/siigo-app
gh repo create visualbi-finanzas --public --source=. --remote=origin --push
```

### Opción 3: Usar SSH (si tienes SSH configurado)

```bash
cd /home/elvix/siigo-app
git remote add origin git@github.com:TU_USUARIO/visualbi-finanzas.git
git branch -M main
git push -u origin main
```

## 🔐 Autenticación

Si GitHub te pide autenticación:

### Para HTTPS:
- Usa un Personal Access Token en lugar de tu contraseña
- Crea uno en: GitHub Settings > Developer settings > Personal access tokens

### Para SSH:
- Asegúrate de tener tu clave SSH configurada en GitHub

## ✅ Verificación

Después de hacer push, verifica en:
```
https://github.com/TU_USUARIO/visualbi-finanzas
```

## 📝 Comandos Útiles

### Ver el estado actual:
```bash
git status
```

### Ver commits:
```bash
git log --oneline
```

### Agregar cambios futuros:
```bash
git add .
git commit -m "Descripción de los cambios"
git push
```

### Ver remotos configurados:
```bash
git remote -v
```

## ⚠️ Recordatorios Importantes

1. **NUNCA subas el archivo `.env`** - Contiene credenciales sensibles
2. El `.gitignore` ya está configurado para excluir archivos sensibles
3. Revisa siempre con `git status` antes de hacer commit
4. Usa mensajes de commit descriptivos

## 🆘 Si Tienes Problemas

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


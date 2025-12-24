#!/bin/bash
# Script para conectar y subir el repositorio a GitHub
# Reemplaza TU_USUARIO con tu nombre de usuario de GitHub

echo "🚀 Conectando repositorio con GitHub..."
echo ""

# Reemplaza TU_USUARIO con tu usuario de GitHub
GITHUB_USER="TU_USUARIO"
REPO_NAME="visualbi-finanzas"

# Agregar remote (si no existe)
if ! git remote | grep -q origin; then
    echo "📡 Agregando remote origin..."
    git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git
    echo "✅ Remote agregado"
else
    echo "⚠️  Remote 'origin' ya existe"
    echo "Si necesitas cambiarlo, ejecuta:"
    echo "  git remote remove origin"
    echo "  git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
fi

echo ""
echo "📤 Subiendo código a GitHub..."
echo ""

# Cambiar a rama main
git branch -M main

# Hacer push
git push -u origin main

echo ""
echo "✅ ¡Listo! Tu código está en GitHub"
echo "🌐 Visita: https://github.com/${GITHUB_USER}/${REPO_NAME}"


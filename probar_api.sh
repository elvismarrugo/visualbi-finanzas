#!/bin/bash
# Script para probar la API paso a paso
# Ejecutar con: bash probar_api.sh

echo "🧪 Probando la API de Siigo..."
echo ""

BASE_URL="http://localhost:8000"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Verificar que el backend está corriendo
echo -e "${BLUE}1. Verificando que el backend está corriendo...${NC}"
HEALTH=$(curl -s "$BASE_URL/health" 2>&1)
if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Backend está corriendo${NC}"
else
    echo -e "${YELLOW}❌ Backend no está corriendo. Inicia el backend primero.${NC}"
    exit 1
fi
echo ""

# 2. Ver estadísticas actuales
echo -e "${BLUE}2. Estadísticas actuales de la base de datos:${NC}"
STATS=$(curl -s "$BASE_URL/api/powerbi/stats")
echo "$STATS" | python3 -m json.tool 2>/dev/null || echo "$STATS"
echo ""

# 3. Preguntar si quiere procesar datos
echo -e "${YELLOW}¿Quieres procesar datos ahora? (s/n)${NC}"
read -r respuesta

if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
    echo ""
    echo -e "${BLUE}3. Procesando datos...${NC}"
    echo -e "${YELLOW}   Esto puede tardar varios minutos...${NC}"
    echo ""
    
    # Procesar solo 1 mes para prueba rápida
    RESULT=$(curl -s -X POST "$BASE_URL/api/etl/process-year" \
        -H "Content-Type: application/json" \
        -d '{
            "year": 2024,
            "month_start": 1,
            "month_end": 1,
            "includes_tax_diff": false,
            "clear_existing": true
        }')
    
    echo "$RESULT" | python3 -m json.tool 2>/dev/null || echo "$RESULT"
    echo ""
    
    # 4. Ver estadísticas después de procesar
    echo -e "${BLUE}4. Estadísticas después de procesar:${NC}"
    sleep 2
    STATS_AFTER=$(curl -s "$BASE_URL/api/powerbi/stats")
    echo "$STATS_AFTER" | python3 -m json.tool 2>/dev/null || echo "$STATS_AFTER"
    echo ""
    
    # 5. Ver algunos registros
    echo -e "${BLUE}5. Primeros 5 registros:${NC}"
    DATA=$(curl -s "$BASE_URL/api/powerbi/balance-reports?limit=5")
    echo "$DATA" | python3 -m json.tool 2>/dev/null || echo "$DATA"
else
    echo ""
    echo -e "${YELLOW}Para procesar datos manualmente:${NC}"
    echo ""
    echo "Opción 1 - Desde Swagger UI:"
    echo "  1. Abre: http://localhost:8000/docs"
    echo "  2. Busca: POST /api/etl/process-year"
    echo "  3. Haz clic en 'Try it out'"
    echo "  4. Ingresa los parámetros y ejecuta"
    echo ""
    echo "Opción 2 - Desde línea de comandos:"
    echo "  curl -X POST \"$BASE_URL/api/etl/process-year\" \\"
    echo "    -H \"Content-Type: application/json\" \\"
    echo "    -d '{\"year\": 2024, \"month_start\": 1, \"month_end\": 3, \"clear_existing\": true}'"
fi

echo ""
echo -e "${GREEN}✅ Prueba completada${NC}"
echo ""
echo "📚 Más información: COMO_USAR_LA_API.md"


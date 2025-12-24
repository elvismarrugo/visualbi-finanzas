# Siigo App - Aplicación de Reportes Siigo

Aplicación web completa para consultar y gestionar reportes de la API de Siigo.

## 📋 Requisitos Previos

- **Python** 3.8 o superior
- **Node.js** 16 o superior y npm
- Credenciales de acceso a la API de Siigo:
  - Access Key
  - Partner ID
  - Username
  - Base URL de la API

## 🏗️ Estructura del Proyecto

```
siigo-app/
├── backend/              # API FastAPI
│   ├── main.py          # Aplicación principal FastAPI
│   ├── config.py        # Configuración y variables de entorno
│   ├── models.py        # Modelos Pydantic para validación
│   ├── siigo_client.py  # Cliente para comunicación con Siigo API
│   └── requirements.txt # Dependencias de Python
├── frontend/            # React + Vite
│   ├── src/             # Código fuente de React
│   ├── public/          # Archivos estáticos
│   └── package.json     # Dependencias de Node.js
└── .env                 # Credenciales (NO subir a git)
```

## ⚙️ Configuración

1. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
SIIGO_ACCESS_KEY=tu_access_key
SIIGO_PARTNER_ID=tu_partner_id
SIIGO_BASE_URL=https://api.siigo.com
SIIGO_USERNAME=tu_usuario
BACKEND_PORT=8000
```

**⚠️ Importante:** Nunca subas el archivo `.env` a git. Contiene información sensible.

## 🚀 Instalación

### Backend

1. Navega al directorio del backend:
```bash
cd backend
```

2. Crea un entorno virtual de Python:
```bash
python -m venv venv
```

3. Activa el entorno virtual:
```bash
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Ejecuta el servidor:
```bash
python main.py
```

El backend estará disponible en `http://localhost:8000`

### Frontend

1. Navega al directorio del frontend:
```bash
cd frontend
```

2. Instala las dependencias:
```bash
npm install
```

3. Ejecuta el servidor de desarrollo:
```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

## 📚 Uso de la API

### Endpoints Disponibles

#### `GET /`
Información general de la API y endpoints disponibles.

#### `GET /health`
Verifica el estado de salud del servidor.

#### `POST /api/balance-report-by-thirdparty`
Obtiene el reporte de balance por terceros de Siigo.

**Parámetros del cuerpo (JSON):**
```json
{
  "year": 2024,
  "month_start": 1,
  "month_end": 12,
  "account_start": "1105",
  "account_end": "1105",
  "includes_tax_diff": false
}
```

**Parámetros:**
- `year` (int): Año del reporte (2000-2100)
- `month_start` (int): Mes de inicio (1-12)
- `month_end` (int): Mes de fin (1-12)
- `account_start` (str): Código de cuenta inicial
- `account_end` (str): Código de cuenta final
- `includes_tax_diff` (bool): Incluir diferencia de impuestos (opcional, default: false)

**Ejemplo de respuesta exitosa:**
```json
{
  "results": [...],
  "metadata": {...}
}
```

### Documentación Interactiva

Una vez que el backend esté corriendo, puedes acceder a la documentación interactiva de la API en:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido para Python
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Pydantic**: Validación de datos y configuración
- **httpx**: Cliente HTTP asíncrono para comunicarse con la API de Siigo
- **python-dotenv**: Manejo de variables de entorno

### Frontend
- **React 19**: Biblioteca para construir interfaces de usuario
- **Vite**: Herramienta de construcción rápida para desarrollo frontend
- **Axios**: Cliente HTTP para realizar peticiones al backend
- **ESLint**: Herramienta de análisis de código

## ✨ Funcionalidades Actuales

- ✅ Reporte de balance por terceros (`/api/balance-report-by-thirdparty`)
- ✅ **Sistema ETL completo** para procesar y almacenar reportes en PostgreSQL
- ✅ **API para Power BI** con endpoints de consulta y estadísticas
- ✅ Procesamiento mes por mes (replica lógica de PowerQuery)
- ✅ Documentación interactiva de la API (Swagger/ReDoc)
- ✅ Validación de datos con Pydantic
- ✅ Manejo de errores y respuestas HTTP apropiadas
- ✅ CORS configurado para desarrollo frontend

## 🔮 Próximas Funcionalidades

- [ ] Más reportes de Siigo
- [ ] Dashboard de visualización de datos
- [ ] Exportación a Excel/PDF
- [ ] Autenticación y autorización de usuarios
- [ ] Caché de respuestas para mejorar rendimiento
- [ ] Tests unitarios y de integración
- [ ] Logging y monitoreo
- [ ] Optimización de consultas para grandes volúmenes de datos

## 📊 Sistema ETL y Base de Datos

El sistema incluye un módulo ETL completo que:

1. **Descarga reportes de Siigo** mes por mes
2. **Procesa archivos Excel** con transformaciones ETL
3. **Almacena en PostgreSQL** para consultas rápidas
4. **Expone API para Power BI** con filtros y paginación

Ver documentación completa en: [README_ETL.md](README_ETL.md)

### Endpoints ETL Disponibles

- `POST /api/etl/process-year` - Procesa año actual mes por mes
- `POST /api/etl/process-previous-year` - Procesa año anterior completo
- `GET /api/powerbi/balance-reports` - Consulta datos para Power BI
- `GET /api/powerbi/stats` - Estadísticas agregadas

## 🧪 Desarrollo

### Scripts Disponibles

**Backend:**
- `python main.py`: Ejecuta el servidor en modo desarrollo con recarga automática

**Frontend:**
- `npm run dev`: Ejecuta el servidor de desarrollo
- `npm run build`: Construye la aplicación para producción
- `npm run lint`: Ejecuta el linter para verificar el código
- `npm run preview`: Previsualiza la build de producción

### Estructura de Código

El proyecto sigue una arquitectura separada entre backend y frontend:

- **Backend**: API RESTful que actúa como intermediario entre el frontend y la API de Siigo
- **Frontend**: Aplicación React que consume los endpoints del backend

## 🐛 Solución de Problemas

### Error de autenticación (401)
- Verifica que las credenciales en el archivo `.env` sean correctas
- Asegúrate de que el archivo `.env` esté en la raíz del proyecto

### Error de conexión con el backend
- Verifica que el backend esté corriendo en el puerto configurado (por defecto 8000)
- Revisa la configuración de CORS si estás usando un puerto diferente para el frontend

### Dependencias no instaladas
- Asegúrate de haber activado el entorno virtual antes de instalar dependencias del backend
- Ejecuta `npm install` nuevamente en el directorio del frontend

## 📝 Notas

- El backend se ejecuta por defecto en el puerto `8000`
- El frontend se ejecuta por defecto en el puerto `5173` (Vite)
- Los cambios en el código del backend se recargan automáticamente gracias a `reload=True` en uvicorn

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Crea un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso privado.

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from sqlalchemy.orm import Session
from typing import Optional, List
from siigo_client import SiigoClient
from models import (
    BalanceReportRequest, 
    ErrorResponse,
    ETLProcessRequest,
    ETLPreviousYearRequest,
    ETLProcessDateRangeRequest,
    PowerBIQueryParams
)
from config import get_settings
from database import get_db, BalanceReport, init_db
from etl_service import ETLService

app = FastAPI(
    title="Siigo API Integration",
    description="API para integración con Siigo - Reportes y Consultas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

siigo_client = SiigoClient()

# Inicializar ETL service y BD solo si PostgreSQL está disponible
try:
    etl_service = ETLService()
    # Intentar inicializar BD (puede fallar si PostgreSQL no está corriendo)
    try:
        init_db()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"⚠️  Base de datos no disponible: {e}")
        print("   Los endpoints ETL no estarán disponibles hasta configurar PostgreSQL")
except Exception as e:
    print(f"⚠️  ETL Service no disponible: {e}")
    etl_service = None


@app.get("/")
async def root():
    return {
        "message": "Siigo API Integration",
        "version": "1.0.0",
        "endpoints": {
            "balance_report": "/api/balance-report-by-thirdparty",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/balance-report-by-thirdparty", response_model=dict)
async def get_balance_report(request: BalanceReportRequest):
    """
    Obtiene el reporte de balance por terceros de Siigo usando el endpoint test-balance-report-by-thirdparty

    - **year**: Año del reporte (2000-2100, obligatorio)
    - **month_start**: Mes de inicio (1-13, obligatorio)
    - **month_end**: Mes de fin (1-13, obligatorio)
    - **account_start**: Código de cuenta inicial (opcional)
    - **account_end**: Código de cuenta final (opcional)
    - **includes_tax_diff**: Incluir diferencia de impuestos (obligatorio, true/false)
    
    Retorna un objeto con file_id y file_url para descargar el reporte en Excel.
    """
    try:
        if request.month_start > request.month_end:
            raise HTTPException(
                status_code=400,
                detail="El mes de inicio no puede ser mayor al mes de fin"
            )

        # Pasar los valores, None será manejado por el cliente de Siigo
        result = await siigo_client.get_balance_report_by_thirdparty(
            year=request.year,
            month_start=request.month_start,
            month_end=request.month_end,
            account_start=request.account_start or "",  # Convertir None a string vacío
            account_end=request.account_end or "",      # Convertir None a string vacío
            includes_tax_diff=request.includes_tax_diff
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        error_message = str(e)
        # Imprimir el error completo en la consola del servidor para debugging
        print(f"ERROR en get_balance_report: {error_message}")
        
        # Determinar el código de estado HTTP basado en el mensaje de error
        if "401" in error_message or "autenticación" in error_message.lower():
            raise HTTPException(
                status_code=401,
                detail=f"Error de autenticación con Siigo: {error_message}"
            )
        elif "404" in error_message:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron datos: {error_message}"
            )
        elif "400" in error_message or "Bad Request" in error_message:
            raise HTTPException(
                status_code=400,
                detail=f"Error en la petición: {error_message}"
            )
        else:
            # Para otros errores, devolver 500 con el mensaje completo
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener el reporte: {error_message}"
            )


# ==========================
# Endpoints ETL
# ==========================

@app.post("/api/etl/process-year", response_model=dict)
async def process_year_etl(request: ETLProcessRequest):
    """
    Procesa reportes de Siigo mes por mes para un año y los guarda en PostgreSQL
    Replica la primera query de PowerQuery
    """
    if etl_service is None:
        raise HTTPException(
            status_code=503,
            detail="Servicio ETL no disponible. PostgreSQL no está configurado o no está corriendo."
        )
    try:
        result = await etl_service.process_year_report(
            year=request.year,
            month_start=request.month_start or 1,
            month_end=request.month_end or 12,
            account_start=request.account_start,
            account_end=request.account_end,
            includes_tax_diff=request.includes_tax_diff,
            clear_existing=request.clear_existing
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en procesamiento ETL: {str(e)}"
        )


@app.post("/api/etl/process-previous-year", response_model=dict)
async def process_previous_year_etl(request: ETLPreviousYearRequest):
    """
    Procesa el año anterior completo (12 meses)
    Replica la segunda y tercera query de PowerQuery
    """
    if etl_service is None:
        raise HTTPException(
            status_code=503,
            detail="Servicio ETL no disponible. PostgreSQL no está configurado o no está corriendo."
        )
    try:
        result = await etl_service.process_previous_year(
            year_base=request.year_base,
            account_start=request.account_start,
            account_end=request.account_end,
            includes_tax_diff=request.includes_tax_diff,
            clear_existing=request.clear_existing
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en procesamiento ETL año anterior: {str(e)}"
        )


@app.post("/api/etl/process-date-range", response_model=dict)
async def process_date_range_etl(request: ETLProcessDateRangeRequest):
    """
    Procesa reportes desde 2024-01-31 hasta la fecha de fin proporcionada
    Replica la lógica de PowerQuery con rango de fechas
    
    Ejemplo: Si fecha_fin es 2025-09-30, procesa desde 2024-01-31 hasta 2025-09-30
    """
    if etl_service is None:
        raise HTTPException(
            status_code=503,
            detail="Servicio ETL no disponible. PostgreSQL no está configurado o no está corriendo."
        )
    try:
        result = await etl_service.process_date_range(
            fecha_fin=request.fecha_fin,
            account_start=request.account_start,
            account_end=request.account_end,
            includes_tax_diff=request.includes_tax_diff,
            clear_existing=request.clear_existing
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en procesamiento ETL por rango de fechas: {str(e)}"
        )


# ==========================
# Endpoints para Power BI
# ==========================

@app.get("/api/powerbi/balance-reports")
async def get_balance_reports_powerbi(
    año: Optional[int] = Query(None, description="Filtrar por año"),
    periodo: Optional[int] = Query(None, description="Filtrar por periodo (AAAAMM)"),
    codigo_cuenta: Optional[int] = Query(None, description="Filtrar por código de cuenta"),
    cod_relacional: Optional[str] = Query(None, description="Filtrar por código relacional"),
    identificacion: Optional[str] = Query(None, description="Filtrar por identificación"),
    limit: int = Query(1000, ge=1, le=10000, description="Límite de registros"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para Power BI - Obtiene datos de balance reports con filtros
    """
    try:
        query = db.query(BalanceReport)
        
        # Aplicar filtros
        if año is not None:
            query = query.filter(BalanceReport.año == año)
        if periodo is not None:
            query = query.filter(BalanceReport.periodo == periodo)
        if codigo_cuenta is not None:
            query = query.filter(BalanceReport.codigo_cuenta_contable == codigo_cuenta)
        if cod_relacional is not None:
            query = query.filter(BalanceReport.cod_relacional == cod_relacional)
        if identificacion is not None:
            query = query.filter(BalanceReport.identificacion == identificacion)
        
        # Aplicar paginación
        total = query.count()
        results = query.offset(offset).limit(limit).all()
        
        # Convertir a diccionarios
        data = []
        for record in results:
            data.append({
                "id": record.id,
                "codigo_cuenta_contable": record.codigo_cuenta_contable,
                "nombre_cuenta_contable": record.nombre_cuenta_contable,
                "cod_relacional": record.cod_relacional,
                "identificacion": record.identificacion,
                "sucursal": record.sucursal,
                "nombre_tercero": record.nombre_tercero,
                "saldo_inicial": float(record.saldo_inicial) if record.saldo_inicial else None,
                "movimiento_debito": float(record.movimiento_debito) if record.movimiento_debito else None,
                "movimiento_credito": float(record.movimiento_credito) if record.movimiento_credito else None,
                "movimiento": float(record.movimiento) if record.movimiento else None,
                "saldo_final": float(record.saldo_final) if record.saldo_final else None,
                "fecha": record.fecha.isoformat() if record.fecha else None,
                "año": record.año,
                "periodo": record.periodo,
                "created_at": record.created_at.isoformat() if record.created_at else None
            })
        
        return {
            "data": data,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener datos: {str(e)}"
        )


@app.get("/api/powerbi/stats")
async def get_stats_powerbi(
    año: Optional[int] = Query(None, description="Filtrar por año"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para Power BI - Estadísticas agregadas
    """
    try:
        query = db.query(BalanceReport)
        
        if año is not None:
            query = query.filter(BalanceReport.año == año)
        
        from sqlalchemy import func
        
        total_records = query.count()
        total_saldo_final = query.with_entities(
            func.sum(BalanceReport.saldo_final)
        ).scalar() or 0
        
        # Agrupar por año
        years = db.query(BalanceReport.año).distinct().all()
        years_list = [y[0] for y in years if y[0] is not None]
        
        # Agrupar por periodo
        periods = db.query(BalanceReport.periodo).distinct().all()
        periods_list = [p[0] for p in periods if p[0] is not None]
        
        return {
            "total_records": total_records,
            "total_saldo_final": float(total_saldo_final),
            "years": sorted(years_list),
            "periods": sorted(periods_list)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.backend_port,
        reload=True
    )

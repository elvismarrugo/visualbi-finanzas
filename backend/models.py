from pydantic import BaseModel, Field
from typing import Optional


class BalanceReportRequest(BaseModel):
    year: int = Field(..., ge=2000, le=2100, description="Año del reporte (obligatorio)")
    month_start: int = Field(..., ge=1, le=13, description="Mes de inicio (1-13, obligatorio)")
    month_end: int = Field(..., ge=1, le=13, description="Mes de fin (1-13, obligatorio)")
    account_start: Optional[str] = Field(None, description="Código de cuenta inicial (opcional)")
    account_end: Optional[str] = Field(None, description="Código de cuenta final (opcional)")
    includes_tax_diff: bool = Field(..., description="Incluir diferencia de impuestos (obligatorio)")

    class Config:
        json_schema_extra = {
            "example": {
                "year": 2024,
                "month_start": 1,
                "month_end": 12,
                "account_start": "1105",
                "account_end": "1199",
                "includes_tax_diff": False
            }
        }


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


class ETLProcessRequest(BaseModel):
    """Request para procesar reportes ETL"""
    year: int = Field(..., ge=2000, le=2100, description="Año del reporte")
    month_start: Optional[int] = Field(1, ge=1, le=13, description="Mes de inicio (1-13, default: 1)")
    month_end: Optional[int] = Field(12, ge=1, le=13, description="Mes de fin (1-13, default: 12)")
    account_start: Optional[str] = Field(None, description="Código de cuenta inicial (opcional)")
    account_end: Optional[str] = Field(None, description="Código de cuenta final (opcional)")
    includes_tax_diff: bool = Field(False, description="Incluir diferencia de impuestos")
    clear_existing: bool = Field(True, description="Eliminar datos existentes antes de insertar")


class ETLPreviousYearRequest(BaseModel):
    """Request para procesar año anterior"""
    year_base: int = Field(..., ge=2000, le=2100, description="Año base (se procesará year_base - 1)")
    account_start: Optional[str] = Field(None, description="Código de cuenta inicial (opcional)")
    account_end: Optional[str] = Field(None, description="Código de cuenta final (opcional)")
    includes_tax_diff: bool = Field(False, description="Incluir diferencia de impuestos")
    clear_existing: bool = Field(True, description="Eliminar datos existentes antes de insertar")


class PowerBIQueryParams(BaseModel):
    """Parámetros de consulta para Power BI"""
    año: Optional[int] = None
    periodo: Optional[int] = None
    codigo_cuenta: Optional[int] = None
    cod_relacional: Optional[str] = None
    identificacion: Optional[str] = None
    limit: int = Field(1000, ge=1, le=10000)
    offset: int = Field(0, ge=0)

"""
Servicio ETL para procesar reportes de Siigo mes por mes
Replica la lógica de PowerQuery
"""
import asyncio
from typing import List, Optional
from datetime import date
import pandas as pd
from siigo_client import SiigoClient
from excel_processor import ExcelProcessor
from database import get_db_session, BalanceReport, init_db, get_db_engine
from sqlalchemy import delete


class ETLService:
    """Servicio para procesar y guardar reportes de Siigo en PostgreSQL"""
    
    def __init__(self):
        self.siigo_client = SiigoClient()
        self.excel_processor = ExcelProcessor()
    
    async def process_year_report(
        self,
        year: int,
        month_start: int = 1,
        month_end: int = 12,
        account_start: Optional[str] = None,
        account_end: Optional[str] = None,
        includes_tax_diff: bool = False,
        clear_existing: bool = True
    ) -> dict:
        """
        Procesa reportes mes por mes para un año completo y los guarda en PostgreSQL
        
        Args:
            year: Año del reporte
            month_start: Mes de inicio (1-13)
            month_end: Mes de fin (1-13)
            account_start: Código de cuenta inicial (opcional)
            account_end: Código de cuenta final (opcional)
            includes_tax_diff: Incluir diferencia de impuestos
            clear_existing: Si True, elimina datos existentes del mismo año antes de insertar
            
        Returns:
            Diccionario con estadísticas del procesamiento
        """
        # Normalizar rango de meses
        start_m = min(month_start, month_end)
        end_m = max(month_start, month_end)
        months = list(range(start_m, end_m + 1))
        
        # Obtener token una sola vez
        token = await self.siigo_client.get_access_token()
        
        # Inicializar base de datos si no existe
        init_db()
        
        # Eliminar datos existentes si se solicita
        if clear_existing:
            await self._clear_year_data(year, months)
        
        total_rows = 0
        processed_months = []
        errors = []
        
        # Procesar cada mes
        for month in months:
            try:
                # Solicitar reporte para el mes específico (m..m)
                result = await self.siigo_client.get_balance_report_by_thirdparty(
                    year=year,
                    month_start=month,
                    month_end=month,
                    account_start=account_start or "",
                    account_end=account_end or "",
                    includes_tax_diff=includes_tax_diff
                )
                
                file_url = result.get('file_url')
                if not file_url:
                    errors.append(f"Mes {month}: No se recibió file_url")
                    continue
                
                # Descargar Excel
                excel_content = await self.excel_processor.download_excel(file_url)
                
                # Procesar Excel
                df = self.excel_processor.process_excel(excel_content, year, month)
                
                # Guardar en PostgreSQL
                rows_inserted = await self._save_to_database(df)
                total_rows += rows_inserted
                processed_months.append(month)
                
            except Exception as e:
                error_msg = f"Mes {month}: {str(e)}"
                errors.append(error_msg)
                print(f"ERROR procesando mes {month}: {e}")
        
        return {
            "year": year,
            "months_processed": processed_months,
            "total_rows": total_rows,
            "errors": errors,
            "success": len(errors) == 0
        }
    
    async def process_previous_year(
        self,
        year_base: int,
        account_start: Optional[str] = None,
        account_end: Optional[str] = None,
        includes_tax_diff: bool = False,
        clear_existing: bool = True
    ) -> dict:
        """
        Procesa el año anterior completo (12 meses) - Replica la segunda query de PowerQuery
        
        Args:
            year_base: Año base (se procesará year_base - 1)
            account_start: Código de cuenta inicial (opcional)
            account_end: Código de cuenta final (opcional)
            includes_tax_diff: Incluir diferencia de impuestos
            clear_existing: Si True, elimina datos existentes del año anterior
            
        Returns:
            Diccionario con estadísticas del procesamiento
        """
        previous_year = year_base - 1
        months = list(range(1, 13))  # Siempre 12 meses para año anterior
        
        return await self.process_year_report(
            year=previous_year,
            month_start=1,
            month_end=12,
            account_start=account_start,
            account_end=account_end,
            includes_tax_diff=includes_tax_diff,
            clear_existing=clear_existing
        )
    
    async def _save_to_database(self, df: pd.DataFrame) -> int:
        """Guarda un DataFrame en PostgreSQL"""
        db = get_db_session()
        rows_inserted = 0
        
        try:
            for _, row in df.iterrows():
                balance_record = BalanceReport(
                    codigo_cuenta_contable=int(row['codigo_cuenta_contable']) if pd.notna(row['codigo_cuenta_contable']) else None,
                    nombre_cuenta_contable=str(row['nombre_cuenta_contable']) if pd.notna(row['nombre_cuenta_contable']) else None,
                    cod_relacional=str(row['cod_relacional']) if pd.notna(row['cod_relacional']) else None,
                    identificacion=str(row['identificacion']) if pd.notna(row['identificacion']) else None,
                    sucursal=str(row['sucursal']) if pd.notna(row['sucursal']) else None,
                    nombre_tercero=str(row['nombre_tercero']) if pd.notna(row['nombre_tercero']) else None,
                    saldo_inicial=float(row['saldo_inicial']) if pd.notna(row['saldo_inicial']) else None,
                    movimiento_debito=float(row['movimiento_debito']) if pd.notna(row['movimiento_debito']) else None,
                    movimiento_credito=float(row['movimiento_credito']) if pd.notna(row['movimiento_credito']) else None,
                    movimiento=float(row['movimiento']) if pd.notna(row['movimiento']) else None,
                    saldo_final=float(row['saldo_final']) if pd.notna(row['saldo_final']) else None,
                    fecha=row['fecha'] if pd.notna(row['fecha']) else None,
                    año=int(row['año']) if pd.notna(row['año']) else None,
                    periodo=int(row['periodo']) if pd.notna(row['periodo']) else None
                )
                db.add(balance_record)
                rows_inserted += 1
            
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
        
        return rows_inserted
    
    async def _clear_year_data(self, year: int, months: List[int]):
        """Elimina datos existentes para un año y meses específicos"""
        db = get_db_session()
        try:
            db.execute(
                delete(BalanceReport).where(
                    BalanceReport.año == year,
                    BalanceReport.periodo.in_([year * 100 + m for m in months])
                )
            )
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error limpiando datos: {e}")
        finally:
            db.close()


"""
Servicio ETL para procesar reportes de Siigo mes por mes
Replica la lógica de PowerQuery
"""
import asyncio
from typing import List, Optional
from datetime import date, datetime
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
        
        # Obtener token una sola vez (con retry para rate limit)
        import asyncio
        max_retries = 3
        retry_delay = 2  # segundos
        
        for attempt in range(max_retries):
            try:
                token = await self.siigo_client.get_access_token()
                break
            except Exception as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)
                        print(f"⚠️  Rate limit alcanzado. Esperando {wait_time} segundos antes de reintentar...")
                        await asyncio.sleep(wait_time)
                        continue
                raise
        
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
    
    async def process_date_range(
        self,
        fecha_fin: str,
        account_start: Optional[str] = None,
        account_end: Optional[str] = None,
        includes_tax_diff: bool = False,
        clear_existing: bool = True
    ) -> dict:
        """
        Procesa reportes desde 2024-01-31 hasta la fecha de fin proporcionada
        Replica la lógica de PowerQuery con rango de fechas
        
        Args:
            fecha_fin: Fecha de fin en formato YYYY-MM-DD (ej: 2025-09-30)
            account_start: Código de cuenta inicial (opcional)
            account_end: Código de cuenta final (opcional)
            includes_tax_diff: Incluir diferencia de impuestos
            clear_existing: Si True, elimina datos existentes del rango antes de insertar
            
        Returns:
            Diccionario con estadísticas del procesamiento
        """
        # Fecha inicio fija: 2024-01-31
        fecha_inicio = date(2024, 1, 31)
        
        # Parsear fecha fin
        try:
            fecha_fin_parsed = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Formato de fecha inválido: {fecha_fin}. Use YYYY-MM-DD")
        
        if fecha_fin_parsed < fecha_inicio:
            raise ValueError(f"La fecha de fin ({fecha_fin}) debe ser posterior a {fecha_inicio}")
        
        # Calcular periodos a procesar
        start_year = fecha_inicio.year
        start_month = fecha_inicio.month
        end_year = fecha_fin_parsed.year
        end_month = fecha_fin_parsed.month
        
        periodos_a_procesar = []
        for year in range(start_year, end_year + 1):
            month_start = start_month if year == start_year else 1
            month_end = end_month if year == end_year else 12
            
            for month in range(month_start, month_end + 1):
                periodos_a_procesar.append((year, month))
        
        # Inicializar base de datos
        init_db()
        
        # Eliminar datos existentes si se solicita
        if clear_existing:
            # Agrupar por año para limpiar
            years_to_clear = {}
            for year, month in periodos_a_procesar:
                if year not in years_to_clear:
                    years_to_clear[year] = []
                if month not in years_to_clear[year]:
                    years_to_clear[year].append(month)
            
            for year, months in years_to_clear.items():
                await self._clear_year_data(year, months)
        
        total_rows = 0
        processed_periods = []
        errors = []
        
        # Obtener token una sola vez (con retry para rate limit)
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                token = await self.siigo_client.get_access_token()
                break
            except Exception as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)
                        print(f"⚠️  Rate limit alcanzado. Esperando {wait_time} segundos antes de reintentar...")
                        await asyncio.sleep(wait_time)
                        continue
                raise
        
        # Procesar cada periodo
        for year, month in periodos_a_procesar:
            try:
                # Solicitar reporte para el mes específico
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
                    errors.append(f"{year}-{month:02d}: No se recibió file_url")
                    continue
                
                # Descargar Excel
                excel_content = await self.excel_processor.download_excel(file_url)
                
                # Procesar Excel
                df = self.excel_processor.process_excel(excel_content, year, month)
                
                # Guardar en base de datos
                rows_inserted = await self._save_to_database(df)
                total_rows += rows_inserted
                processed_periods.append(f"{year}-{month:02d}")
                
                print(f"✅ Procesado {year}-{month:02d}: {rows_inserted} registros")
                
            except Exception as e:
                error_msg = f"{year}-{month:02d}: {str(e)}"
                errors.append(error_msg)
                print(f"ERROR procesando {year}-{month:02d}: {e}")
        
        return {
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin_parsed.isoformat(),
            "periodos_procesados": processed_periods,
            "total_periodos": len(processed_periods),
            "total_rows": total_rows,
            "errors": errors,
            "success": len(errors) == 0
        }


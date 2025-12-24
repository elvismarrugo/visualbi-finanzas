"""
Procesador de archivos Excel de Siigo
Replica la lógica ETL de PowerQuery
"""
import pandas as pd
import httpx
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import io


class ExcelProcessor:
    """Procesa archivos Excel descargados de Siigo y los transforma según la lógica de PowerQuery"""
    
    @staticmethod
    async def download_excel(file_url: str) -> bytes:
        """
        Descarga el archivo Excel desde la URL proporcionada por Siigo
        
        Args:
            file_url: URL del archivo Excel
            
        Returns:
            Contenido del archivo en bytes
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(file_url, timeout=120.0)
            response.raise_for_status()
            return response.content
    
    @staticmethod
    def process_excel(
        excel_content: bytes,
        year: int,
        month: int
    ) -> pd.DataFrame:
        """
        Procesa un archivo Excel y aplica las transformaciones ETL de PowerQuery
        
        Args:
            excel_content: Contenido del archivo Excel en bytes
            year: Año del reporte
            month: Mes del reporte (1-13, donde 13 es cierre)
            
        Returns:
            DataFrame de pandas con los datos procesados
        """
        # Leer el Excel
        excel_file = io.BytesIO(excel_content)
        excel_workbook = pd.ExcelFile(excel_file, engine='openpyxl')
        
        # Obtener la primera hoja
        first_sheet = excel_workbook.sheet_names[0]
        df = pd.read_excel(excel_file, sheet_name=first_sheet, header=None, engine='openpyxl')
        
        # ETL: Detectar fila de encabezados
        # Buscar fila donde columna 0 = "Nivel" y columna 2 = "Código cuenta contable"
        header_index = -1
        for idx, row in df.iterrows():
            if (pd.notna(row.iloc[0]) and str(row.iloc[0]).strip() == "Nivel" and
                pd.notna(row.iloc[2]) and str(row.iloc[2]).strip() == "Código cuenta contable"):
                header_index = idx
                break
        
        # Si se encontró el encabezado, usar esa fila como header
        if header_index != -1:
            df = df.iloc[header_index + 1:].copy()
            # Obtener los nombres de las columnas de la fila de encabezado
            header_row = pd.read_excel(
                excel_file, 
                sheet_name=first_sheet, 
                header=header_index,
                nrows=0,
                engine='openpyxl'
            )
            df.columns = header_row.columns
        else:
            # Si no se encuentra, usar la primera fila como header
            df.columns = df.iloc[0]
            df = df.iloc[1:].copy()
        
        # Limpiar: Eliminar filas completamente vacías
        df = df.dropna(how='all')
        
        # Filtrar: Eliminar filas donde Nivel esté vacío
        if 'Nivel' in df.columns:
            df = df[df['Nivel'].astype(str).str.strip() != '']
            df = df[df['Nivel'].astype(str).str.strip().notna()]
        
        # Filtrar: Solo filas donde Transaccional = "Sí" o "SI"
        if 'Transaccional' in df.columns:
            df['Transaccional_upper'] = df['Transaccional'].astype(str).str.upper().str.strip()
            df = df[df['Transaccional_upper'].isin(['SÍ', 'SI'])]
            df = df.drop(columns=['Transaccional_upper'])
        
        # Eliminar columnas Nivel y Transaccional
        columns_to_drop = []
        if 'Nivel' in df.columns:
            columns_to_drop.append('Nivel')
        if 'Transaccional' in df.columns:
            columns_to_drop.append('Transaccional')
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
        
        # Calcular Fecha: último día del mes
        from calendar import monthrange
        
        if month == 13:
            # Mes 13 = cierre = 31 de diciembre
            fecha = date(year, 12, 31)
        else:
            # Último día del mes especificado
            last_day = monthrange(year, month)[1]
            fecha = date(year, month, last_day)
        
        # Agregar columnas calculadas
        df['Fecha'] = fecha
        df['Año'] = year
        df['Periodo'] = year * 100 + month
        
        # Convertir tipos de datos
        numeric_columns = [
            'Código cuenta contable',
            'Saldo Inicial',
            'Movimiento Débito',
            'Movimiento Crédito',
            'Saldo final'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Redondear valores numéricos a 2 decimales
        for col in ['Saldo Inicial', 'Movimiento Débito', 'Movimiento Crédito', 'Saldo final']:
            if col in df.columns:
                df[col] = df[col].round(2)
        
        # Calcular Movimiento = Débito - Crédito
        if 'Movimiento Débito' in df.columns and 'Movimiento Crédito' in df.columns:
            df['Movimiento'] = (df['Movimiento Débito'] - df['Movimiento Crédito']).round(2)
        
        # Calcular Cod Relacional = primeros 6 caracteres del código cuenta
        if 'Código cuenta contable' in df.columns:
            df['Cod Relacional'] = df['Código cuenta contable'].astype(str).str[:6]
        
        # Renombrar columnas para que coincidan con el modelo de BD
        column_mapping = {
            'Código cuenta contable': 'codigo_cuenta_contable',
            'Nombre Cuenta contable': 'nombre_cuenta_contable',
            'Identificación': 'identificacion',
            'Sucursal': 'sucursal',
            'Nombre tercero': 'nombre_tercero',
            'Saldo Inicial': 'saldo_inicial',
            'Movimiento Débito': 'movimiento_debito',
            'Movimiento Crédito': 'movimiento_credito',
            'Saldo final': 'saldo_final',
            'Movimiento': 'movimiento',
            'Cod Relacional': 'cod_relacional',
            'Fecha': 'fecha',
            'Año': 'año',
            'Periodo': 'periodo'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Asegurar que todas las columnas esperadas existan
        expected_columns = [
            'codigo_cuenta_contable', 'nombre_cuenta_contable', 'cod_relacional',
            'identificacion', 'sucursal', 'nombre_tercero',
            'saldo_inicial', 'movimiento_debito', 'movimiento_credito',
            'movimiento', 'saldo_final',
            'fecha', 'año', 'periodo'
        ]
        
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None
        
        # Seleccionar solo las columnas esperadas
        df = df[expected_columns]
        
        return df


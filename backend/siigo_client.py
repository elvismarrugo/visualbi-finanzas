import httpx
from typing import Optional, Dict, Any
from config import get_settings


class SiigoClient:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.siigo_base_url
        self.access_token: Optional[str] = None

    async def get_access_token(self) -> str:
        """Obtiene el token de acceso de la API de Siigo"""
        if self.access_token:
            return self.access_token

        async with httpx.AsyncClient() as client:
            # Para autenticación, SOLO se necesita Content-Type (según PowerQuery)
            # NO incluir Partner-Id en el header de auth
            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "username": self.settings.siigo_username,
                "access_key": self.settings.siigo_access_key
            }

            try:
                # Endpoint de autenticación: /auth (según PowerQuery)
                auth_endpoint = f"{self.base_url}/auth"
                response = await client.post(
                    auth_endpoint,
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )

                response.raise_for_status()
                data = response.json()
                self.access_token = data.get("access_token")
                
                if not self.access_token:
                    raise Exception(f"No se recibió access_token en la respuesta: {data}")

                return self.access_token
            except httpx.HTTPStatusError as e:
                error_detail = f"Error de autenticación: {e.response.status_code}"
                if e.response.text:
                    try:
                        error_data = e.response.json()
                        error_detail += f" - {error_data}"
                    except:
                        error_detail += f" - {e.response.text}"
                raise Exception(error_detail)
            except Exception as e:
                raise Exception(f"Error al obtener token de acceso: {str(e)}")

    async def get_balance_report_by_thirdparty(
        self,
        year: int,
        month_start: int,
        month_end: int,
        account_start: str,
        account_end: str,
        includes_tax_diff: bool = False
    ) -> Dict[str, Any]:
        """
        Obtiene el reporte de balance por terceros usando el endpoint test-balance-report-by-thirdparty

        Args:
            year: Año del reporte (obligatorio)
            month_start: Mes de inicio 1-13 (obligatorio)
            month_end: Mes de fin 1-13 (obligatorio)
            account_start: Código de cuenta inicial (opcional)
            account_end: Código de cuenta final (opcional)
            includes_tax_diff: Incluir diferencia de impuestos (obligatorio, true/false)

        Returns:
            Datos del reporte de balance con file_id y file_url para descargar el Excel
        """
        token = await self.get_access_token()

        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {token}",
                "Partner-Id": self.settings.siigo_partner_id,
                "Content-Type": "application/json"
            }

            # Construir el cuerpo de la petición según la documentación de Siigo
            payload = {
                "year": year,
                "month_start": month_start,
                "month_end": month_end,
                "includes_tax_difference": includes_tax_diff
            }

            # Agregar account_start y account_end solo si están presentes y no están vacíos
            if account_start and account_start.strip():
                payload["account_start"] = account_start.strip()
            if account_end and account_end.strip():
                payload["account_end"] = account_end.strip()

            # El endpoint test-balance-report-by-thirdparty usa POST
            try:
                response = await client.post(
                    f"{self.base_url}/v1/test-balance-report-by-thirdparty",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )

                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                error_detail = f"Error de la API de Siigo: {e.response.status_code}"
                if e.response.text:
                    try:
                        error_data = e.response.json()
                        error_detail += f" - {error_data}"
                    except:
                        error_detail += f" - {e.response.text[:500]}"  # Limitar tamaño
                raise Exception(error_detail)
            except Exception as e:
                raise Exception(f"Error al obtener el reporte: {str(e)}")

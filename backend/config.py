from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    siigo_access_key: str
    siigo_partner_id: str
    siigo_base_url: str
    siigo_username: str
    backend_port: int = 8000
    
    # Configuración de PostgreSQL
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "siigo_db"
    db_user: str = "postgres"
    db_password: str = "postgres"

    class Config:
        env_file = "../.env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()

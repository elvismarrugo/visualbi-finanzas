"""
Configuración de la base de datos PostgreSQL
"""
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings
from datetime import datetime

Base = declarative_base()


class BalanceReport(Base):
    """
    Modelo de datos para almacenar los reportes de balance procesados
    Replica la estructura de datos de PowerQuery
    """
    __tablename__ = "balance_reports"

    id = Column(Integer, primary_key=True, index=True)
    
    # Datos de la cuenta contable
    codigo_cuenta_contable = Column(Integer, index=True)
    nombre_cuenta_contable = Column(Text)
    cod_relacional = Column(String(10), index=True)  # Primeros 6 caracteres
    
    # Datos del tercero
    identificacion = Column(String(50), index=True)
    sucursal = Column(String(100))
    nombre_tercero = Column(Text)
    
    # Valores contables
    saldo_inicial = Column(Numeric(18, 2))
    movimiento_debito = Column(Numeric(18, 2))
    movimiento_credito = Column(Numeric(18, 2))
    movimiento = Column(Numeric(18, 2))  # Débito - Crédito
    saldo_final = Column(Numeric(18, 2))
    
    # Dimensiones temporales
    fecha = Column(Date, index=True)
    año = Column(Integer, index=True)
    periodo = Column(Integer, index=True)  # AAAAMM formato
    
    # Metadatos
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def get_db_engine():
    """Crea y retorna el engine de SQLAlchemy"""
    settings = get_settings()
    
    # Intentar usar PostgreSQL primero, si falla usar SQLite como fallback
    try:
        # Construir la URL de conexión desde variables de entorno
        # Formato: postgresql://user:password@host:port/database
        db_url = (
            f"postgresql://{settings.db_user}:{settings.db_password}"
            f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
        )
        
        engine = create_engine(db_url, pool_pre_ping=True)
        # Probar la conexión
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return engine
    except Exception as e:
        # Fallback a SQLite si PostgreSQL no está disponible
        import os
        sqlite_path = os.path.join(os.path.dirname(__file__), "..", "siigo_data.db")
        print(f"⚠️  PostgreSQL no disponible ({e}), usando SQLite: {sqlite_path}")
        sqlite_url = f"sqlite:///{sqlite_path}"
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
        return engine


def get_db_session():
    """Crea y retorna una sesión de base de datos"""
    engine = get_db_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


# Para usar con FastAPI Depends
def get_db():
    """Dependency para FastAPI"""
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Crea todas las tablas en la base de datos"""
    engine = get_db_engine()
    Base.metadata.create_all(bind=engine)


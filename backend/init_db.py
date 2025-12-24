"""
Script para inicializar la base de datos PostgreSQL
Ejecutar: python init_db.py
"""
from database import init_db

if __name__ == "__main__":
    print("Inicializando base de datos...")
    init_db()
    print("✅ Base de datos inicializada correctamente")


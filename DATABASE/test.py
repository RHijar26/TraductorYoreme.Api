import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from sqlalchemy import create_engine, text
from config import config

def test_basic_connection():
    """Prueba básica de conexión a PostgreSQL."""
    print("\n" + "="*70)
    print("TEST DE CONEXIÓN A POSTGRESQL")
    print("="*70)
    print(f"\nURL de conexión: {config.database_url}")
    print("-"*70)
    
    try:
        # Crear engine de SQLAlchemy
        engine = create_engine(config.database_url)
        
        # Intentar conectar
        print("\n[1/3] Probando conexión...")
        with engine.connect() as connection:
            # Ejecutar query simple
            result = connection.execute(text("SELECT 1"))
            result.close()
            print("✓ Conexión exitosa")
            
            # Obtener versión de PostgreSQL
            print("\n[2/3] Obteniendo versión de PostgreSQL...")
            version_result = connection.execute(text("SELECT version()"))
            version = version_result.scalar()
            print(f"✓ {version.split(',')[0]}")
            
            # Información de la base de datos
            print("\n[3/3] Información de la base de datos...")
            
            db_result = connection.execute(text("SELECT current_database()"))
            db_name = db_result.scalar()
            print(f"  - Base de datos: {db_name}")
            
            user_result = connection.execute(text("SELECT current_user"))
            user = user_result.scalar()
            print(f"  - Usuario: {user}")
            
            # Cerrar conexión
            connection.close()
        
        print("\n" + "="*70)
        print("✅ TEST EXITOSO - PostgreSQL está funcionando correctamente")
        print("="*70 + "\n")
        return True
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ ERROR AL CONECTAR CON POSTGRESQL")
        print("="*70)
        print(f"\nTipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("\nVerifica:")
        print("  1. PostgreSQL está corriendo")
        print("  2. Las credenciales en enviroment.env son correctas")
        print("  3. La base de datos existe")
        print("  4. El host y puerto son accesibles")
        print("="*70 + "\n")
        return False

if __name__ == "__main__":
    test_basic_connection()
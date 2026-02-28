# verify_sqlalchemy_flow.py
"""
Verifica el flujo de inicialización de SQLAlchemy.
"""
import sys
from pathlib import Path
import ast
import re

root = Path(__file__).parent
sys.path.insert(0, str(root))

def print_section(title):
    """Imprime un encabezado."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def check_file_content(file_path, checks):
    """Verifica el contenido de un archivo."""
    print(f"\n📄 Verificando: {file_path}")
    
    if not file_path.exists():
        print(f"❌ Archivo no existe: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_passed = True
    for check_name, pattern, expected in checks:
        found = bool(re.search(pattern, content, re.MULTILINE))
        status = "✅" if found == expected else "❌"
        print(f"  {status} {check_name}")
        if found != expected:
            all_passed = False
            if expected and not found:
                print(f"      ⚠️  NO encontrado: {pattern}")
    
    return all_passed

def verify_structure():
    """Verifica la estructura de inicialización."""
    print_section("VERIFICACIÓN DE ESTRUCTURA DE SQLALCHEMY")
    
    # 1. Verificar DATABASE/db.py
    print_section("1. DATABASE/db.py")
    
    db_file = root / "DATABASE" / "db.py"
    db_checks = [
        ("Importa SQLAlchemy", r"from flask_sqlalchemy import SQLAlchemy", True),
        ("Crea instancia db", r"db\s*=\s*SQLAlchemy\(\)", True),
        ("Define init_db", r"def init_db\(app\)", True),
        ("Llama db.init_app", r"db\.init_app\(app\)", True),
        ("Llama db.create_all", r"db\.create_all\(\)", True),
        ("Usa app_context", r"with app\.app_context\(\)", True),
        ("NO crea múltiples instancias", r"db\s*=\s*SQLAlchemy\(app\)", False),
    ]
    
    db_ok = check_file_content(db_file, db_checks)
    
    # 2. Verificar DATABASE/models.py
    print_section("2. DATABASE/models.py")
    
    models_file = root / "DATABASE" / "models.py"
    models_checks = [
        ("Importa db desde DATABASE.db", r"from DATABASE\.db import db", True),
        ("Usa db.Model", r"class.*\(db\.Model\)", True),
        ("Usa db.Column", r"db\.Column", True),
        ("NO importa SQLAlchemy directamente", r"from flask_sqlalchemy import SQLAlchemy", False),
        ("NO crea nueva instancia db", r"db\s*=\s*SQLAlchemy\(\)", False),
    ]
    
    models_ok = check_file_content(models_file, models_checks)
    
    # 3. Verificar DATABASE/repositories/userRepository.py
    print_section("3. DATABASE/repositories/userRepository.py")
    
    repo_file = root / "DATABASE" / "repositories" / "userRepository.py"
    repo_checks = [
        ("Importa db desde DATABASE.db", r"from DATABASE\.db import db", True),
        ("Usa db.session", r"db\.session", True),
        ("NO crea nueva instancia db", r"db\s*=\s*SQLAlchemy\(\)", False),
    ]
    
    repo_ok = check_file_content(repo_file, repo_checks)
    
    # 4. Verificar API/app.py
    print_section("4. API/app.py")
    
    app_file = root / "API" / "app.py"
    app_checks = [
        ("Crea app Flask", r"app\s*=\s*Flask\(__name__\)", True),
        ("Importa init_db", r"from DATABASE\.db import init_db", True),
        ("Llama init_db(app)", r"init_db\(app\)", True),
        ("init_db ANTES de blueprints", r"init_db\(app\).*from.*routes", True),
        ("NO crea SQLAlchemy en app.py", r"SQLAlchemy\(app\)", False),
    ]
    
    app_ok = check_file_content(app_file, app_checks)
    
    # Verificar orden en app.py
    if app_file.exists():
        with open(app_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        init_db_line = None
        blueprint_import_line = None
        blueprint_register_line = None
        
        for i, line in enumerate(lines, 1):
            if 'init_db(app)' in line:
                init_db_line = i
            if 'from API.' in line and 'import' in line and '_bp' in line:
                if blueprint_import_line is None:
                    blueprint_import_line = i
            if 'register_blueprint' in line:
                if blueprint_register_line is None:
                    blueprint_register_line = i
        
        print("\n📋 Orden de inicialización en app.py:")
        if init_db_line:
            print(f"  ✓ init_db(app) en línea: {init_db_line}")
        else:
            print(f"  ❌ NO se encuentra init_db(app)")
        
        if blueprint_import_line:
            print(f"  ✓ Import de blueprint en línea: {blueprint_import_line}")
        else:
            print(f"  ⚠️  NO se encontró import de blueprint")
        
        if blueprint_register_line:
            print(f"  ✓ register_blueprint en línea: {blueprint_register_line}")
        else:
            print(f"  ⚠️  NO se encontró register_blueprint")
        
        if init_db_line and blueprint_import_line:
            if init_db_line < blueprint_import_line:
                print(f"\n  ✅ ORDEN CORRECTO: init_db ANTES de import blueprints")
            else:
                print(f"\n  ❌ ORDEN INCORRECTO: init_db DESPUÉS de import blueprints")
                print(f"     init_db debe estar ANTES de importar los blueprints")
    
    # 5. Verificar blueprints
    print_section("5. Blueprints (API/users.py, API/auth.py)")
    
    users_file = root / "API" / "users.py"
    if users_file.exists():
        print(f"\n📄 {users_file}")
        users_checks = [
            ("Importa UserRepository", r"from DATABASE\.repositories.*import UserRepository", True),
            ("NO importa db directamente", r"from DATABASE\.db import db", False),
            ("NO usa db.session directamente", r"db\.session", False),
        ]
        check_file_content(users_file, users_checks)
    
    # Resumen
    print_section("RESUMEN")
    
    issues = []
    if not db_ok:
        issues.append("DATABASE/db.py tiene problemas")
    if not models_ok:
        issues.append("DATABASE/models.py tiene problemas")
    if not repo_ok:
        issues.append("DATABASE/repositories/userRepository.py tiene problemas")
    if not app_ok:
        issues.append("API/app.py tiene problemas")
    
    if issues:
        print("\n❌ PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\n✅ ESTRUCTURA CORRECTA")
        return True

def test_runtime():
    """Prueba la inicialización en runtime."""
    print_section("PRUEBA EN RUNTIME")
    
    try:
        # Test 1: Importar db
        print("\n[1/5] Importando db...")
        from DATABASE.db import db, init_db
        print(f"✅ db importado")
        print(f"   Tipo: {type(db)}")
        
        # Test 2: Importar modelos
        print("\n[2/5] Importando modelos...")
        from DATABASE.models import User
        print(f"✅ User importado")
        
        # Test 3: Importar repositorios
        print("\n[3/5] Importando repositorios...")
        from DATABASE.repositories.userRepository import UserRepository
        print(f"✅ UserRepository importado")
        
        # Test 4: Crear app y vincular db
        print("\n[4/5] Creando app y vinculando db...")
        from flask import Flask
        app = Flask(__name__)
        
        from config import config
        app.config['SQLALCHEMY_DATABASE_URI'] = config.database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Vincular db con app
        db.init_app(app)
        print(f"✅ db vinculado con app")
        
        # Test 5: Probar operación dentro de app_context
        print("\n[5/5] Probando operación en app_context...")
        with app.app_context():
            # Intentar una operación simple
            count = User.query.count()
            print(f"✅ Query ejecutado correctamente")
            print(f"   Total usuarios: {count}")
        
        print("\n✅ TODAS LAS PRUEBAS PASARON")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print("\n📋 Traceback completo:")
        print(traceback.format_exc())
        return False

def main():
    """Ejecuta todas las verificaciones."""
    print("\n" + "="*70)
    print("DIAGNÓSTICO COMPLETO DE SQLALCHEMY")
    print("="*70)
    
    structure_ok = verify_structure()
    runtime_ok = test_runtime()
    
    print("\n" + "="*70)
    print("RESULTADO FINAL")
    print("="*70)
    
    if structure_ok and runtime_ok:
        print("\n✅ TODO ESTÁ CORRECTO")
        print("\nSi aún tienes errores, el problema puede estar en:")
        print("  1. El orden de ejecución en tu código")
        print("  2. Importaciones circulares")
        print("  3. Múltiples instancias de app o db")
    else:
        print("\n❌ SE ENCONTRARON PROBLEMAS")
        print("\nRevisa los errores arriba y corrige los archivos indicados.")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
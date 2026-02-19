#!/usr/bin/env python3
"""
Script de Verificación de Configuración - Maxocracia
=====================================================

Verifica que todas las dependencias y configuraciones estén correctas
antes de lanzar el sistema de pagos.

Uso:
    python scripts/verify_setup.py

Autor: Kimi (Moonshot AI)
Fecha: Febrero 2026
"""

import importlib
import os
import sys
from pathlib import Path


def check_colored_print(text: str, status: str, details: str = ""):
    """Imprime con colores según estado."""
    colors = {
        "ok": "\033[92m",      # Verde
        "error": "\033[91m",   # Rojo
        "warning": "\033[93m", # Amarillo
        "info": "\033[94m",    # Azul
        "reset": "\033[0m"
    }
    
    icons = {
        "ok": "✓",
        "error": "✗",
        "warning": "⚠",
        "info": "ℹ"
    }
    
    color = colors.get(status, colors["info"])
    icon = icons.get(status, "•")
    reset = colors["reset"]
    
    print(f"{color}{icon}{reset} {text}")
    if details:
        print(f"  {details}")


def check_python_version():
    """Verifica versión de Python."""
    version = sys.version_info
    if version >= (3, 8):
        check_colored_print(
            f"Python {version.major}.{version.minor}.{version.micro}",
            "ok"
        )
        return True
    else:
        check_colored_print(
            f"Python {version.major}.{version.minor}.{version.micro}",
            "error",
            "Se requiere Python 3.8 o superior"
        )
        return False


def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    required = [
        "flask",
        "stripe",
        "jwt",
        "werkzeug",
    ]
    
    all_ok = True
    for package in required:
        try:
            importlib.import_module(package)
            check_colored_print(f"Dependencia: {package}", "ok")
        except ImportError:
            check_colored_print(
                f"Dependencia: {package}",
                "error",
                f"Ejecuta: pip install {package}"
            )
            all_ok = False
    
    return all_ok


def check_env_file():
    """Verifica archivo .env."""
    env_path = Path(".env")
    example_path = Path("config.example.env")
    
    if not env_path.exists():
        if example_path.exists():
            check_colored_print(
                "Archivo .env",
                "error",
                f"No existe. Copia: cp config.example.env .env"
            )
        else:
            check_colored_print(
                "Archivo .env",
                "error",
                "No existe config.example.env para copiar"
            )
        return False
    
    check_colored_print("Archivo .env", "ok")
    return True


def check_stripe_config():
    """Verifica configuración de Stripe."""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "STRIPE_SECRET_KEY",
        "STRIPE_PUBLISHABLE_KEY",
    ]
    
    optional_vars = [
        "STRIPE_WEBHOOK_SECRET",
        "STRIPE_PRICE_CONTRIBUTOR",
        "STRIPE_PRICE_ENTERPRISE",
    ]
    
    all_ok = True
    
    # Verificar requeridas
    for var in required_vars:
        value = os.environ.get(var)
        if not value or value.startswith("...") or value == f"{var.lower()}_here":
            check_colored_print(
                f"Variable {var}",
                "error",
                "No configurada o valor placeholder"
            )
            all_ok = False
        else:
            # Ocultar parte de la clave
            display = value[:10] + "..." if len(value) > 10 else value
            check_colored_print(f"Variable {var}: {display}", "ok")
    
    # Verificar opcionales
    for var in optional_vars:
        value = os.environ.get(var)
        if not value:
            check_colored_print(
                f"Variable {var}",
                "warning",
                "No configurada (opcional pero recomendada)"
            )
        else:
            check_colored_print(f"Variable {var}: configurada", "ok")
    
    # Verificar si es modo test o live
    secret_key = os.environ.get("STRIPE_SECRET_KEY", "")
    if "sk_live" in secret_key:
        check_colored_print(
            "⚠️  ATENCIÓN: Usando Stripe en MODO LIVE",
            "warning",
            "Los pagos serán reales. Asegúrate de estar listo."
        )
    elif "sk_test" in secret_key:
        check_colored_print("Stripe en modo TEST", "ok")
    
    return all_ok


def check_database():
    """Verifica conexión a base de datos."""
    try:
        # Intentar importar y conectar
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from app.utils import get_db
        
        db = get_db()
        db.execute("SELECT 1")
        check_colored_print("Base de datos", "ok")
        return True
    except Exception as e:
        check_colored_print(
            "Base de datos",
            "error",
            str(e)
        )
        return False


def check_frontend():
    """Verifica que el frontend esté configurado."""
    frontend_path = Path("frontend/package.json")
    
    if not frontend_path.exists():
        check_colored_print(
            "Frontend",
            "error",
            "No se encontró frontend/package.json"
        )
        return False
    
    check_colored_print("Frontend", "ok")
    
    # Verificar node_modules
    node_modules = Path("frontend/node_modules")
    if not node_modules.exists():
        check_colored_print(
            "Frontend dependencias",
            "warning",
            "Ejecuta: cd frontend && npm install"
        )
        return False
    
    check_colored_print("Frontend dependencias", "ok")
    return True


def check_migrations():
    """Verifica que las migraciones estén aplicadas."""
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from app.utils import get_db
        
        db = get_db()
        
        # Verificar tabla subscriptions
        result = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='subscriptions'"
        ).fetchone()
        
        if result:
            check_colored_print("Tabla subscriptions", "ok")
            
            # Verificar columnas
            columns = db.execute("PRAGMA table_info(subscriptions)").fetchall()
            column_names = [col["name"] for col in columns]
            
            required_columns = [
                "user_id", "tier", "status", "external_customer_id"
            ]
            
            for col in required_columns:
                if col in column_names:
                    check_colored_print(f"  Columna: {col}", "ok")
                else:
                    check_colored_print(
                        f"  Columna: {col}",
                        "error",
                        "Falta columna requerida"
                    )
            
            return True
        else:
            check_colored_print(
                "Tabla subscriptions",
                "error",
                "Ejecuta migración: sqlite3 comun.db < migrations/001_add_subscriptions.sql"
            )
            return False
            
    except Exception as e:
        check_colored_print(
            "Migraciones",
            "error",
            str(e)
        )
        return False


def main():
    """Función principal de verificación."""
    print("=" * 60)
    print("  Verificación de Configuración - Maxocracia")
    print("=" * 60)
    print()
    
    checks = [
        ("Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Archivo .env", check_env_file),
        ("Configuración Stripe", check_stripe_config),
        ("Base de datos", check_database),
        ("Migraciones", check_migrations),
        ("Frontend", check_frontend),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📦 {name}")
        print("-" * 40)
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            check_colored_print(f"Error en verificación: {e}", "error")
            results.append((name, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("  RESUMEN")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "ok" if result else "error"
        check_colored_print(name, status)
    
    print()
    print(f"Resultado: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print()
        check_colored_print(
            "🎉 Todo está configurado correctamente",
            "ok"
        )
        check_colored_print(
            "Puedes iniciar el servidor: python run.py",
            "info"
        )
        return 0
    else:
        print()
        check_colored_print(
            "⚠️  Hay problemas que debes solucionar",
            "warning"
        )
        check_colored_print(
            "Revisa los errores arriba y corrígelos",
            "info"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())

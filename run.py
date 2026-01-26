import os

# Intentar cargar .env, pero no fallar si hay error de encoding o falta librería
try:
    from dotenv import load_dotenv
    load_dotenv(encoding="utf-8") # Intentar forzar utf-8
    print("INFO: Intentando cargar .env con python-dotenv...")
except Exception as e:
    print(f"ADVERTENCIA: No se pudo cargar .env: {e}")

# FALLBACKS DE SEGURIDAD (Para desbloquear al usuario)
# Si no hay SECRET_KEY, lo forzamos.
if not os.environ.get("SECRET_KEY"):
    print("AVISO: Forzando SECRET_KEY temporal para desarrollo.")
    os.environ["SECRET_KEY"] = "dev-fallback-key-12345"

# Si no hay FLASK_ENV, lo ponemos en development para ver errores detallados
if not os.environ.get("FLASK_ENV"):
    print("AVISO: Forzando FLASK_ENV='development'")
    os.environ["FLASK_ENV"] = "development"
    os.environ["FLASK_DEBUG"] = "1"

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="127.0.0.1", port=port)

import os

# Intentar cargar .env, pero no fallar si hay error de encoding o falta librería
try:
    from dotenv import load_dotenv

    load_dotenv(encoding="utf-8")  # Intentar forzar utf-8
    print("INFO: Intentando cargar .env con python-dotenv...")
except Exception as e:
    print(f"ADVERTENCIA: No se pudo cargar .env: {e}")

# FALLBACKS DE SEGURIDAD (Para desbloquear al usuario en DESARROLLO).
# En producción la SECRET_KEY es obligatoria: una clave conocida permitiría
# forjar JWTs e invitaciones firmadas (escalera de confianza, Cap. 13).
if not os.environ.get("SECRET_KEY"):
    if os.environ.get("FLASK_ENV") == "production":
        print(
            "ERROR DE SEGURIDAD: SECRET_KEY no definida en producción. "
            "Defínela en el entorno (openssl rand -hex 32) y reintenta."
        )
        raise SystemExit(1)
    print("AVISO: Forzando SECRET_KEY temporal para desarrollo.")
    os.environ["SECRET_KEY"] = "dev-fallback-key-maxocracia-0123456789abcdef"

# Si no hay FLASK_ENV, lo ponemos en development para ver errores detallados
if not os.environ.get("FLASK_ENV"):
    print("AVISO: Forzando FLASK_ENV='development'")
    os.environ["FLASK_ENV"] = "development"
    os.environ["FLASK_DEBUG"] = "1"

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))

    if os.environ.get("FLASK_ENV") == "production":
        print(f"Iniciando servidor de PRODUCCIÓN con Waitress en el puerto {port}...")
        from waitress import serve

        serve(app, host="0.0.0.0", port=port)
    else:
        print(f"Iniciando servidor de DESARROLLO en el puerto {port}...")
        app.run(host="0.0.0.0", port=port, debug=True)

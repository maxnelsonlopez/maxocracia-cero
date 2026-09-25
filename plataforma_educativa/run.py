# -*- coding: utf-8 -*-
"""Punto de entrada de la Plataforma Educativa.

Arranca la aplicación Flask en el puerto 5050, distinto del 5001 que usa el
backend de Maxocracia. Se puede ejecutar directamente:

    python run.py

o bien con el comando equivalente del CLI de Flask:

    python -m flask --app app run --port 5050

Por defecto corre en modo producción (sin debugger, con waitress si está
instalado): la escuela se publica por el túnel de Cloudflare, así que el
debugger interactivo de Werkzeug NUNCA debe quedar expuesto. Para desarrollo
local existe ``PLATAFORMA_EDUCATIVA_DEBUG=1``.

Variables de entorno:
- ``PLATAFORMA_EDUCATIVA_DB``: ruta de la base SQLite (default: junto a run.py).
- ``PLATAFORMA_EDUCATIVA_HOST`` / ``PLATAFORMA_EDUCATIVA_PORT``.
- ``PLATAFORMA_EDUCATIVA_DEBUG=1``: servidor de desarrollo con debugger
  (solo en localhost; jamás detrás de un túnel público).
"""

import os

from app import create_app

# Ruta por defecto de la base de datos.
DEFAULT_DB = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "plataforma_educativa.db"
)


def main():
    # Se lee la variable de entorno (con encoding por defecto utf-8 en Python 3).
    db_path = os.environ.get("PLATAFORMA_EDUCATIVA_DB", DEFAULT_DB)
    app = create_app(db_path=db_path)

    host = os.environ.get("PLATAFORMA_EDUCATIVA_HOST", "127.0.0.1")
    port = int(os.environ.get("PLATAFORMA_EDUCATIVA_PORT", "5050"))

    if os.environ.get("PLATAFORMA_EDUCATIVA_DEBUG") == "1":
        print(f"AVISO: modo desarrollo con debugger en http://{host}:{port}")
        app.run(host=host, port=port, debug=True)
        return

    try:
        from waitress import serve
    except ImportError:
        print(
            "AVISO: waitress no está instalado; sirviendo en producción sin "
            "debugger. Instálalo con: pip install waitress"
        )
        app.run(host=host, port=port, debug=False)
        return

    print(f"Plataforma Educativa en http://{host}:{port} (producción, debug off)")
    serve(app, host=host, port=port)


if __name__ == "__main__":
    main()

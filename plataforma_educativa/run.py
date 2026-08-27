# -*- coding: utf-8 -*-
"""Punto de entrada de la Plataforma Educativa.

Arranca la aplicación Flask en el puerto 5050, distinto del 5001 que usa el
backend de Maxocracia. Se puede ejecutar directamente:

    python run.py

o bien con el comando equivalente del CLI de Flask:

    python -m flask --app app run --port 5050

La ruta de la base de datos SQLite se resuelve a un archivo dentro de este
mismo directorio (``plataforma_educativa.db``). Existe una variable de entorno
``PLATAFORMA_EDUCATIVA_DB`` para apuntar a otra ruta si hace falta.
"""

import os

from app import create_app

# Ruta por defecto de la base de datos.
DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plataforma_educativa.db")


def main():
    # Se lee la variable de entorno (con encoding por defecto utf-8 en Python 3).
    db_path = os.environ.get("PLATAFORMA_EDUCATIVA_DB", DEFAULT_DB)
    app = create_app(db_path=db_path)
    # host="127.0.0.1" evita abrirse a la red; debug=True para desarrollo.
    app.run(host="127.0.0.1", port=5050, debug=True)


if __name__ == "__main__":
    main()

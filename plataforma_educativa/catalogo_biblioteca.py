# -*- coding: utf-8 -*-
"""B8 Catálogo de la biblioteca curada: inventario máquina-legible real.

Genera ``catalogo.json`` en la raíz de la biblioteca a partir de LOS ARCHIVOS
REALES (nombres, tamaños, hashes) — nada inventado. Cada ítem trae placeholders
de licencia/curaduría que el curador (humano) rellena:

Uso::

    .venv\\Scripts\\python.exe plataforma_educativa/catalogo_biblioteca.py "D:\\biblioteca privada"

Campos por ítem: ruta_relativa, titulo, tamano, sha256, categoria, formato,
indexable, licencia (default "closed": sin licencia no hay nivel 1),
visibilidad (default "privada"), curaduria, source_url, oa_candidato.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

INDEXABLES = {".pdf", ".txt", ".md", ".markdown"}

# Candidatos OA/dominio público a verificar UNO A UNO (humano, no asumir).
OA_PISTAS = ("v55n1a16", "galileo_sph", "JoseAntonioPrieto", "springeropen", "open-access")


def generar_catalogo(pdf_dir):
    """Recorre la biblioteca y devuelve el catálogo (dict serializable)."""
    pdf_dir = os.path.abspath(pdf_dir)
    items = []
    for raiz, _dirs, archivos in os.walk(pdf_dir):
        for nombre in sorted(archivos):
            if nombre == "catalogo.json":
                continue
            ruta = os.path.join(raiz, nombre)
            rel = os.path.relpath(ruta, pdf_dir).replace(os.sep, "/")
            try:
                tamano = os.path.getsize(ruta)
            except OSError:
                continue
            h = hashlib.sha256()
            try:
                with open(ruta, "rb") as fh:
                    for bloque in iter(lambda: fh.read(1 << 20), b""):
                        h.update(bloque)
            except OSError:
                continue
            partes = rel.split("/")
            ext = os.path.splitext(nombre)[1].lower()
            items.append(
                {
                    "ruta_relativa": rel,
                    "titulo": os.path.splitext(nombre)[0],
                    "tamano": tamano,
                    "sha256": h.hexdigest(),
                    "categoria": partes[0] if len(partes) > 1 else "",
                    "formato": ext or "sin-extension",
                    "indexable": ext in INDEXABLES,
                    "licencia": "closed",
                    "visibilidad": "privada",
                    "curaduria": "",
                    "source_url": "",
                    "oa_candidato": any(p.lower() in nombre.lower() for p in OA_PISTAS),
                }
            )
    return {
        "generado": datetime.now(timezone.utc).isoformat(),
        "raiz": pdf_dir,
        "n_items": len(items),
        "items": items,
    }


def main(argv):
    if not argv or not os.path.isdir(argv[0]):
        print("uso: catalogo_biblioteca.py <carpeta-biblioteca>")
        return 1
    catalogo = generar_catalogo(argv[0])
    salida = os.path.join(os.path.abspath(argv[0]), "catalogo.json")
    with open(salida, "w", encoding="utf-8") as fh:
        json.dump(catalogo, fh, ensure_ascii=False, indent=1)
    indexables = sum(1 for i in catalogo["items"] if i["indexable"])
    oas = [i["ruta_relativa"] for i in catalogo["items"] if i["oa_candidato"]]
    print(f"items={catalogo['n_items']} indexables={indexables} -> {salida}")
    print(f"oa_candidatos={len(oas)} (verificar uno a uno, no asumir):")
    for o in oas:
        print(f"  ? {o}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# -*- coding: utf-8 -*-
"""Auditoría del corpus canónico — ¿el Concilio lee todo lo que dice leer?

Un tope excedido no produce un error: produce **silencio**. `_read_head`
recorta por la cabeza y añade un marcador al final, así que el oráculo lee un
archivo incompleto creyendo que eso es todo el texto. El recorte se descubre
semanas después, cuando alguien nota que el Concilio ignora algo que estaba
escrito.

Esta auditoría convierte ese silencio en un veredicto duro (exit code), para
que la degradación se vea el día que ocurre y no cuando ya dañó una decisión.

    .venv\\Scripts\\python.exe scripts\\auditar_canon.py

Caso real que la motivó (16-09-2026): `atribuciones_sinteticas.md` medía
46.920 chars con tope de 45.000 → se perdían 1.920 chars **del final**, que
eran justo su §3 ("cómo agregar una atribución") y su §4 (el ledger como
sustento). El Concilio deliberaba sin leer la regla que mantiene vivo su
propio registro.
"""

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from maxocontracts.concilio.canon import (  # noqa: E402
    DEFAULT_MAX_CHARS,
    auditar_corpus,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Audita el corpus canónico contra los topes de CANON_FILES"
    )
    parser.add_argument(
        "--root",
        default=str(REPO),
        help="raíz del repo a auditar (por defecto, este repositorio)",
    )
    args = parser.parse_args(argv)
    root = str(args.root)
    estados = auditar_corpus(root)
    recortadas = [e for e in estados if e.recortado]

    print("=== AUDITORIA DEL CORPUS CANONICO ===")
    print(f"{'fuente':60} {'real':>8} {'tope':>8}  estado")
    print("-" * 96)
    for e in estados:
        if not e.existe:
            estado = "AUSENTE"
        elif e.recortado:
            estado = f"RECORTADO (-{e.caracteres - e.tope})"
        else:
            estado = f"ok (+{e.holgura} holgura)"
        print(f"{e.ruta:60} {e.caracteres:>8} {e.tope:>8}  {estado}")
    print("-" * 96)

    total = sum(e.caracteres for e in estados if e.existe)
    print(f"suma de fuentes: {total} chars | tope del corpus: {DEFAULT_MAX_CHARS}")

    if recortadas:
        print()
        for e in recortadas:
            print(
                f"[XX] {e.ruta} excede su tope en {e.caracteres - e.tope} chars: "
                "el Concilio NO lee su final. Sube el tope en CANON_FILES o "
                "recorta el documento a mano — pero no dejes que se pierda en silencio."
            )
        print(f"\n>> CANON: {len(recortadas)} fuente(s) se leen incompletas.")
        return 1

    print("\n>> CANON: integro. El Concilio lee todo lo que dice leer.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""Tests de la auditoría del corpus canónico.

Motivación verificada (16-09-2026): `docs/architecture/atribuciones_sinteticas.md`
medía 46.920 chars con un tope de 45.000 en `CANON_FILES`. `_read_head` recorta
por la cabeza, así que se perdían 1.920 chars **del final** — que eran su §3
("cómo agregar una atribución") y su §4 (el ledger como sustento). El Concilio
deliberaba sin leer la regla que mantiene vivo su propio registro.

El primer test de este archivo es la regresión: si alguien vuelve a exceder un
tope, falla el día que ocurre en vez de descubrirse semanas después.
"""

import sys
from pathlib import Path

import pytest

from maxocontracts.concilio.canon import (
    CANON_FILES,
    DEFAULT_MAX_CHARS,
    EstadoArchivo,
    auditar_corpus,
    fuentes_recortadas,
    read_canon,
)

REPO = Path(__file__).resolve().parents[1]


# ── La regresión sobre el repo real ───────────────────────────────


def test_ninguna_fuente_del_canon_esta_recortada():
    """El Concilio debe leer todo lo que dice leer.

    Si esto falla, NO se arregla bajando el test: se sube el tope en
    `CANON_FILES` o se recorta el documento a mano. Un recorte silencioso es
    una amputación silenciosa de la memoria del sistema.
    """
    recortadas = fuentes_recortadas(str(REPO))
    detalle = "; ".join(f"{e.ruta} ({e.caracteres} > {e.tope})" for e in recortadas)
    assert recortadas == [], f"fuentes del canon recortadas: {detalle}"


def test_el_corpus_ensamblado_no_contiene_ningun_recorte():
    """El invariante real: ninguna fuente aparece recortada en el corpus final.

    Nota de diseño (16-09-2026): los topes por archivo son techos INDIVIDUALES,
    no una partición del presupuesto global — su suma (343.000) supera a
    `DEFAULT_MAX_CHARS` a propósito, porque ningún archivo llega a su techo a la
    vez. Por eso el invariante no se comprueba sumando topes (error de la
    primera versión de este test) sino buscando la marca de recorte en el corpus
    ya ensamblado: si no está, el Concilio leyó todo.
    """
    corpus = read_canon(str(REPO))
    assert "[recortado por el Concilio]" not in corpus
    assert len(corpus) <= DEFAULT_MAX_CHARS


def test_el_corpus_deja_margen_para_la_proxima_sesion():
    """El corpus crece (el registro crece): debe quedar sitio antes del techo."""
    margen = DEFAULT_MAX_CHARS - len(read_canon(str(REPO)))
    assert margen >= 2_000, (
        f"margen {margen} sobre el presupuesto {DEFAULT_MAX_CHARS}: "
        "la próxima entrada del registro podría empujar el corpus al recorte"
    )


def test_el_registro_tiene_margen_para_la_proxima_entrada():
    """El registro crece por diseño (§3): debe quedar sitio para la próxima sesión.

    No se exige un porcentaje grande a propósito: medido el 16-09-2026, el tope
    máximo del registro que mantiene el peor caso dentro del presupuesto global
    es 56.981, así que el registro vive cerca de su techo. Cuando este margen se
    agote, el arreglo NO es subir el tope otra vez: es destilar el registro
    (comprimir entradas antiguas), igual que la memoria del workspace destila
    los diarios de más de 30 días. Una memoria que crece sin mantenimiento se
    recorta sola tarde o temprano.
    """
    registro = next(
        e
        for e in auditar_corpus(str(REPO))
        if e.ruta.endswith("atribuciones_sinteticas.md")
    )
    assert registro.existe
    assert registro.holgura >= 2_000, (
        f"holgura {registro.holgura} sobre tope {registro.tope}: "
        "el registro está a punto de recortarse otra vez — destilar, no ampliar"
    )


def test_el_corpus_ensamblado_cabe_en_el_tope_global():
    corpus = read_canon(str(REPO))
    assert len(corpus) <= DEFAULT_MAX_CHARS


def test_todos_los_archivos_del_canon_existen():
    faltantes = [e.ruta for e in auditar_corpus(str(REPO)) if not e.existe]
    assert faltantes == [], f"fuentes ausentes del canon: {faltantes}"


# ── La auditoría en sí (con raíz temporal) ────────────────────────


def _raiz_falsa(tmp_path: Path, exceder: str = "", faltar: str = "") -> Path:
    """Crea las rutas de CANON_FILES con contenido mínimo y controlado."""
    for ruta, tope in CANON_FILES:
        destino = tmp_path / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        if ruta == faltar:
            continue
        if ruta == exceder:
            destino.write_text("x" * (tope + 37), encoding="utf-8")
        else:
            destino.write_text("contenido breve\n", encoding="utf-8")
    return tmp_path


def test_detecta_una_fuente_recortada(tmp_path):
    raiz = _raiz_falsa(tmp_path, exceder="maxocontracts/core/axioms.py")
    recortadas = fuentes_recortadas(str(raiz))
    assert [e.ruta for e in recortadas] == ["maxocontracts/core/axioms.py"]
    estado = recortadas[0]
    assert estado.recortado is True
    assert estado.holgura == 0
    assert estado.caracteres - estado.tope == 37


def test_corpus_integro_no_reporta_nada(tmp_path):
    raiz = _raiz_falsa(tmp_path)
    assert fuentes_recortadas(str(raiz)) == []
    estados = auditar_corpus(str(raiz))
    assert len(estados) == len(CANON_FILES)
    assert all(e.existe and not e.recortado for e in estados)


def test_reporta_archivo_ausente_sin_reventar(tmp_path):
    raiz = _raiz_falsa(tmp_path, faltar="maxocontracts/core/axioms.py")
    estados = {e.ruta: e for e in auditar_corpus(str(raiz))}
    ausente = estados["maxocontracts/core/axioms.py"]
    assert ausente.existe is False
    assert ausente.caracteres == 0
    # Ausente no es lo mismo que recortado: no cuenta como amputación.
    assert ausente.recortado is False
    assert fuentes_recortadas(str(raiz)) == []


def test_estado_archivo_es_inmutable():
    estado = EstadoArchivo("x.md", True, 10, 20)
    with pytest.raises(Exception):
        estado.tope = 99  # type: ignore[misc]


# ── El comando (veredicto duro) ───────────────────────────────────


def _cargar_script():
    sys.path.insert(0, str(REPO / "scripts"))
    import auditar_canon

    return auditar_canon


def test_el_comando_sale_cero_con_corpus_integro(tmp_path):
    script = _cargar_script()
    assert script.main(["--root", str(_raiz_falsa(tmp_path))]) == 0


def test_el_comando_sale_uno_con_fuente_recortada(tmp_path, capsys):
    script = _cargar_script()
    raiz = _raiz_falsa(tmp_path, exceder="docs/SESION_NEXT_PROMPT.md")
    assert script.main(["--root", str(raiz)]) == 1
    salida = capsys.readouterr().out
    assert "RECORTADO" in salida
    assert "se leen incompletas" in salida


def test_el_comando_corre_sobre_el_repo_real(capsys):
    script = _cargar_script()
    assert script.main([]) == 0
    assert "integro" in capsys.readouterr().out

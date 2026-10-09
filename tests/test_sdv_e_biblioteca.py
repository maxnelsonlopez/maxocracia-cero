# -*- coding: utf-8 -*-
"""Auditoria estructural determinista de la biblioteca SDV-E (Reino Natural).

Regla del proyecto: una biblioteca de referencia no se cree, se verifica.
Este test no juzga la prosa: comprueba que cada documento del estandar
cumpla la plantilla canonica y las reglas duras del brief maestro.

Que se verifica (sin red, determinista):
  1. Encabezado: titulo H1.
  2. Secciones obligatorias de la plantilla (14 secciones del brief).
  3. Separacion MINIMO ABSOLUTO vs OPTIMO (el error historico del SDV-H
     fue confundir el optimo del agua con su minimo).
  4. Las cuatro frases prohibidas del validador conceptual.
  5. Cero enlaces `file:///` y cero anclas de linea (`#L12-L34`):
     el canon manda citar archivos y secciones, nunca numeros de linea.
  6. Sustento documental: al menos 3 URLs http(s) verificables por documento
     y una seccion de Referencias con enlaces.
  7. Cuerpo minimo: un estandar no es un resumen.

El estado HTTP real de esos enlaces lo comprueba, aparte y contra la red,
`scripts/verificar_enlaces_sdv_e.py` (regla M15: jamas URLs alucinadas).

Si la biblioteca aun no existe, el test se salta: no rompe la suite.
"""

import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
BIBLIOTECA = REPO / "docs" / "theory" / "SDV-E"

# Fuente unica de verdad: la lista de frases vetadas vive en el validador
# conceptual. Copiarla aqui haria que este propio archivo contuviera las frases
# prohibidas —el validador escanea todo el repo, incluido este test— y ademas
# las duplicaria, con riesgo de que se desincronicen.
sys.path.insert(0, str(REPO / "scripts"))
from validador_conceptual import GLOBAL_FORBIDDEN_PHRASES  # noqa: E402

FRASES_PROHIBIDAS = tuple(GLOBAL_FORBIDDEN_PHRASES)

# El indice no es un estandar: se rige por otras reglas.
EXENTOS = {"00_README_indice.md"}
PREFIJOS_EXENTOS = ("_",)

SECCIONES_OBLIGATORIAS = (
    "Preambulo metodologico",
    "Pilares epistemologicos",
    "Dimensiones del SDV-E",
    "Protocolo de medicion",
    "Estado de implementacion",
    "Preguntas abiertas",
    "Referencias",
)

RE_ANCLA_LINEA = re.compile(r"#L\d+")
RE_FILE_URL = re.compile(r"file:///")
RE_URL = re.compile(r"https?://[^\s\)\]\>\"'`,;]+")

# La negacion ("no votable", "no es votable", "no se vota/n") contiene como
# subcadena la afirmacion ("votable", "se vota"). Un `in` ingenuo hace que
# cualquier documento que declare LEY pase gratis el chequeo de POLITICA.
# Por eso la negacion se detecta con regex y la afirmacion se busca SOLO
# despues de retirar las negaciones del texto.
RE_NEGACION_VOTO = re.compile(r"\bno[\s\-]+(?:es\s+|son\s+|se\s+)?vot\w*\b")

MIN_LINEAS = 80
MIN_URLS = 3


@pytest.fixture(autouse=True)
def _requiere_biblioteca():
    """Sin biblioteca no hay nada que auditar: se salta el modulo entero.

    Evita el falso verde de tests que iteran sobre una lista vacia.
    """
    if not BIBLIOTECA.exists():
        pytest.skip(f"La biblioteca {BIBLIOTECA.name}/ aun no existe")


def _sin_tildes(texto: str) -> str:
    """Normaliza para comparar titulos sin depender de acentos."""
    reemplazos = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    return texto.translate(reemplazos)


def documentos():
    if not BIBLIOTECA.exists():
        return []
    return [
        ruta
        for ruta in sorted(BIBLIOTECA.rglob("*.md"))
        if ruta.name not in EXENTOS and not ruta.name.startswith(PREFIJOS_EXENTOS)
    ]


def test_la_biblioteca_existe_y_tiene_documentos():
    """La rama SDV-E debe existir con documentos, o el test se salta."""
    if not BIBLIOTECA.exists():
        pytest.skip(f"La biblioteca {BIBLIOTECA.name}/ aun no existe")
    docs = documentos()
    assert docs, f"{BIBLIOTECA.name}/ existe pero no contiene documentos del estandar"
    assert len(docs) >= 9, (
        f"La biblioteca tiene {len(docs)} documentos; la rama SDV-E exige al menos "
        "la columna doctrinal completa (9 documentos)"
    )


def test_plantilla_canonica_en_cada_documento():
    """Cada documento cumple las secciones obligatorias del brief maestro."""
    fallos = []
    for ruta in documentos():
        texto = ruta.read_text(encoding="utf-8", errors="ignore")
        plano = _sin_tildes(texto).lower()
        nombre = ruta.name

        if not re.search(r"^#\s+\S", texto, re.MULTILINE):
            fallos.append(f"{nombre}: falta el titulo H1")

        for seccion in SECCIONES_OBLIGATORIAS:
            if _sin_tildes(seccion).lower() not in plano:
                fallos.append(f"{nombre}: falta la seccion '{seccion}'")

        lineas = texto.count("\n") + 1
        if lineas < MIN_LINEAS:
            fallos.append(
                f"{nombre}: solo {lineas} lineas (minimo {MIN_LINEAS}): un estandar "
                "no es un resumen"
            )

    assert not fallos, "Plantilla incompleta:\n  - " + "\n  - ".join(fallos)


def test_minimo_absoluto_separado_del_optimo():
    """El piso (LEY) nunca se confunde con la plenitud (POLITICA).

    Precedente: el motor del SDV-H tomo el optimo del agua (50-100 L/dia)
    como minimo, cuando el minimo absoluto es 20 L/dia (OMS). El SDV-E no
    puede repetir ese error de mapeo.
    """
    fallos = []
    for ruta in documentos():
        plano = _sin_tildes(ruta.read_text(encoding="utf-8", errors="ignore")).lower()
        tiene_minimo = "minimo absoluto" in plano
        tiene_optimo = "optimo" in plano
        if not (tiene_minimo and tiene_optimo):
            fallos.append(
                f"{ruta.name}: minimo_absoluto={tiene_minimo} optimo={tiene_optimo} "
                "-> deben aparecer ambos y separados"
            )
    assert not fallos, "Minimo y optimo no estan separados:\n  - " + "\n  - ".join(
        fallos
    )


def _declara_ley(plano: str) -> bool:
    """True si el texto declara alguna parte como no votable (LEY).

    Cubre "no votable", "no es/son votable/s" y "no se vota/n".
    """
    return bool(RE_NEGACION_VOTO.search(plano))


def _declara_politica(plano: str) -> bool:
    """True si el texto declara alguna parte afirmativamente votable (POLITICA).

    Las negaciones se retiran antes de buscar, para que "no votable" no
    cuente como declaracion de lo votable. Cubre "votable/s" y "se vota/n".
    """
    limpio = RE_NEGACION_VOTO.sub(" ", plano)
    return ("votable" in limpio) or ("se vota" in limpio) or ("se votan" in limpio)


def test_ley_y_politica_declaradas():
    """Todo estandar del reino natural distingue lo no votable de lo votable."""
    fallos = []
    for ruta in documentos():
        plano = _sin_tildes(ruta.read_text(encoding="utf-8", errors="ignore")).lower()
        if not _declara_ley(plano):
            fallos.append(f"{ruta.name}: no declara que parte es LEY (no votable)")
        if not _declara_politica(plano):
            fallos.append(f"{ruta.name}: no declara que parte es POLITICA (votable)")
    assert not fallos, "LEY/POLITICA sin declarar:\n  - " + "\n  - ".join(fallos)


def test_ley_politica_distinguen_negacion_de_afirmacion():
    """Regresion: "no votable" no debe contar como declaracion de POLITICA.

    El chequeo anterior usaba `"votable" in texto`, y como "no votable"
    contiene "votable", todo documento con LEY pasaba gratis POLITICA.
    """
    solo_ley = _sin_tildes("El piso es LEY (no votable).").lower()
    assert _declara_ley(solo_ley)
    assert not _declara_politica(solo_ley)

    solo_ley_vota = _sin_tildes("El piso no se vota.").lower()
    assert _declara_ley(solo_ley_vota)
    assert not _declara_politica(solo_ley_vota)

    solo_politica = _sin_tildes("La plenitud es POLITICA (votable).").lower()
    assert _declara_politica(solo_politica)

    solo_politica_vota = _sin_tildes("La plenitud si se vota.").lower()
    assert _declara_politica(solo_politica_vota)

    ambas = _sin_tildes(
        "El piso es LEY y no se vota; la plenitud es POLITICA y si se vota."
    ).lower()
    assert _declara_ley(ambas)
    assert _declara_politica(ambas)


def test_prohibiciones_del_validador_conceptual():
    """Las cuatro frases vetadas del repo no aparecen en la biblioteca."""
    fallos = []
    for ruta in documentos():
        bajo = ruta.read_text(encoding="utf-8", errors="ignore").lower()
        for frase in FRASES_PROHIBIDAS:
            if frase in bajo:
                fallos.append(f"{ruta.name}: frase prohibida -> '{frase}'")
    assert not fallos, "Frases prohibidas:\n  - " + "\n  - ".join(fallos)


def test_sin_anclas_de_linea_ni_file_url():
    """El canon prohibe citar numeros de linea y rutas absolutas locales."""
    fallos = []
    for ruta in documentos():
        texto = ruta.read_text(encoding="utf-8", errors="ignore")
        if RE_FILE_URL.search(texto):
            fallos.append(f"{ruta.name}: contiene un enlace file:///")
        for ancla in RE_ANCLA_LINEA.findall(texto):
            fallos.append(f"{ruta.name}: ancla de linea '{ancla}' (cita por seccion)")
    assert not fallos, "Anclas inestables:\n  - " + "\n  - ".join(fallos)


def test_sustento_documental_minimo():
    """Una biblioteca de referencia cita fuentes externas, no solo a si misma."""
    fallos = []
    for ruta in documentos():
        texto = ruta.read_text(encoding="utf-8", errors="ignore")
        urls = set(RE_URL.findall(texto))
        if len(urls) < MIN_URLS:
            fallos.append(
                f"{ruta.name}: {len(urls)} URLs (minimo {MIN_URLS}) -> sin sustento externo"
            )
    assert not fallos, "Sustento insuficiente:\n  - " + "\n  - ".join(fallos)

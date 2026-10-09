# -*- coding: utf-8 -*-
"""Auditoria aritmetica de los pesos del SDV-E (Reino Natural).

Regla del proyecto: una biblioteca de referencia no se cree, se verifica.
Este modulo no juzga la doctrina de los pesos (que son POLITICA y se votan):
comprueba que las tablas publiquen lo que sus propias filas suman.

Que se verifica (sin red, determinista):
  1. Cada vector `PESOS_TABLERO` suma 1,000: precondicion del tipo en el
     documento 07 (`abs(sum - 1) < 1e-9`) y del pseudocodigo del 08.
  2. Cada cifra declarada (Suma, Cobertura, Agujero) iguala el computo de
     sus filas: una suma publicada no es una intencion.
  3. Coherencia cruzada 07-vs-08: cada documento nombra la cifra del otro,
     para que la horquilla (suelo/caudal) no se vuelva silencio.
  4. El ejemplo canonico del 07 (§5.8): el Total iguala sus filas y el
     `v_tablero` iguala la suma de aportes.

Precedente que lo exige: la tabla del 07 §5.3 declaro `Suma 1,000` con filas
que sumaban 1,150, y el ejemplo declaro `v = 0,3804` con aportes que sumaban
0,4041. Los documentos 23 y 31 lo detectaron en prosa; este test lo detecta
por codigo para que no vuelva a entrar.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BIBLIOTECA = REPO / "docs" / "theory" / "SDV-E"
DOC07 = BIBLIOTECA / "07_Formula_de_violacion_y_pesos.md"
DOC08 = BIBLIOTECA / "08_INV2-E_invariante.md"
INDICE = BIBLIOTECA / "00_README_indice.md"

TOL_PESOS = 1e-9
TOL_EJEMPLO = 5e-4

RE_DECIMAL_COMA = re.compile(r"(\d+),(\d+)")


def _a_float(texto: str, ultimo: bool = False) -> float:
    """Decimal con coma de una celda (`0,300` -> 0.3).

    Con `ultimo=True` toma el ultimo (`1,000 − 0,075 = 0,925` -> 0.925):
    las celdas de cobertura escriben la derivacion y lo que vale es el
    resultado.
    """
    matches = RE_DECIMAL_COMA.findall(texto)
    if not matches:
        raise ValueError(f"sin decimal con coma en: {texto!r}")
    a, b = matches[-1] if ultimo else matches[0]
    return float(f"{a}.{b}")


def _es_separador(fila: str) -> bool:
    """Fila de guiones de tabla markdown (`|---|---|`)."""
    celdas = [c.strip() for c in fila.strip().strip("|").split("|")]
    return bool(celdas) and all(re.fullmatch(r":?-{2,}:?", c) for c in celdas)


def _filas_tabla(texto: str, ancla_cabecera: str):
    """Filas de datos de la tabla cuyo encabezado contiene el ancla.

    Empieza en la linea de encabezado y toma las lineas `|` consecutivas;
    se detiene en la primera linea que no es de tabla. Asi el recorte no
    depende de que exista un encabezado siguiente.
    """
    lineas = texto.splitlines()
    inicio = next(
        i
        for i, linea in enumerate(lineas)
        if linea.strip().startswith("|") and ancla_cabecera in linea
    )
    filas = []
    for linea in lineas[inicio + 1 :]:
        if not linea.strip().startswith("|"):
            break
        if _es_separador(linea):
            continue
        filas.append([c.strip() for c in linea.strip().strip("|").split("|")])
    return filas


def _es_fila_dato(fila, primera_col=0) -> bool:
    """True si la fila es de datos y no de totales/declaraciones."""
    nombre = fila[primera_col]
    if "Dimensi" in nombre or "Grupo" in nombre:
        return False
    return not any(
        marca in nombre for marca in ("Suma", "Cobertura", "Fracci", "Total")
    )


def _tabla_07():
    """Vector de §5.3 del 07: columnas TABLERO (2) y PISO (4)."""
    texto = DOC07.read_text(encoding="utf-8", errors="ignore")
    filas = _filas_tabla(texto, "PESOS_TABLERO")
    datos = [f for f in filas if _es_fila_dato(f)]
    tablero = sum(_a_float(f[2]) for f in datos)
    piso = sum(_a_float(f[4]) for f in datos)
    declarado = {}
    for f in filas:
        if "Cobertura" in f[0]:
            declarado["cobertura"] = _a_float(f[4], ultimo=True)
        elif "Suma" in f[0]:
            declarado["suma_tablero"] = _a_float(f[2])
            declarado["suma_piso"] = _a_float(f[4])
    return {"tablero": tablero, "piso": piso, **declarado}


def _tabla_08():
    """Vector de §5.2 del 08: peso unico (1), piso por bandera 🟢 (2).

    🟡 (umbral verificado sin coeficiente, regla 1) NO cuenta en PISO:
    produce violacion sin dimensionar `v`, como `arrecife_dhw`.
    """
    texto = DOC08.read_text(encoding="utf-8", errors="ignore")
    filas = _filas_tabla(texto, "Peso declarado")
    datos = [f for f in filas if _es_fila_dato(f)]
    tablero = sum(_a_float(f[1]) for f in datos)
    piso = sum(_a_float(f[1]) for f in datos if f[2].startswith("🟢"))
    declarado = {}
    for f in filas:
        nombre = f[0].strip()
        if nombre == "**Suma**":
            declarado["suma_tablero"] = _a_float(f[1])
        elif "tienen piso" in nombre:
            declarado["suma_piso"] = _a_float(f[1])
        elif "Fracci" in nombre:
            declarado["agujero"] = _a_float(f[1])
    return {"tablero": tablero, "piso": piso, **declarado}


def _tabla_indice():
    """Tabla del indice §3: catalogo (1) y piso declarado (2)."""
    texto = INDICE.read_text(encoding="utf-8", errors="ignore")
    filas = _filas_tabla(texto, "Peso (cat")
    datos = [f for f in filas if _es_fila_dato(f)]
    catalogo = sum(_a_float(f[1]) for f in datos)
    piso = sum(_a_float(f[2]) for f in datos)
    declarado = {}
    for f in filas:
        if "Total" in f[0]:
            declarado["total_catalogo"] = _a_float(f[1])
            declarado["total_piso"] = _a_float(f[2])
    return {"tablero": catalogo, "piso": piso, **declarado}


def test_tableros_suman_uno():
    """Todo PESOS_TABLERO suma 1,000: precondicion del motor (F4 del 07)."""
    tablas = {
        "07 §5.3": _tabla_07(),
        "08 §5.2": _tabla_08(),
        "indice §3": _tabla_indice(),
    }
    fallos = [
        f"{nombre}: Σ TABLERO = {valores['tablero']:.4f} (debe ser 1,000)"
        for nombre, valores in tablas.items()
        if abs(valores["tablero"] - 1.0) > TOL_PESOS
    ]
    assert not fallos, "TABLERO no suma 1,000:\n  - " + "\n  - ".join(fallos)


def test_sumas_declaradas_igualan_computo():
    """Ninguna Suma/Cobertura/Agujero publicada difiere de sus filas."""
    fallos = []

    t07 = _tabla_07()
    if abs(t07["suma_tablero"] - t07["tablero"]) > TOL_PESOS:
        fallos.append(
            f"07: Suma TABLERO declara {t07['suma_tablero']:.3f}, filas {t07['tablero']:.3f}"
        )
    if abs(t07["suma_piso"] - t07["piso"]) > TOL_PESOS:
        fallos.append(
            f"07: Suma PISO declara {t07['suma_piso']:.3f}, filas {t07['piso']:.3f}"
        )
    if abs(t07["cobertura"] - t07["piso"]) > TOL_PESOS:
        fallos.append(
            f"07: Cobertura declara {t07['cobertura']:.3f}, filas {t07['piso']:.3f}"
        )

    t08 = _tabla_08()
    if abs(t08["suma_tablero"] - t08["tablero"]) > TOL_PESOS:
        fallos.append(
            f"08: Suma TABLERO declara {t08['suma_tablero']:.3f}, filas {t08['tablero']:.3f}"
        )
    if abs(t08["suma_piso"] - t08["piso"]) > TOL_PESOS:
        fallos.append(
            f"08: Suma PISO declara {t08['suma_piso']:.3f}, filas 🟢 {t08['piso']:.3f}"
        )
    if abs(t08["agujero"] - (t08["tablero"] - t08["piso"])) > TOL_PESOS:
        fallos.append(
            f"08: Agujero declara {t08['agujero']:.3f}, "
            f"TABLERO-PISO {t08['tablero'] - t08['piso']:.3f}"
        )

    t00 = _tabla_indice()
    if abs(t00["total_catalogo"] - t00["tablero"]) > TOL_PESOS:
        fallos.append(
            f"indice: Total declara {t00['total_catalogo']:.3f}, filas {t00['tablero']:.3f}"
        )
    if abs(t00["total_piso"] - t00["piso"]) > TOL_PESOS:
        fallos.append(
            f"indice: PISO declara {t00['total_piso']:.3f}, filas {t00['piso']:.3f}"
        )

    assert not fallos, "Declarado != computado:\n  - " + "\n  - ".join(fallos)


def test_cobertura_cruzada_07_08():
    """Cada documento nombra la cifra del otro: la horquilla no se calla."""
    texto07 = DOC07.read_text(encoding="utf-8", errors="ignore")
    texto08 = DOC08.read_text(encoding="utf-8", errors="ignore")
    t07 = _tabla_07()
    t08 = _tabla_08()
    cifra08 = f"{t08['piso']:.3f}".replace(".", ",")
    cifra07 = f"{t07['piso']:.3f}".replace(".", ",")
    fallos = []
    if cifra08 not in texto07:
        fallos.append(f"07 no nombra la cobertura del 08 ({cifra08})")
    if cifra07 not in texto08:
        fallos.append(f"08 no nombra la cobertura del 07 ({cifra07})")
    assert not fallos, "Cobertura cruzada rota:\n  - " + "\n  - ".join(fallos)


def test_ejemplo_07_total_coherente():
    """El ejemplo §5.8: Total iguala filas y v_tablero iguala aportes."""
    texto = DOC07.read_text(encoding="utf-8", errors="ignore")
    filas = _filas_tabla(texto, "Aporte `v_k`")
    datos = [f for f in filas if _es_fila_dato(f)]
    total = next(f for f in filas if "Total" in f[0])
    suma_pesos = sum(_a_float(f[6]) for f in datos)
    suma_aportes = sum(_a_float(f[7]) for f in datos)
    peso_total = _a_float(total[6])
    v_total = _a_float(re.search(r"v_tablero\s*=\s*\d+,\d+", total[7]).group(0))
    fallos = []
    if abs(suma_pesos - peso_total) > TOL_PESOS:
        fallos.append(
            f"ejemplo: Total PESOS declara {peso_total:.3f}, filas {suma_pesos:.3f}"
        )
    if abs(suma_aportes - v_total) > TOL_EJEMPLO:
        fallos.append(
            f"ejemplo: v_tablero declara {v_total:.4f}, aportes {suma_aportes:.4f}"
        )
    assert not fallos, "Ejemplo incoherente:\n  - " + "\n  - ".join(fallos)


def test_helpers_pesos():
    """Regresion de los helpers: coma decimal, separadores y 🟡 excluida."""
    assert _a_float("**0,300**") == 0.3
    assert _a_float("0,075 (conectividad)") == 0.075
    assert _es_separador("|---|---|---|")
    assert not _es_separador("| Biodiversidad | 0,300 |")
    assert not _es_fila_dato(["**Suma**", "**1,000**"])
    assert _es_fila_dato(["Biodiversidad", "**0,300**"])
    # 🟡 con umbral sin coeficiente no entra en PISO (regla 1 del 08).
    filas = [
        ["Aire", "**0,20**", "🟢 sí (proxy)"],
        ["Oxígeno", "**0,02**", "🟡 con umbral, sin coeficiente (regla 1)"],
        ["Conectividad", "**0,075**", "🔴 no"],
        ["**Suma**", "**1,000**", "—"],
    ]
    datos = [f for f in filas if _es_fila_dato(f)]
    piso = sum(_a_float(f[1]) for f in datos if f[2].startswith("🟢"))
    assert abs(piso - 0.20) < TOL_PESOS

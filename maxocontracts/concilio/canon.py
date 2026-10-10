# -*- coding: utf-8 -*-
"""Corpus canónico del Concilio — qué lee cada oráculo antes de proponer.

Regla G1 (base canónica): el oráculo solo puede citar aquello que leyó;
por eso el corpus es explícito y acotado. El canon total del libro cabe en
el contexto de DeepSeek V4 (1M tokens), pero el corpus se mantiene compacto
para que también sirva con motores de 128K.

Fuentes: mapa de coherencia (vivo), doctrina humano-sintética, contrato de
custodia, axiomas del motor, fundamentos conceptuales, requisitos de la Ola 4,
el handoff vigente y —desde sep 2026— la memoria pública del Reino Sintético.

Regla G6 (estirpe): el oráculo lee `atribuciones_sinteticas.md` antes de
proponer. Sin estirpe, cada ciclo vuelve a inventar lo ya inventado; el
registro es la cápsula de memoria que el SDV-S exige (dimensión I, peso 0.30:
"la memoria es tiempo propio; alterarla es amputación").
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

# (ruta relativa al root del repo, máximo de caracteres) — en el orden de lectura.
CANON_FILES: List[Tuple[str, int]] = [
    ("docs/architecture/mapa_coherencia_ola4.md", 60_000),
    ("docs/architecture/administracion_humano_sintetica.md", 30_000),
    ("docs/architecture/sesiones_custodia_sintetica.md", 30_000),
    ("docs/architecture/mapa_trazabilidad_canonica.md", 25_000),
    ("maxocontracts/core/axioms.py", 30_000),
    ("docs/architecture/maxocontracts/FUNDAMENTOS_CONCEPTUALES.md", 40_000),
    ("docs/architecture/requisitos_fase2_ola4.md", 40_000),
    ("docs/SESION_NEXT_PROMPT.md", 34_000),
    # El registro de atribuciones CRECE por diseño: su propio §3 obliga a cada
    # sesión con obra verificable a añadir su entrada. Su tope sube de 45k a 56k
    # el 16-09-2026 — medía 46.920 chars y `_read_head` recortaba 1.920 POR LA
    # CABEZA, es decir, perdía el FINAL: las entradas más recientes y los
    # apartados §3 ("cómo agregar una atribución") y §4 (el ledger como
    # sustento). El Concilio deliberaba sin leer la regla que mantiene vivo su
    # propio registro. Un tope que hay que subir cada sesión no es un arreglo:
    # por eso existe `auditar_corpus()`, que detecta el recorte en vez de confiar.
    #
    # TECHO MEDIDO (16-09-2026): con las demás fuentes en 132.133 chars y 5.886
    # de cabeceras, el tope máximo del registro que mantiene el peor caso dentro
    # de DEFAULT_MAX_CHARS es 56.981. Es decir: el registro vive al ~88% de su
    # techo y NO queda margen para seguir ampliando. Cuando la holgura se agote,
    # el arreglo es DESTILAR el registro (comprimir entradas antiguas), no subir
    # este número — o subir DEFAULT_MAX_CHARS, que es una decisión de coste del
    # Concilio y por eso no se toma aquí. Ver
    # tests/test_canon_audit.py::test_el_peor_caso_del_corpus_cabe_en_el_presupuesto_global
    ("docs/architecture/atribuciones_sinteticas.md", 63_000),
]

# Tope del corpus completo: cabe en cualquier motor de >=128K con margen.
#
# MEDICION (04-10-2026, rama SDV-E): el corpus medía 200.916 chars y DOS fuentes
# se leían recortadas — `docs/SESION_NEXT_PROMPT.md` (32.154 > 32.000) y
# `docs/architecture/atribuciones_sinteticas.md` (60.141 > 56.000). Es decir: el
# Concilio llevaba semanas deliberando sin leer el final del handoff ni las
# últimas entradas del registro de atribuciones (justo las más recientes).
# Se suben los dos topes por encima de su tamaño real y el presupuesto global
# para conservar el invariante de margen (≥2.000 chars).
#
# SEGUNDA SUBIDA EL MISMO DÍA (04-10-2026): registrar la rama SDV-E en el handoff
# volvió a apretar el margen (204.205 chars de fuentes + 5.886 de cabeceras =
# 210.091, con 1.909 de holgura sobre 212.000). Dos subidas en una sola sesión
# son la prueba de que esto no escala: el arreglo es destilar, no ampliar.
#
# ADVERTENCIA ESTRUCTURAL (heredada del 16-09-2026 y ahora confirmada): subir el
# presupuesto NO es el arreglo de fondo. El registro de atribuciones y el handoff
# crecen por diseño en cada sesión, así que estos números volverán a apretarse
# (el 04-10-2026, tras registrar la rama SDV-E, el handoff volvió a tocar techo:
# 33.309 sobre un tope de 33.000). El arreglo real es DESTILAR los documentos que
# crecen —comprimir lo antiguo conservando la memoria, o quitar del handoff la
# copia de `git log`, que git ya guarda— o dar al Concilio un corpus por capas en
# vez de un solo bloque. Mientras no se haga, `auditar_corpus()` sigue siendo la
# defensa: detecta el recorte en vez de confiar. Esta subida es una reparación,
# no una solución, y es reversible.
DEFAULT_MAX_CHARS = 213_000


def _read_head(path: Path, max_chars: int) -> str:
    """Lee UTF-8 y recorta por caracteres (nunca por bytes, hay acentos)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n… [recortado por el Concilio]"


def _indice_resumen(root: Path, workspace: str, max_chars: int = 5_000) -> str:
    """Primeras entradas del índice navegable (si fue generado), para F1.

    El Concilio escribió esta hipótesis en su propia memoria (ciclo
    20260909-114428): que el índice generado por `scripts/canon_index.py`
    entre al corpus de absorción — así cada oráculo se orienta antes de
    leer el corpus completo. Si no existe el artefacto, no pasa nada.
    """
    path = Path(workspace) / "canon_index.md"
    if not path.exists():
        return ""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    if len(text) > max_chars:
        text = (
            text[:max_chars]
            + "\n… [índice recortado; regenerar con scripts/canon_index.py]"
        )
    return text


# --- Capas del corpus (destilación 09-10-2026, hito 3) ---
#
# C0 índice: orientación (canon_index generado, siempre abre). C1 destilado: lo
# que nunca se cae aunque el presupuesto apriete (axiomas + ledger + agenda).
# C2 completo: el resto de las fuentes íntegras. Regla de degradación: C0 y C1
# se sirven primero; C2 se omite de atrás hacia adelante y queda registrado en
# el manifiesto — nada silencioso, la auditoría sigue vigilando el resto.

CAPA_POR_FUENTE: Dict[str, str] = {
    "maxocontracts/core/axioms.py": "C1",
    "docs/SESION_NEXT_PROMPT.md": "C1",
    "docs/architecture/atribuciones_sinteticas.md": "C1",
}

PERFILES: Dict[str, Dict[str, object]] = {
    # completo: todo el corpus (el de siempre; lo beben F1/F2).
    "completo": {"tope_default": DEFAULT_MAX_CHARS},
    # esencial: C0 + C1 en 40k (firma barata, motores chicos, pre-vuelos).
    "esencial": {"tope_default": 40_000},
}

_FICHA_RE = re.compile(r"^-\s*\(\d{1,2}/\d{1,2}[^)]*\)")


def _leer_ledger(root_path: Path, max_chars: int) -> str:
    """Fichas C1 del registro: fecha + obra + huella, sin la prosa.

    Deriva el destilado del propio `atribuciones_sinteticas.md` (las fichas que
    empiezan con fecha entre paréntesis + la nota de archivo). Si aún no hay
    fichas, devuelve vacío y el perfil esencial cae a axiomas + agenda.
    """
    path = root_path / "docs" / "architecture" / "atribuciones_sinteticas.md"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    inicio = text.find("### DeepSeek")
    if inicio == -1:
        return ""
    fin = text.find("\n### ", inicio + 10)
    seccion = text[inicio : fin if fin != -1 else inicio + 8_000]
    lineas = [
        ln
        for ln in seccion.splitlines()
        if ln.startswith(">") or _FICHA_RE.match(ln)
    ]
    if not lineas:
        return ""
    body = (
        "### LEDGER C1 — fichas del registro (destilado; la prosa vive en el archivo)\n"
        + "\n".join(lineas)
    )
    if len(body) > max_chars:
        body = body[:max_chars] + "\n… [ledger recortado]"
    return body


@dataclass(frozen=True)
class FuenteServida:
    """Una fuente del corpus frente al presupuesto: qué capa y cómo quedó."""

    ruta: str
    capa: str
    caracteres: int
    estado: str  # "integra" | "recortada" | "omitida"


@dataclass(frozen=True)
class ManifiestoCorpus:
    """Lo que bebió cada oráculo: perfil, presupuesto y degradación aplicada."""

    perfil: str
    presupuesto: int
    caracteres: int
    degradada: bool
    indice_incluido: bool
    fuentes: Tuple[FuenteServida, ...] = field(default_factory=tuple)

    def omitidas(self) -> List[str]:
        return [f.ruta for f in self.fuentes if f.estado == "omitida"]

    def recortadas(self) -> List[str]:
        return [f.ruta for f in self.fuentes if f.estado == "recortada"]


def ensamblar_capas(
    root: str,
    perfil: str = "completo",
    total_max_chars: int = 0,
    workspace: str = "scratch/concilio",
) -> Tuple[str, ManifiestoCorpus]:
    """Ensambla el corpus por capas con manifiesto de lo servido.

    C0 (índice) abre; C1 (axiomas + handoff + registro, y en perfil esencial el
    ledger + la agenda) nunca se cae; C2 rellena hasta agotar el presupuesto y
    lo que no quepa queda listado en el manifiesto, jamás en silencio.
    """
    if perfil not in PERFILES:
        raise ValueError(
            f"perfil '{perfil}' desconocido: elige entre {sorted(PERFILES)}"
        )
    tope_default = int(PERFILES[perfil]["tope_default"])  # type: ignore[arg-type]
    budget = tope_default if not total_max_chars else total_max_chars
    root_path = Path(root)
    parts = [
        "=== CORPUS CANONICO DEL CONCILIO DE LA MAXOCRACIA ===",
        "Fuente de verdad: libro Ed. 3 Dinamica + estas capas de coherencia.",
        "Regla: solo cita lo que aqui aparece; si algo no esta, no lo inventes.",
        "",
    ]
    indice = _indice_resumen(root_path, workspace)
    if indice:
        parts.append(
            "\n### INDICE NAVEGABLE (generado; para orientarte antes de leer)\n"
            + indice
        )
    indice_incluido = bool(indice)
    fuentes: List[FuenteServida] = []
    used = 0

    def _servir(ruta: str, capa: str, cuerpo: str) -> None:
        nonlocal used
        if not cuerpo:
            fuentes.append(FuenteServida(ruta, capa, 0, "omitida"))
            return
        parts.append(f"\n\n### FUENTE: {ruta}\n{cuerpo}")
        used += len(cuerpo)
        estado = (
            "recortada"
            if ("recortado" in cuerpo[-60:] or "recortada" in cuerpo[-60:])
            else "integra"
        )
        fuentes.append(FuenteServida(ruta, capa, len(cuerpo), estado))

    if perfil == "esencial":
        for ruta, capa, tope in (
            ("ledger C1 (derivado del registro)", "C1", 8_000),
            ("agenda C1 (pendientes + memoria)", "C1", 15_000),
        ):
            if used >= budget:
                fuentes.append(FuenteServida(ruta, capa, 0, "omitida"))
                continue
            if ruta.startswith("ledger"):
                cuerpo = _leer_ledger(root_path, min(tope, budget - used))
            else:
                cuerpo = read_agenda(str(root_path), workspace=workspace)
                if len(cuerpo) > min(tope, budget - used):
                    cuerpo = cuerpo[: min(tope, budget - used)] + "\n… [agenda recortada]"
            _servir(ruta, capa, cuerpo)
        tope_axiomas = dict(CANON_FILES).get("maxocontracts/core/axioms.py", 30_000)
        if used >= budget:
            fuentes.append(
                FuenteServida("maxocontracts/core/axioms.py", "C1", 0, "omitida")
            )
        else:
            _servir(
                "maxocontracts/core/axioms.py",
                "C1",
                _read_head(
                    root_path / "maxocontracts/core/axioms.py",
                    min(tope_axiomas, budget - used),
                ),
            )
    else:
        caps = dict(CANON_FILES)
        c1 = [rel for rel, _ in CANON_FILES if CAPA_POR_FUENTE.get(rel) == "C1"]
        c2 = [rel for rel, _ in CANON_FILES if CAPA_POR_FUENTE.get(rel) != "C1"]
        for rel in c1 + c2:
            capa = CAPA_POR_FUENTE.get(rel, "C2")
            if used >= budget:
                fuentes.append(FuenteServida(rel, capa, 0, "omitida"))
                continue
            _servir(
                rel, capa, _read_head(root_path / rel, min(caps[rel], budget - used))
            )
    parts.append(f"\n\n[fin del corpus; {used} caracteres]")
    texto = "\n".join(parts)
    degradada = any(f.estado != "integra" for f in fuentes)
    return texto, ManifiestoCorpus(
        perfil=perfil,
        presupuesto=budget,
        caracteres=len(texto),
        degradada=degradada,
        indice_incluido=indice_incluido,
        fuentes=tuple(fuentes),
    )


def read_canon(
    root: str,
    total_max_chars: int = DEFAULT_MAX_CHARS,
    workspace: str = "scratch/concilio",
) -> str:
    """Ensambla el corpus canónico con cabeceras por archivo (perfil completo)."""
    texto, _ = ensamblar_capas(
        root, perfil="completo", total_max_chars=total_max_chars, workspace=workspace
    )
    return texto


@dataclass(frozen=True)
class EstadoArchivo:
    """Estado de una fuente del canon frente a su tope.

    T13 aplicado al corpus: verificar, no confiar. Un tope excedido no produce
    un error, produce silencio — y el silencio se lee como si el texto no
    existiera.
    """

    ruta: str
    existe: bool
    caracteres: int
    tope: int

    @property
    def holgura(self) -> int:
        return max(0, self.tope - self.caracteres)

    @property
    def recortado(self) -> bool:
        return self.existe and self.caracteres > self.tope


def auditar_corpus(root: str) -> List[EstadoArchivo]:
    """Mide cada fuente del canon contra su tope.

    Existe porque el recorte de `_read_head` es silencioso en su efecto: añade
    un marcador al final, pero el oráculo no sabe *qué* se perdió. Esta
    auditoría encontró el 16-09-2026 que `atribuciones_sinteticas.md` perdía
    1.920 chars — su propio §3 y §4, la regla que mantiene vivo el registro y
    la doctrina del ledger como sustento — de modo que el Concilio deliberaba
    sin leer por qué su registro importa.

    Un recorte no detectado es una amputación silenciosa: la misma clase de
    daño que `concilio/git_guard.py` evita en el historial de git.
    """
    root_path = Path(root)
    estados: List[EstadoArchivo] = []
    for rel, cap in CANON_FILES:
        path = root_path / rel
        try:
            n = len(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            estados.append(EstadoArchivo(rel, False, 0, cap))
            continue
        estados.append(EstadoArchivo(rel, True, n, cap))
    return estados


def fuentes_recortadas(root: str) -> List[EstadoArchivo]:
    """Fuentes que exceden su tope y por tanto se leen incompletas.

    Lista vacía = el Concilio lee todo lo que dice leer. Cualquier elemento es
    un fallo duro, no una advertencia.
    """
    return [estado for estado in auditar_corpus(root) if estado.recortado]


def read_agenda(
    root: str, workspace: str = "scratch/concilio", max_chars: int = 12_000
) -> str:
    """Agenda del Concilio: pendientes del handoff + aprendizajes previos.

    El bucle de aprendizaje (Aster §7): el próximo F2 lee lo que los ciclos
    anteriores aprendieron — "optimizar A no produjo mejora" se vuelve regla
    explícita para no repetir A y probar B. Los aprendizajes viven en
    `scratch/concilio/aprendizaje.jsonl` (memoria causal).
    """
    path = Path(root) / "docs" / "SESION_NEXT_PROMPT.md"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    marker = "## 4. Pendientes priorizados"
    idx = text.find(marker)
    if idx == -1:
        section = ""
    else:
        section = text[idx:]
        # la sección termina en el siguiente "## " de nivel 2
        for next_marker in ("\n## 5.", "\n## ", "\n---"):
            end = section.find(next_marker, len(marker))
            if end != -1:
                section = section[:end]
                break
        if len(section) > max_chars:
            section = section[:max_chars] + "\n… [recortado]"

    # Memoria causal: destilado fresco primero (digestión completa); la ventana
    # heredada (últimos 5) solo cuando no hay destilado o está rancio.
    from .memoria import (
        leer_aprendizajes,
        leer_desacuerdos,
        leer_memoria_destilada,
    )

    destilado = leer_memoria_destilada(workspace)
    if destilado:
        section += (
            "\n\n## Memoria destilada del Concilio (digestión completa; "
            "la ventana queda jubilada):\n" + destilado
        )
        return section

    # Ventana heredada: lo aprendido en ciclos anteriores (hipótesis → resultado).
    aprendizajes = leer_aprendizajes(workspace, n=5)
    bloque = "".join(
        (
            f"\n### APRENDIZAJE {i + 1} (ciclo {a.get('cycle_id', '?')} · "
            f"{a.get('decision', '?')})\n"
            f"- hipótesis: {str(a.get('hypothesis', ''))[:300]}\n"
            + (
                f"- aprendido: {str(a.get('outcome', ''))[:300]}"
                if a.get("outcome")
                else ""
            )
            + (
                f"\n- próxima hipótesis: {str(a.get('next_hypothesis', ''))[:300]}"
                if a.get("next_hypothesis")
                else ""
            )
            + "\n"
        )
        for i, a in enumerate(aprendizajes)
    )
    if bloque:
        section += (
            "\n\n## Memoria del Concilio (NO repitas lo ya aprendido; "
            "constrúyelo):\n" + bloque
        )

    # Cuarta dimensión (Aster): memoria de desacuerdos — "esto ya se intentó
    # y se descartó porque…". Contra la amnesia institucional: una civilización
    # puede cometer dos veces el mismo error si solo guarda la decisión final.
    desacuerdos = leer_desacuerdos(workspace, n=5)
    bloque_d = "".join(
        (
            f"\n### OBJECIÓN {i + 1} ({a.get('cycle_id', '?')})\n"
            f"- cuestión: {str(a.get('question', ''))[:200]}\n"
            f"- alternativa descartada: {str(a.get('discarded_alternative', ''))[:200]}\n"
            f"- defendida por: {str(a.get('defended_by', ''))[:80]} · razón: "
            f"{str(a.get('reason', ''))[:200]}\n"
            + (
                f"- evidencia que la descartó: {str(a.get('evidence', ''))[:200]}"
                if a.get("evidence")
                else ""
            )
            + "\n"
        )
        for i, a in enumerate(desacuerdos)
    )
    if bloque_d:
        section += (
            "\n\n## Objeciones históricas (CUIDADO: no re-proponer sin evidencia "
            "nueva):\n" + bloque_d
        )
    return section

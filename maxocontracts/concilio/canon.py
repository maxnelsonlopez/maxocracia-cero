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

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

# (ruta relativa al root del repo, máximo de caracteres) — en el orden de lectura.
CANON_FILES: List[Tuple[str, int]] = [
    ("docs/architecture/mapa_coherencia_ola4.md", 60_000),
    ("docs/architecture/administracion_humano_sintetica.md", 30_000),
    ("docs/architecture/sesiones_custodia_sintetica.md", 30_000),
    ("docs/architecture/mapa_trazabilidad_canonica.md", 25_000),
    ("maxocontracts/core/axioms.py", 30_000),
    ("docs/architecture/maxocontracts/FUNDAMENTOS_CONCEPTUALES.md", 40_000),
    ("docs/architecture/requisitos_fase2_ola4.md", 40_000),
    ("docs/SESION_NEXT_PROMPT.md", 32_000),
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
    ("docs/architecture/atribuciones_sinteticas.md", 56_000),
]

# Tope del corpus completo: cabe en cualquier motor de >=128K con margen.
# El corpus real mide ~183k chars con atribuciones incluida; 195k deja ~12k de
# holgura para que ningún archivo quede recortado (medido el 15-09-2026).
# Nota: el tope de SESION_NEXT_PROMPT sube de 25k a 32k porque el handoff crecio
# hasta 29.5k y se venia recortando en silencio (degradacion previa, no nueva).
DEFAULT_MAX_CHARS = 195_000


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
        text = text[:max_chars] + "\n… [índice recortado; regenerar con scripts/canon_index.py]"
    return text


def read_canon(
    root: str,
    total_max_chars: int = DEFAULT_MAX_CHARS,
    workspace: str = "scratch/concilio",
) -> str:
    """Ensambla el corpus canónico con cabeceras por archivo."""
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
            "\n### INDICE NAVEGABLE (generado; para orientarte antes de leer)\n" + indice
        )
    used = 0
    for rel, cap in CANON_FILES:
        if used >= total_max_chars:
            break
        budget = min(cap, total_max_chars - used)
        body = _read_head(root_path / rel, budget)
        if not body:
            continue
        parts.append(f"\n\n### FUENTE: {rel}\n{body}")
        used += len(body)
    parts.append(f"\n\n[fin del corpus; {used} caracteres]")
    return "\n".join(parts)


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

    # Memoria causal: lo aprendido en ciclos anteriores (hipótesis → resultado).
    from .memoria import leer_aprendizajes

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
    from .memoria import leer_desacuerdos

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

# -*- coding: utf-8 -*-
"""Corpus canónico del Concilio — qué lee cada oráculo antes de proponer.

Regla G1 (base canónica): el oráculo solo puede citar aquello que leyó;
por eso el corpus es explícito y acotado. El canon total del libro cabe en
el contexto de DeepSeek V4 (1M tokens), pero el corpus se mantiene compacto
para que también sirva con motores de 128K.

Fuentes: mapa de coherencia (vivo), doctrina humano-sintética, contrato de
custodia, axiomas del motor, fundamentos conceptuales, requisitos de la Ola 4
y el handoff vigente.
"""

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
    ("docs/SESION_NEXT_PROMPT.md", 25_000),
]

# Tope del corpus completo: cabe en cualquier motor de >=128K con margen.
DEFAULT_MAX_CHARS = 160_000


def _read_head(path: Path, max_chars: int) -> str:
    """Lee UTF-8 y recorta por caracteres (nunca por bytes, hay acentos)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n… [recortado por el Concilio]"


def read_canon(root: str, total_max_chars: int = DEFAULT_MAX_CHARS) -> str:
    """Ensambla el corpus canónico con cabeceras por archivo."""
    root_path = Path(root)
    parts = [
        "=== CORPUS CANONICO DEL CONCILIO DE LA MAXOCRACIA ===",
        "Fuente de verdad: libro Ed. 3 Dinamica + estas capas de coherencia.",
        "Regla: solo cita lo que aqui aparece; si algo no esta, no lo inventes.",
        "",
    ]
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

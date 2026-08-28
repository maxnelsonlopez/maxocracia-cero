# -*- coding: utf-8 -*-
"""
Árbol de Habilidades (el tejido) — motor de dominio puro.

El árbol de habilidades es el conocimiento total de la humanidad: el
**tejido** infinito y forkable; cada rama muta (OEV §1.8 — trama vs tejido).
El árbol es la trama común de la Maxocracia que arma el método de todos los
talleres; el contenido (matemáticas, cocina, programación, confección...) lo
siembran las propias comunidades.

Sea cada nodo un `SkillNode` con su id canónico (path `rama/nodo`), sus
prerrequisitos (un árbol — la maestría se encadena: no hay "años", hay
**caminos de maestría**) y su dificultad. La maestría NO se declara: se
gana por vacuación (obra aplicada + material publicado + mentoría, ver
`maxocontracts/skills.py`) y se valida por triada.

`evaluate_unlock` es el veredicto completo de un nodo: prerrequisitos
cumplidos + regla de oro + triada, todo con razones (T13).

Regla: los prerequisitos de un nodo DEBEN existir en el árbol, salvo que se
marquen como externos (`with_node(..., allow_external=[...])` para forks que
dependen de otros jardines); un nodo no puede ser su propio prerequisito
(guardarraíl anti-auto-certificación).
"""

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Iterable, List, Optional, Set, Tuple

from .skills import (
    TriadaVotos,
    VacuacionRequirements,
    DEFAULT_VACUACION_REQUIREMENTS,
    evaluate_triada,
    evaluate_vacuacion,
)

# Las 8 ramas canónicas del árbol inicial (el mismo cosmos del prototipo
# `plataforma_educativa/` — la máquina de datos siembra los temas dentro
# de estas ramas; el tejido se expande con cada taller).
CANONICAL_BRANCHES: Tuple[str, ...] = (
    "matematicas",
    "higiene",
    "relaciones",
    "lectura",
    "escritura",
    "lenguaje",
    "naturaleza",
    "computadores",
)


class SkillTreeError(ValueError):
    """Árbol mal formado (ids duplicados, prerequisitos ausentes o ciclos)."""


@dataclass(frozen=True)
class SkillNode:
    """Un nodo de skill: unidad de maestría del tejido."""

    id: str  # path canónico: "rama/nodo" (o "rama" para el nodo raíz)
    name: str
    branch: str  # rama del árbol
    prereq_ids: Tuple[str, ...] = ()
    dificultad: int = 1  # 1-5; orienta el ritmo, nunca el ranking (anti-gamificación)
    description: str = ""


@dataclass(frozen=True)
class MasteryState:
    """Conjunto inmutable de maestrías y nodos vistos (estado, no tribunal)."""

    mastered: FrozenSet[str] = frozenset()


@dataclass(frozen=True)
class UnlockResult:
    """Veredicto de apertura de un nodo (prerrequisitos + oro + triada)."""

    unlocked: bool
    prereqs_ok: bool
    vacua_faltantes: List[str] = field(default_factory=list)
    triada_bloqueos: List[str] = field(default_factory=list)
    razones: List[str] = field(default_factory=list)


class SkillTree:
    """Árbol inmutable de habilidades (el tejido), validado al construir.

    - ids únicos;
    - cada prerequisito existe en el árbol (o está en `allow_external`);
    - ningún nodo es su propio prerequisito (anti-auto-certificación);
    - el camino de prerequisitos no puede formar ciclos.
    """

    def __init__(
        self,
        nodes: Iterable[SkillNode],
        allow_external: Iterable[str] = (),
    ) -> None:
        self._nodes: Dict[str, SkillNode] = {}
        for node in nodes:
            if node.id in self._nodes:
                raise SkillTreeError(f"nodo duplicado: {node.id}")
            if node.id in node.prereq_ids:
                raise SkillTreeError(
                    f"un nodo no puede ser su propio prerrequisito: {node.id}"
                )
            self._nodes[node.id] = node

        external = set(allow_external)
        for node in self._nodes.values():
            for prereq in node.prereq_ids:
                if prereq == node.id:
                    raise SkillTreeError(
                        f"un nodo no puede ser su propio prerrequisito: {node.id}"
                    )
                if prereq not in self._nodes and prereq not in external:
                    raise SkillTreeError(
                        f"prerrequisito ausente: {node.id} -> {prereq}"
                    )

        self._assert_acyclic()

    def _assert_acyclic(self) -> None:
        visiting: Set[str] = set()
        visited: Set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in visiting:
                raise SkillTreeError(f"ciclo de prerrequisitos en: {node_id}")
            if node_id in visited:
                return
            visiting.add(node_id)
            node = self._nodes[node_id]
            for prereq in node.prereq_ids:
                if prereq in self._nodes:
                    visit(prereq)
            visiting.discard(node_id)
            visited.add(node_id)

        for node_id in self._nodes:
            visit(node_id)

    # -- consultas ----------------------------------------------------------

    def node(self, node_id: str) -> Optional[SkillNode]:
        return self._nodes.get(node_id)

    def branches(self) -> List[str]:
        return sorted({node.branch for node in self._nodes.values()})

    def nodes_by_branch(self, branch: str) -> List[SkillNode]:
        return sorted(
            (n for n in self._nodes.values() if n.branch == branch),
            key=lambda n: (n.dificultad, n.id),
        )

    def prereqs_met(self, node_id: str, state: MasteryState) -> bool:
        """Todos los prerrequisitos del nodo están dominados (maestría, no edad)."""
        node = self._nodes.get(node_id)
        if node is None:
            raise SkillTreeError(f"nodo desconocido: {node_id}")
        return all(prereq in state.mastered for prereq in node.prereq_ids)

    def path_of(self, node_id: str) -> List[str]:
        """Camino de maestría desde la raíz hasta el nodo (orden de conquista)."""
        node = self._nodes.get(node_id)
        if node is None:
            raise SkillTreeError(f"nodo desconocido: {node_id}")
        path: List[str] = []

        def walk(current: str) -> None:
            n = self._nodes[current]
            for prereq in n.prereq_ids:
                if prereq in self._nodes:
                    walk(prereq)
            if current not in path:
                path.append(current)

        walk(node_id)
        return path

    def with_node(
        self,
        node: SkillNode,
        allow_external: Iterable[str] = (),
    ) -> "SkillTree":
        """Fork del árbol con un nodo sembrado (el tejido se expande)."""
        nodes = list(self._nodes.values())
        if node.id in self._nodes:
            raise SkillTreeError(f"nodo duplicado: {node.id}")
        nodes.append(node)
        return SkillTree(nodes, allow_external=allow_external)


def build_canonical_tree() -> SkillTree:
    """El árbol canónico inicial: las 8 ramas como nodos raíz sin prerrequisitos.

    El cosmos completo (temas dentro de cada rama) lo siembran cada taller y
    el prototipo vivo `plataforma_educativa/` (8 ramas, 35 temas); este árbol
    es el mínimo común que garantiza coherencia de ramas en toda la red.
    """
    nodes = [
        SkillNode(
            id=branch,
            name=branch.capitalize(),
            branch=branch,
            prereq_ids=(),
            dificultad=1,
            description=f"Rama canónica '{branch}' del árbol de habilidades (OEV §1.8).",
        )
        for branch in CANONICAL_BRANCHES
    ]
    return SkillTree(nodes)


def is_valid_node_id(node_id: str) -> bool:
    """Formato canónico: `rama` o `rama/nodo` (slugs minúsculos con _ o -)."""
    if not node_id or not node_id.strip():
        return False
    parts = node_id.split("/")
    if len(parts) > 2:
        return False
    for part in parts:
        if not part or not part.replace("-", "").replace("_", "").isalnum():
            return False
    return True


def evaluate_unlock(
    tree: SkillTree,
    node_id: str,
    state: MasteryState,
    obra_aplicada: bool,
    material_publicado: bool,
    mentoria_horas: float,
    votos: TriadaVotos,
    requirements: VacuacionRequirements = DEFAULT_VACUACION_REQUIREMENTS,
) -> UnlockResult:
    """Veredicto completo de apertura: prerequisitos + oro + triada (T13).

    Un nodo solo se abre cuando el camino de maestría está caminado Y la
    regla de oro se cumple Y la triada aprueba (el oráculo con veto protege
    los axiomas; los humanos custodian el sentido).
    """
    node = tree.node(node_id)
    if node is None:
        raise SkillTreeError(f"nodo desconocido: {node_id}")

    prereqs_ok = tree.prereqs_met(node_id, state)
    vacua = evaluate_vacuacion(
        obra_aplicada, material_publicado, mentoria_horas, requirements
    )
    triada = evaluate_triada(votos)

    razones: List[str] = []
    if not prereqs_ok:
        faltantes = [
            p for p in node.prereq_ids if p not in state.mastered
        ]
        razones.append(f"prerrequisitos no dominados: {', '.join(faltantes)}")
    if not vacua.vacua:
        razones.append("regla de oro incompleta: " + ", ".join(vacua.faltantes))
    if not triada.aprobada:
        razones.append("triada incompleta: " + "; ".join(triada.bloqueos))

    unlocked = prereqs_ok and vacua.vacua and triada.aprobada
    return UnlockResult(
        unlocked=unlocked,
        prereqs_ok=prereqs_ok,
        vacua_faltantes=vacua.faltantes,
        triada_bloqueos=triada.bloqueos,
        razones=razones,
    )

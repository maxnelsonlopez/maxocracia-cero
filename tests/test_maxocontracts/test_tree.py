# -*- coding: utf-8 -*-
"""Tests del Árbol de Habilidades (M6 — rama educativa, motor puro).

maxocontracts/tree.py: el tejido — nodos con prerrequisitos (caminos de
maestría, no años), forkes, y el veredicto completo evaluate_unlock
(prerrequisitos + regla de oro + triada).
"""

import pytest

from maxocontracts.skills import TriadaVotos
from maxocontracts.tree import (
    MasteryState,
    SkillNode,
    SkillTree,
    SkillTreeError,
    build_canonical_tree,
    evaluate_unlock,
    is_valid_node_id,
)


def _huerta_tree():
    return SkillTree(
        [
            SkillNode(id="naturaleza", name="Naturaleza", branch="naturaleza"),
            SkillNode(
                id="naturaleza/tierras",
                name="Tierras",
                branch="naturaleza",
                prereq_ids=("naturaleza",),
            ),
            SkillNode(
                id="naturaleza/huertas",
                name="Huertas",
                branch="naturaleza",
                prereq_ids=("naturaleza/tierras",),
                dificultad=2,
            ),
        ]
    )


class TestValidacionDeArbol:
    def test_ids_unicos(self):
        with pytest.raises(SkillTreeError, match="duplicado"):
            SkillTree(
                [
                    SkillNode(id="rama/a", name="a", branch="rama"),
                    SkillNode(id="rama/a", name="b", branch="rama"),
                ]
            )

    def test_prerequisito_ausente(self):
        with pytest.raises(SkillTreeError, match="ausente"):
            SkillTree(
                [
                    SkillNode(
                        id="rama/b", name="b", branch="rama", prereq_ids=("rama/a",)
                    )
                ]
            )

    def test_prerequisito_externo_permitido(self):
        tree = SkillTree(
            [
                SkillNode(
                    id="rama/b", name="b", branch="rama", prereq_ids=("otro_jardin/x",)
                )
            ],
            allow_external=("otro_jardin/x",),
        )
        assert tree.node("rama/b") is not None

    def test_auto_prerequisito_rechazado(self):
        # Un nodo NO puede ser su propia llave (anti-auto-certificación).
        with pytest.raises(SkillTreeError, match="propio prerrequisito"):
            SkillTree(
                [
                    SkillNode(
                        id="rama/a", name="a", branch="rama", prereq_ids=("rama/a",)
                    )
                ]
            )

    def test_ciclos_rechazados(self):
        with pytest.raises(SkillTreeError, match="ciclo"):
            SkillTree(
                [
                    SkillNode(id="rama/a", name="a", branch="rama", prereq_ids=("rama/b",)),
                    SkillNode(id="rama/b", name="b", branch="rama", prereq_ids=("rama/a",)),
                ]
            )


class TestPrerequisitos:
    def test_prereqs_met(self):
        tree = _huerta_tree()
        state = MasteryState(mastered=frozenset(("naturaleza", "naturaleza/tierras")))
        assert tree.prereqs_met("naturaleza/huertas", state) is True

    def test_prereqs_no_met(self):
        tree = _huerta_tree()
        state = MasteryState(mastered=frozenset(("naturaleza",)))
        assert tree.prereqs_met("naturaleza/huertas", state) is False

    def test_raiz_sin_prereqs_siempre_abierta(self):
        tree = _huerta_tree()
        assert tree.prereqs_met("naturaleza", MasteryState()) is True

    def test_camino_de_maestria(self):
        tree = _huerta_tree()
        assert tree.path_of("naturaleza/huertas") == [
            "naturaleza",
            "naturaleza/tierras",
            "naturaleza/huertas",
        ]


class TestCanonicalYForks:
    def test_arbol_canonico_8_ramas(self):
        tree = build_canonical_tree()
        assert tree.branches() == [
            "computadores",
            "escritura",
            "higiene",
            "lectura",
            "lenguaje",
            "matematicas",
            "naturaleza",
            "relaciones",
        ]
        assert len(tree.branches()) == 8

    def test_segmento_canonico(self):
        tree = build_canonical_tree()
        assert tree.node("naturaleza").branch == "naturaleza"

    def test_fork_con_nodo_nuevo(self):
        tree = build_canonical_tree().with_node(
            SkillNode(
                id="gastronomia/fermentos",
                name="Fermentos",
                branch="gastronomia",
                prereq_ids=("higiene",),
            ),
            allow_external=("higiene",),
        )
        assert tree.node("gastronomia/fermentos") is not None
        assert tree.prereqs_met(
            "gastronomia/fermentos",
            MasteryState(mastered=frozenset(("higiene",))),
        )

    def test_duplicado_en_fork(self):
        tree = build_canonical_tree()
        with pytest.raises(SkillTreeError, match="duplicado"):
            tree.with_node(
                SkillNode(id="naturaleza", name="X", branch="naturaleza")
            )


class TestNodoId:
    def test_formatos_validos(self):
        assert is_valid_node_id("naturaleza")
        assert is_valid_node_id("naturaleza/huertas")
        assert is_valid_node_id("computadores/programacion_inicial")
        assert is_valid_node_id("rama/nodo-uno")

    def test_formatos_invalidos(self):
        assert is_valid_node_id("") is False
        assert is_valid_node_id("a/b/c") is False
        assert is_valid_node_id("sin espacio!") is False
        assert is_valid_node_id("  ") is False


class TestEvaluateUnlock:
    def test_apertura_completa(self):
        tree = _huerta_tree()
        state = MasteryState(mastered=frozenset(("naturaleza", "naturaleza/tierras")))
        resultado = evaluate_unlock(
            tree,
            "naturaleza/huertas",
            state,
            obra_aplicada=True,
            material_publicado=True,
            mentoria_horas=2.0,
            votos=TriadaVotos(mentor_ok=True, peer_ok=True),
        )
        assert resultado.unlocked is True
        assert resultado.prereqs_ok is True
        assert resultado.vacua_faltantes == []
        assert resultado.triada_bloqueos == []

    def test_falla_por_prerequisitos(self):
        tree = _huerta_tree()
        resultado = evaluate_unlock(
            tree,
            "naturaleza/huertas",
            MasteryState(mastered=frozenset(("naturaleza",))),
            obra_aplicada=True,
            material_publicado=True,
            mentoria_horas=2.0,
            votos=TriadaVotos(mentor_ok=True, peer_ok=True),
        )
        assert resultado.unlocked is False
        assert resultado.prereqs_ok is False
        assert "naturaleza/tierras" in resultado.razones[0]

    def test_falla_por_regla_de_oro(self):
        tree = _huerta_tree()
        state = MasteryState(mastered=frozenset(("naturaleza", "naturaleza/tierras")))
        resultado = evaluate_unlock(
            tree,
            "naturaleza/huertas",
            state,
            obra_aplicada=False,
            material_publicado=True,
            mentoria_horas=2.0,
            votos=TriadaVotos(mentor_ok=True, peer_ok=True),
        )
        assert resultado.unlocked is False
        assert resultado.vacua_faltantes == ["obra aplicada"]

    def test_falla_por_veto_del_oraculo(self):
        tree = _huerta_tree()
        state = MasteryState(mastered=frozenset(("naturaleza", "naturaleza/tierras")))
        resultado = evaluate_unlock(
            tree,
            "naturaleza/huertas",
            state,
            obra_aplicada=True,
            material_publicado=True,
            mentoria_horas=2.0,
            votos=TriadaVotos(mentor_ok=True, peer_ok=True, oracle_veto=True),
        )
        assert resultado.unlocked is False
        assert resultado.triada_bloqueos

    def test_nodo_desconocido_levanta(self):
        tree = _huerta_tree()
        with pytest.raises(SkillTreeError, match="desconocido"):
            evaluate_unlock(
                tree,
                "otro/nodo",
                MasteryState(),
                True,
                True,
                2.0,
                TriadaVotos(True, True),
            )

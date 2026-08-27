# -*- coding: utf-8 -*-
"""Test 5: el algoritmo puro de planificación de reuniones.

Aquí se prueba la función :func:`app.planner.plan_meetings` (agrupación por
similitud de perfiles, máx 8 por célula) y :func:`app.planner.assign_monitors`
(asignar monitor solo si está calificado).
"""

from app.planner import assign_monitors, plan_meetings


def _user(uid, weak):
    return {"user_id": uid, "weak_topics": weak}


def test_25_users_same_topic_produce_max8_and_min3_groups():
    """25 usuarios con el mismo tema débil -> células de a lo sumo 8 (>=4 grupos)."""
    users = [_user(i, [1]) for i in range(1, 26)]
    groups = plan_meetings(users, {})
    user_ids = groups

    assert len(user_ids) >= 4, f"Se esperaban al menos 4 grupos, se obtuvieron {len(user_ids)}"
    assert all(len(g["user_ids"]) <= 8 for g in user_ids), "Ningún grupo puede superar 8."
    assert all(len(g["user_ids"]) >= 3 for g in user_ids), "Reequilibrio: cada grupo >= 3."
    assert sum(len(g["user_ids"]) for g in user_ids) == 25, "No se pierden usuarios."


def test_groups_nearby_profiles_together():
    """Con perfiles distintos, se agrupa a los que comparten debilidades.

    8 usuarios débiles en {1,2,3} y 8 débiles en {1,4,5}, todos con el tema 1
    como más urgente. Al haber más de 8 por tema, la similitud separa a los que
    se parecen: los {1,2,3} quedan juntos y los {1,4,5} juntos.
    """
    users = [_user(i, [1, 2, 3]) for i in range(1, 9)]
    users += [_user(i, [1, 4, 5]) for i in range(9, 17)]

    groups = plan_meetings(users, {}, max_size=8)
    assert len(groups) == 2, f"Se esperaban 2 células, se obtuvieron {len(groups)}"
    assert all(len(g["user_ids"]) == 8 for g in groups)

    group_a = next(g for g in groups if 1 in g["user_ids"])
    group_b = next(g for g in groups if 9 in g["user_ids"])

    assert group_a["user_ids"] == list(range(1, 9)), "Los perfiles {1,2,3} deben estar juntos."
    assert group_b["user_ids"] == list(range(9, 17)), "Los perfiles {1,4,5} deben estar juntos."


def test_assign_monitors_only_if_qualified():
    """Se asigna monitor solo en el tema que tiene a alguien calificado."""
    groups = [
        {"topic_id": 1, "user_ids": [1, 2, 3], "slot": "LUN 19:00"},
        {"topic_id": 2, "user_ids": [4, 5, 6], "slot": "MIE 19:00"},
    ]
    qualified = {1: [99]}  # Solo el tema 1 tiene monitor calificado.

    result = assign_monitors(groups, qualified)
    assert result[0]["monitor_id"] == 99
    assert result[1]["monitor_id"] is None, "Sin calificados, la reunión queda sin monitor."


def test_assign_monitors_excludes_participant_and_picks_smallest():
    """El monitor no puede ser participante y se elige el de menor id."""
    groups = [{"topic_id": 1, "user_ids": [1, 2, 3], "slot": None}]
    qualified = {1: [2, 10, 5]}  # 2 es participante; de los válidos, el menor es 5.
    result = assign_monitors(groups, qualified)
    assert result[0]["monitor_id"] == 5


def test_slot_pick_prefers_most_common():
    """El horario de la célula es el más repetido entre sus miembros."""
    users = [_user(1, [1]), _user(2, [1]), _user(3, [1])]
    availability = {
        1: ["LUN 19:00", "MIE 19:00"],
        2: ["LUN 19:00"],
        3: ["VIE 18:00"],
    }
    groups = plan_meetings(users, availability, max_size=8)
    assert groups[0]["slot"] == "LUN 19:00"

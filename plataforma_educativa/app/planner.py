# -*- coding: utf-8 -*-
"""Algoritmo de planificación de reuniones.

Ese es el corazón de la Plataforma Educativa: dado un conjunto de usuarios con
disponibilidad y con temas "débiles" (en ``not_seen`` o ``learning``), armar
grupos de reunión. Cada reunión es una célula de aprendizaje:

* Máximo ``max_size`` (8) estudiantes.
* Se agrupa primero por el **tema más débil** de cada persona.
* Cuando hay muchos usuarios con el mismo tema débil, se **reparte por
  similitud de perfiles**: se juntan las personas cuyo *resto* de debilidades se
  parece más. Luego un rebalanceo garantiza que ninguna célula quede con menos
  de ``min_size`` (3) si es posible, sin superar ``max_size``.

``plan_meetings`` es una función pura: no toca la base de datos. Eso permite
probarla aislada y hace el algoritmo transparente.
"""

from collections import defaultdict

DEFAULT_MAX_SIZE = 8
DEFAULT_MIN_SIZE = 3


def plan_meetings(users, availability, max_size=DEFAULT_MAX_SIZE, min_size=None):
    """Agrupa usuarios en reuniones según el tema que deben reforzar.

    Args:
        users: lista de dicts ``{"user_id": int, "weak_topics": [int, ...]}``
            donde ``weak_topics`` ya está **ordenada de más débil a menos débil**
            (el primer elemento es el tema más urgente).
        availability: dict ``{user_id: [slot_str, ...]}`` con la disponibilidad
            semanal de cada usuario (para elegir el horario de la reunión).
        max_size: tamaño máximo de reunión (por defecto 8).
        min_size: tamaño mínimo deseado (por defecto 3).

    Returns:
        Lista de dicts ``{"topic_id", "user_ids", "slot"}``. ``slot`` es el
        horario más común del grupo o ``None`` si ninguno tiene disponibilidad.
    """
    if min_size is None:
        min_size = DEFAULT_MIN_SIZE
    groups = _group_by_weakness(users, max_size, min_size)
    result = []
    for group in groups:
        user_ids = [user["user_id"] for user in group["members"]]
        result.append(
            {
                "topic_id": group["topic_id"],
                "user_ids": user_ids,
                "slot": _pick_slot(user_ids, availability),
            }
        )
    return result


def assign_monitors(groups, qualified_monitors):
    """Asigna un monitor a cada reunión si hay alguien calificado y disponible.

    Args:
        groups: lista de dicts devuelta por :func:`plan_meetings`.
        qualified_monitors: dict ``{topic_id: [user_id, ...]}`` con los usuarios
            calificados para **enseñar** ese tema (en la plataforma: tema
            ``mastered`` y ``mentor_rounds >= 1``, además de disponibilidad).

    Returns:
        La misma lista de grupos, pero cada uno con ``monitor_id`` (``None`` si
        no hay nadie calificado). Se elige al monitor con menor ``user_id`` para
        que la asignación sea determinista.
    """
    result = []
    for group in groups:
        topic_id = group["topic_id"]
        participant_ids = set(group["user_ids"])
        candidates = [
            uid for uid in qualified_monitors.get(topic_id, []) if uid not in participant_ids
        ]
        monitor_id = min(candidates) if candidates else None
        result.append({**group, "monitor_id": monitor_id})
    return result


# --------------------------------------------------------------------------
# Implementación interna
# --------------------------------------------------------------------------


def _group_by_weakness(users, max_size, min_size):
    """Primero agrupa por tema más débil, luego subdivide por similitud."""
    by_topic = defaultdict(list)
    for user in users:
        weak = user.get("weak_topics") or []
        if not weak:
            continue  # El usuario no tiene nada que reforzar.
        by_topic[weak[0]].append(user)

    groups = []
    for topic_id in sorted(by_topic):
        members = by_topic[topic_id]
        for cluster in _cluster_members(members, topic_id, max_size, min_size):
            groups.append({"topic_id": topic_id, "members": cluster})

    # Orden final determinista para que el resultado sea reproducible.
    groups.sort(key=lambda g: (g["topic_id"], [u["user_id"] for u in g["members"]]))
    return groups


def _profile(user, primary_topic):
    """Perfil de debilidades de un usuario, sin contar el tema principal.

    Es la base de la "cercanía de perfiles": se comparan qué *otras* cosas
    debe reforzar cada persona, para juntar a las que más se parecen.
    """
    return set(user.get("weak_topics") or []) - {primary_topic}


def _cluster_members(members, primary_topic, max_size, min_size):
    """Divide los miembros de un mismo tema débil en células de tamaño acotado.

    Estrategia (determinista, sin aleatoriedad):

    1. Se ordenan los usuarios por su perfil (las debilidades que comparten).
    2. Se toma el primero como semilla de una célula y se van sumando los
       usuarios **más parecidos** a la célula hasta llenarla (``max_size``).
       Así las personas con perfiles afines quedan juntas.
    3. Al final, un rebalanceo mueve a un puñado de usuarios desde las células
       más grandes a las más pequeñas para que ninguna quede por debajo de
       ``min_size`` cuando es posible, sin romper ``max_size``.
    """
    ordered = sorted(
        members,
        key=lambda u: (tuple(sorted(_profile(u, primary_topic))), u["user_id"]),
    )
    clusters = []
    remaining = list(ordered)
    while remaining:
        seed = remaining.pop(0)
        cluster = [seed]
        while len(cluster) < max_size and remaining:
            best_index = _most_similar_index(remaining, cluster, primary_topic)
            cluster.append(remaining.pop(best_index))
        clusters.append(cluster)

    return _rebalance(clusters, min_size, max_size, primary_topic)


def _most_similar_index(candidates, cluster, primary_topic):
    """Devuelve el índice del candidato más parecido al perfil de la célula."""
    cluster_profile = set()
    for member in cluster:
        cluster_profile |= _profile(member, primary_topic)
    best_index = 0
    best_score = -1
    for i, candidate in enumerate(candidates):
        profile = _profile(candidate, primary_topic)
        score = len(cluster_profile & profile)
        if score > best_score:
            best_score = score
            best_index = i
    return best_index


def _rebalance(clusters, min_size, max_size, primary_topic):
    """Intenta llevar todas las células a al menos ``min_size`` sin pasar de ``max_size``."""
    for _ in range(len(clusters) * max_size):
        low = None
        high = None
        # Célula más pequeña (por debajo del mínimo).
        for i, cluster in enumerate(clusters):
            if len(cluster) < min_size and (low is None or len(cluster) < len(clusters[low])):
                low = i
        if low is None:
            break
        # Célula más grande con margen para donar un miembro.
        for i, cluster in enumerate(clusters):
            if i != low and len(cluster) > min_size and (high is None or len(cluster) > len(clusters[high])):
                high = i
        if high is None:
            break  # No se puede rebalancear más.
        # Mover al miembro de la célula grande más parecido a la pequeña.
        low_profile = set()
        for member in clusters[low]:
            low_profile |= _profile(member, primary_topic)
        source = clusters[high]
        donor_index = 0
        best_score = -1
        for i, member in enumerate(source):
            score = len(low_profile & _profile(member, primary_topic))
            if score > best_score:
                best_score = score
                donor_index = i
        clusters[low].append(source.pop(donor_index))
    return clusters


def _pick_slot(user_ids, availability):
    """Elige el horario más común del grupo (desempate lexicográfico)."""
    counter = defaultdict(int)
    for uid in user_ids:
        for slot in availability.get(uid, []):
            counter[slot] += 1
    if not counter:
        return None
    best = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return best

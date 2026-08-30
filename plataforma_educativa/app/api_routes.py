# -*- coding: utf-8 -*-
"""API REST de la Plataforma Educativa.

Endpoints autenticados por token (cabecera ``X-Auth-Token``). Devuelven JSON.
"""

import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from datetime import date as _date

from flask import Blueprint, g, jsonify, request

from .auth import login_required
from .db import get_db
from .planner import assign_monitors, plan_meetings

api_bp = Blueprint("api", __name__)

MAX_PARTICIPANTS = 8
MIN_PARTICIPANTS = 3
TEST_PASS_THRESHOLD = 70.0
ISO_WEEK_FORMAT = "%Y-W%W"

# Días de la semana (índice 0 = lunes, como datetime.isoweekday()).
_DAY_INDEX = {"LUN": 0, "MAR": 1, "MIE": 2, "JUE": 3, "VIE": 4, "SAB": 5, "DOM": 6}


# --------------------------------------------------------------------------
# Helpers de estado y datos
# --------------------------------------------------------------------------

def _now():
    return datetime.now(timezone.utc).isoformat()


def _user_row():
    return get_db().execute("SELECT * FROM users WHERE id = ?", (g.user_id,)).fetchone()


def _is_coordinator():
    user = _user_row()
    return bool(user and user["is_coordinator"])


def _user_state(user_id, topic_id):
    """Estado del usuario sobre un tema, con valores por defecto."""
    row = get_db().execute(
        "SELECT * FROM user_topics WHERE user_id = ? AND topic_id = ?",
        (user_id, topic_id),
    ).fetchone()
    if row is None:
        return {
            "estado": "not_seen",
            "score": None,
            "mentor_rounds": 0,
            "mentorship_approved": False,
            "evidence": None,
            "ready_to_teach": False,
        }
    evidence = None
    if row["evidence"]:
        try:
            evidence = json.loads(row["evidence"])
        except (ValueError, TypeError):
            evidence = {"tipo": "texto", "titulo": "material (sin metadatos legibles)"}
    # Regla de oro sin muros (M13): aprobado + material propio + mentoría >= 1
    # es maestría; aprobado + material (sin alumnos aún) es 'listo para enseñar'.
    ready_to_teach = row["estado"] == "test_passed" and bool(evidence)
    return {
        "estado": row["estado"],
        "score": row["score"],
        "mentor_rounds": row["mentor_rounds"],
        "mentorship_approved": bool(row["mentorship_approved"]),
        "evidence": evidence,
        "ready_to_teach": ready_to_teach,
    }


def _report_mastery_to_maxocracia(user_id, topic_id, score, mentor_rounds):
    """Reporta una maestría verificada al puente (:5001) — sincronización
    automática del OEV (M12). Best-effort: el nodo autónomo jamás se rompe
    porque el puente esté caído o no esté federado; sin configuración no
    reporta (el nodo autónomo sigue siendo autónomo)."""
    url = os.environ.get("EDU_BRIDGE_URL")
    secret = os.environ.get("EDU_BRIDGE_SERVICE_TOKEN")
    if not url or not secret:
        return False
    db = get_db()
    maxo = db.execute("SELECT maxo_user_id FROM users WHERE id = ?", (user_id,)).fetchone()
    if maxo is None or not maxo["maxo_user_id"]:
        return False  # nodo autónomo: sin identidad federada, nada que sincronizar
    topic = db.execute("SELECT slug, branch_id FROM topics WHERE id = ?", (topic_id,)).fetchone()
    if topic is None:
        return False
    branch = db.execute("SELECT slug FROM branches WHERE id = ?", (topic["branch_id"],)).fetchone()
    if branch is None:
        return False
    payload = {
        "user_id": int(maxo["maxo_user_id"]),
        "topic_slug": topic["slug"],
        "branch_slug": branch["slug"],
        "score": score,
        "mentor_rounds": mentor_rounds or 0,
        "triada_approved": True,
    }
    try:
        req = urllib.request.Request(
            url.rstrip("/") + "/edu-bridge/sync-mastery",
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Edu-Bridge-Token": secret,
            },
            data=json.dumps(payload).encode("utf-8"),
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 201
    except Exception:
        return False


def _upsert_user_state(user_id, topic_id, estado=None, score=None, mentor_rounds=None,
                       mentorship_approved=None, evidence=None):
    """Inserta o actualiza la fila de progreso user_topics."""
    db = get_db()
    current = db.execute(
        "SELECT * FROM user_topics WHERE user_id = ? AND topic_id = ?",
        (user_id, topic_id),
    ).fetchone()
    new_evidence = evidence if evidence is not None else (current["evidence"] if current else None)
    transitioned_to_mastered = False
    if current is None:
        db.execute(
            "INSERT INTO user_topics (user_id, topic_id, estado, score, updated_at, "
            "mentor_rounds, mentorship_approved, evidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                user_id,
                topic_id,
                estado or "not_seen",
                score,
                _now(),
                mentor_rounds if mentor_rounds is not None else 0,
                1 if mentorship_approved else 0,
                new_evidence,
            ),
        )
        transitioned_to_mastered = estado == "mastered"
        final_score = score
        final_mr = mentor_rounds if mentor_rounds is not None else 0
    else:
        new_estado = estado if estado is not None else current["estado"]
        new_score = score if score is not None else current["score"]
        new_mr = mentor_rounds if mentor_rounds is not None else current["mentor_rounds"]
        new_ma = (
            int(bool(mentorship_approved))
            if mentorship_approved is not None
            else current["mentorship_approved"]
        )
        # Regla de oro sin muros (M13): aprobado + material propio + primera
        # mentoría = maestría (la vacuación completa, aunque no haya aula llena).
        if new_estado == "test_passed" and new_mr >= 1 and new_evidence:
            new_estado = "mastered"
        db.execute(
            "UPDATE user_topics SET estado = ?, score = ?, updated_at = ?, "
            "mentor_rounds = ?, mentorship_approved = ?, evidence = ? "
            "WHERE user_id = ? AND topic_id = ?",
            (new_estado, new_score, _now(), new_mr, new_ma, new_evidence, user_id, topic_id),
        )
        transitioned_to_mastered = new_estado == "mastered" and current["estado"] != "mastered"
        final_score = new_score
        final_mr = new_mr
    db.commit()

    # La validación es la transferencia: al vacuar (mastered), el nodo reporta
    # al Perfil Vital con su token de servicio (M12, best-effort).
    if transitioned_to_mastered:
        _report_mastery_to_maxocracia(user_id, topic_id, final_score, final_mr)


def _topic_questions(topic_id):
    """Devuelve las preguntas de un tema como dicts (opciones ya separadas)."""
    rows = get_db().execute(
        "SELECT * FROM questions WHERE topic_id = ? ORDER BY id", (topic_id,)
    ).fetchall()
    return [
        {
            "id": row["id"],
            "pregunta": row["pregunta"],
            "opciones": json.loads(row["opciones"]),
            "correcta": row["correcta"],
            "explicacion": row["explicacion"],
        }
        for row in rows
    ]


def _get_topic_or_404(topic_id):
    row = get_db().execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
    if row is None:
        return None
    return dict(row)


def _prereqs_ok(user_id, prereq_ids):
    """True si todos los prerrequisitos de la lista están aprobados."""
    for pid in prereq_ids:
        st = _user_state(user_id, pid)
        if st["estado"] not in ("test_passed", "mastered"):
            return False
    return True


def suggest_next_topic(user_id):
    """El compañero de la ciudad: el siguiente lote a construir (M14).

    Prioridad: el barrio (rama) donde la persona ya construye más, con lotes
    desbloqueados y libres; dentro, primero lo más sencillo. Cero presión:
    es una sugerencia de la mano, nunca un mandato; sin ranking ni tiempo.
    Devuelve dict (sugerencia) o None si la ciudad está completa por hoy.
    """
    db = get_db()
    rows = db.execute(
        "SELECT t.id, t.slug, t.titulo, t.dificultad, t.orden, t.prereq_ids, t.branch_id, "
        "b.slug AS branch_slug, b.nombre AS branch_nombre, b.descripcion AS branch_descripcion "
        "FROM topics t JOIN branches b ON b.id = t.branch_id ORDER BY t.orden ASC, t.id ASC"
    ).fetchall()

    candidatos = []
    for row in rows:
        prereq_ids = json.loads(row["prereq_ids"] or "[]")
        if not _prereqs_ok(user_id, prereq_ids):
            continue
        st = _user_state(user_id, row["id"])
        # Solo lotes sin empezar: la obra en curso NO se repite (el compañero
        # no insiste en lo que ya está construyendo — cero presión psicológica).
        if st["estado"] == "not_seen":
            candidatos.append((dict(row), st["estado"]))

    if not candidatos:
        return None

    # Progreso por rama: lote iluminado = aprobados/mastered sobre el total.
    by_branch = {}
    for row in rows:
        by_branch.setdefault(row["branch_id"], {"total": 0, "hechos": 0})
        by_branch[row["branch_id"]]["total"] += 1
        st = _user_state(user_id, row["id"])
        if st["estado"] in ("test_passed", "mastered"):
            by_branch[row["branch_id"]]["hechos"] += 1

    def score(cand):
        b = by_branch[cand[0]["branch_id"]]
        progreso = (b["hechos"] / b["total"]) if b["total"] else 0.0
        return (progreso, -cand[0]["dificultad"])

    mejor = max(candidatos, key=score)
    tema = mejor[0]
    return {
        "topic_id": tema["id"],
        "slug": tema["slug"],
        "titulo": tema["titulo"],
        "dificultad": tema["dificultad"],
        "branch_slug": tema["branch_slug"],
        "branch_nombre": tema["branch_nombre"],
        "branch_descripcion": tema["branch_descripcion"],
        "estado": mejor[1],
    }


@api_bp.route("/api/suggest", methods=["GET"])
@login_required
def api_suggest():
    """El compañero de la ciudad sugiere el siguiente lote (M14, guía de la mano)."""
    return jsonify({"suggestion": suggest_next_topic(g.user_id)}), 200


# --------------------------------------------------------------------------
# Helpers de semana (formato ISO "YYYY-Www")
# --------------------------------------------------------------------------

def _iso_week_key(d):
    return f"{d.isocalendar()[0]}-W{d.isocalendar()[1]:02d}"


def _current_week():
    return _iso_week_key(datetime.now())


def _parse_week(week_key):
    """Devuelve (año ISO, número de semana) desde "YYYY-Www"."""
    year_part, week_part = week_key.split("-W")
    return int(year_part), int(week_part)


def _monday_of_week(year, week):
    return _date.fromisocalendar(year, week, 1)


def _meeting_date_from_slot(week_key, slot):
    """Convierte "LUN 19:00" en (fecha ISO, hora). Si el slot es None, lunes 19:00."""
    year, week = _parse_week(week_key)
    monday = _monday_of_week(year, week)
    if not slot:
        return monday.isoformat(), "19:00"
    parts = slot.split()
    day_index = _DAY_INDEX.get(parts[0].upper(), 0)
    hora = parts[1] if len(parts) > 1 else "19:00"
    fecha = monday + timedelta(days=day_index)
    return fecha.isoformat(), hora


# --------------------------------------------------------------------------
# Perfil y árbol
# --------------------------------------------------------------------------

@api_bp.route("/api/me", methods=["GET"])
@login_required
def me():
    """Perfil del usuario más su progreso por rama."""
    user = _user_row()
    db = get_db()
    branches = db.execute("SELECT * FROM branches ORDER BY orden").fetchall()

    progress = []
    for branch in branches:
        topics = db.execute(
            "SELECT id FROM topics WHERE branch_id = ?", (branch["id"],)
        ).fetchall()
        total = len(topics)
        passed = 0
        mastered = 0
        for topic in topics:
            st = _user_state(g.user_id, topic["id"])
            if st["estado"] in ("test_passed", "mastered"):
                passed += 1
            if st["estado"] == "mastered":
                mastered += 1
        progress.append(
            {
                "slug": branch["slug"],
                "nombre": branch["nombre"],
                "topics_total": total,
                "topics_passed": passed,
                "topics_mastered": mastered,
                "progress_pct": round(100 * passed / total) if total else 0,
            }
        )

    return (
        jsonify(
            {
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "is_coordinator": bool(user["is_coordinator"]),
                    "maxo_user_id": user["maxo_user_id"] if "maxo_user_id" in user.keys() else None,
                    "is_federated": getattr(g, "is_federated", False),
                },
                "branches": progress,
            }
        ),
        200,
    )



def _triada_state(user_id, topic_id):
    """Estado de la triada de mentoría de un par (usuario, tema), o None.

    La triada es la capa de opinión de la validación (mentor + par + oráculo
    con veto); la regla es: mentor y par aprueban y el oráculo no veta.
    """
    db = get_db()
    row = db.execute(
        "SELECT * FROM mentorship_triadas WHERE user_id = ? AND topic_id = ?",
        (user_id, topic_id),
    ).fetchone()
    if row is None:
        return None
    return {
        "outcome": row["outcome"],
        "mentor_ok": bool(row["mentor_ok"]),
        "peer_ok": bool(row["peer_ok"]),
        "oracle_veto": bool(row["oracle_veto"]),
        "created_at": row["created_at"],
    }


@api_bp.route("/api/tree", methods=["GET"])
@login_required
def tree():
    """Árbol completo con el estado del usuario en cada tema."""
    db = get_db()
    branches = db.execute("SELECT * FROM branches ORDER BY orden").fetchall()
    result = []
    for branch in branches:
        topics = db.execute(
            "SELECT * FROM topics WHERE branch_id = ? ORDER BY orden", (branch["id"],)
        ).fetchall()
        topic_list = []
        for topic in topics:
            prereq_ids = json.loads(topic["prereq_ids"] or "[]")
            st = _user_state(g.user_id, topic["id"])
            q_count = db.execute(
                "SELECT COUNT(*) AS n FROM questions WHERE topic_id = ?", (topic["id"],)
            ).fetchone()["n"]
            topic_list.append(
                {
                    "id": topic["id"],
                    "slug": topic["slug"],
                    "titulo": topic["titulo"],
                    "descripcion": topic["descripcion"],
                    "dificultad": topic["dificultad"],
                    "prereq_ids": prereq_ids,
                    "questions": q_count,
                    "estado": st["estado"],
                    "score": st["score"],
                    "mentor_rounds": st["mentor_rounds"],
                    "mentorship_approved": st["mentorship_approved"],
                    "evidence": st["evidence"],
                    "ready_to_teach": st["ready_to_teach"],
                    "triada": _triada_state(g.user_id, topic["id"]),
                    "unlocked": _prereqs_ok(g.user_id, prereq_ids),
                }
            )
        result.append(
            {
                "id": branch["id"],
                "slug": branch["slug"],
                "nombre": branch["nombre"],
                "descripcion": branch["descripcion"],
                "topics": topic_list,
            }
        )
    return jsonify({"branches": result}), 200


# --------------------------------------------------------------------------
# Progreso de temas
# --------------------------------------------------------------------------

@api_bp.route("/api/topics/<int:topic_id>", methods=["GET"])
@login_required
def topic_detail(topic_id):
    """Detalle de un tema con sus preguntas (sin revelar la respuesta correcta).

    Permite que el frontend muestre el test sin que el servidor filtre la clave.
    """
    topic = _get_topic_or_404(topic_id)
    if topic is None:
        return jsonify({"error": "El tema no existe."}), 404
    questions = _topic_questions(topic_id)
    return (
        jsonify(
            {
                "id": topic["id"],
                "slug": topic["slug"],
                "titulo": topic["titulo"],
                "descripcion": topic["descripcion"],
                "dificultad": topic["dificultad"],
                "preguntas": [
                    {
                        "id": q["id"],
                        "pregunta": q["pregunta"],
                        "opciones": q["opciones"],
                        "explicacion": q["explicacion"],
                    }
                    for q in questions
                ],
            }
        ),
        200,
    )


@api_bp.route("/api/topics/<int:topic_id>/start", methods=["POST"])
@login_required
def topic_start(topic_id):
    """Marca el tema como ``learning``, validando que los prerrequisitos estén aprobados."""
    topic = _get_topic_or_404(topic_id)
    if topic is None:
        return jsonify({"error": "El tema no existe."}), 404

    prereq_ids = json.loads(topic.get("prereq_ids") or "[]")
    if not _prereqs_ok(g.user_id, prereq_ids):
        return (
            jsonify({"error": "Debes aprobar los prerrequisitos antes de empezar este tema."}),
            403,
        )

    st = _user_state(g.user_id, topic_id)
    if st["estado"] == "not_seen":
        _upsert_user_state(g.user_id, topic_id, estado="learning", score=0)

    return jsonify({"topic_id": topic_id, "estado": _user_state(g.user_id, topic_id)}), 200


@api_bp.route("/api/topics/<int:topic_id>/test", methods=["POST"])
@login_required
def topic_test(topic_id):
    """Califica un intento de test. >=70% aprueba el tema.

    El estado ``mastered`` se alcanza al aprobar el test Y haber participado
    como monitor de al menos 1 reunión (``mentor_rounds >= 1``).
    """
    topic = _get_topic_or_404(topic_id)
    if topic is None:
        return jsonify({"error": "El tema no existe."}), 404

    data = request.get_json(silent=True) or {}
    answers = data.get("answers") or []
    prereq_ids = json.loads(topic["prereq_ids"] or "[]")
    if not _prereqs_ok(g.user_id, prereq_ids):
        return (
            jsonify(
                {
                    "error": "Este tema tiene prerrequisitos: primero aprueba lo anterior (el árbol se camina, no se salta).",
                    "blocked_by": prereq_ids,
                }
            ),
            403,
        )
    questions = _topic_questions(topic_id)
    if not questions:
        return jsonify({"error": "El tema no tiene preguntas."}), 400

    total = len(questions)
    correct = 0
    for i, question in enumerate(questions):
        if i < len(answers) and answers[i] == question["correcta"]:
            correct += 1
    score = round(100 * correct / total)

    st = _user_state(g.user_id, topic_id)
    best_score = max(score, st["score"] or 0)

    if score >= TEST_PASS_THRESHOLD:
        new_estado = "mastered" if (st["mentor_rounds"] >= 1 and st["evidence"]) else "test_passed"
    else:
        # Si ya estaba aprobado, no se degrada con un intento peor.
        new_estado = "test_passed" if st["estado"] in ("test_passed", "mastered") else "learning"

    _upsert_user_state(g.user_id, topic_id, estado=new_estado, score=best_score)
    return (
        jsonify(
            {
                "topic_id": topic_id,
                "correct": correct,
                "total": total,
                "score": score,
                "passed": score >= TEST_PASS_THRESHOLD,
                "estado": _user_state(g.user_id, topic_id),
            }
        ),
        200,
    )


@api_bp.route("/api/topics/<int:topic_id>/evidence", methods=["POST"])
@login_required
def topic_evidence(topic_id):
    """Aporta material de enseñanza propio (M13): texto, audio, video o imagen.

    La vacuación sin muros: aunque no haya alumnos todavía, quien aprobó puede
    dejar su material didáctico (la obra de la regla de oro). Con material +
    primera ronda de mentoría, la maestría se cierra sola.
    """
    topic = _get_topic_or_404(topic_id)
    if topic is None:
        return jsonify({"error": "El tema no existe."}), 404

    st = _user_state(g.user_id, topic_id)
    if st["estado"] not in ("test_passed", "mastered"):
        return (
            jsonify(
                {
                    "error": "Primero aprueba el tema: el material de enseñanza se aporta sobre lo que ya sabes (mínimo 70%).",
                    "estado": st["estado"],
                }
            ),
            400,
        )

    data = request.get_json(silent=True) or {}
    tipo = (data.get("tipo") or "").strip()
    titulo = (data.get("titulo") or "").strip()
    url = (data.get("url") or "").strip()
    texto = (data.get("texto") or "").strip()
    if tipo not in ("texto", "audio", "video", "imagen"):
        return jsonify({"error": "tipo debe ser: texto, audio, video o imagen."}), 400
    if not titulo:
        return jsonify({"error": "dales un título a tu material."}), 400
    if tipo == "texto" and not texto:
        return jsonify({"error": "para texto, escribe el contenido."}), 400
    if tipo != "texto" and not url:
        return jsonify({"error": f"para {tipo}, pega la dirección (URL) del archivo."}), 400

    evidence = json.dumps(
        {"tipo": tipo, "titulo": titulo[:200], "url": url[:1000], "texto": texto[:8000]},
        ensure_ascii=False,
    )
    # La regla de oro: si ya tenía mentoría (sin material), ahora se cierra.
    _upsert_user_state(g.user_id, topic_id, evidence=evidence, mentor_rounds=st["mentor_rounds"])
    return jsonify({"success": True, "evidence": {"tipo": tipo, "titulo": titulo}}), 201


@api_bp.route("/api/topics/<int:topic_id>/request-mentorship", methods=["POST"])
@login_required
def topic_request_mentorship(topic_id):
    """Solicita mentoría. En el MVP queda marcada como ``pendiente``.

    En producción la valida la triada (mentor + par + oráculo con veto). Aquí
    solo registramos la intención y devolvemos un mensaje explicativo.
    """
    topic = _get_topic_or_404(topic_id)
    if topic is None:
        return jsonify({"error": "El tema no existe."}), 404
    _upsert_user_state(g.user_id, topic_id, mentorship_approved=True)
    return (
        jsonify(
            {
                "message": "Solicitud de mentoría registrada (pendiente). "
                "En producción la valida la triada: mentor + par + oráculo con veto.",
                "mentorship_approved": True,
            }
        ),
        200,
    )


@api_bp.route("/api/topics/<int:topic_id>/mentorship/verify", methods=["POST"])
@login_required
def topic_mentorship_verify(topic_id):
    """Verifica la triada de mentoría (mentor + par + oráculo con veto).

    Solo el coordinador puede verificar. Resultado por la regla de la
    validación en tres capas:
      - ``validated`` si mentor y par aprueban y el oráculo no veta;
      - ``vetoed`` si el oráculo ejerce el veto (axiomas en riesgo);
      - ``pending`` si falta algún aval.
    """
    topic = _get_topic_or_404(topic_id)
    if topic is None:
        return jsonify({"error": "El tema no existe."}), 404
    if not _is_coordinator():
        return jsonify({"error": "Solo el coordinador verifica la triada."}), 403

    data = request.get_json(silent=True) or {}
    mentor_ok = bool(data.get("mentor_ok", False))
    peer_ok = bool(data.get("peer_ok", False))
    oracle_veto = bool(data.get("oracle_veto", False))
    target_user = data.get("user_id")
    if not isinstance(target_user, int):
        return jsonify({"error": "user_id (el aprendiz) es requerido."}), 400

    if oracle_veto:
        outcome = "vetoed"
    elif mentor_ok and peer_ok:
        outcome = "validated"
    else:
        outcome = "pending"

    db = get_db()
    existing = db.execute(
        "SELECT id FROM mentorship_triadas WHERE user_id = ? AND topic_id = ?",
        (target_user, topic_id),
    ).fetchone()
    if existing:
        db.execute(
            "UPDATE mentorship_triadas SET mentor_ok = ?, peer_ok = ?, oracle_veto = ?, outcome = ? "
            "WHERE id = ?",
            (int(mentor_ok), int(peer_ok), int(oracle_veto), outcome, existing["id"]),
        )
    else:
        db.execute(
            "INSERT INTO mentorship_triadas (user_id, topic_id, mentor_ok, peer_ok, oracle_veto, outcome, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (target_user, topic_id, int(mentor_ok), int(peer_ok), int(oracle_veto), outcome, _now()),
        )
    db.commit()
    return jsonify({"success": True, "triada": _triada_state(target_user, topic_id)}), 200


# --------------------------------------------------------------------------
# Disponibilidad
# --------------------------------------------------------------------------

@api_bp.route("/api/availability", methods=["POST"])
@login_required
def availability_post():
    """Registra/actualiza la disponibilidad del usuario para una semana."""
    data = request.get_json(silent=True) or {}
    week = (data.get("week") or "").strip()
    slots = data.get("slots") or []
    if not week or not isinstance(slots, list):
        return jsonify({"error": "week y slots son obligatorios."}), 400

    db = get_db()
    db.execute(
        "INSERT INTO availability (user_id, semana, slots) VALUES (?, ?, ?) "
        "ON CONFLICT(user_id, semana) DO UPDATE SET slots = excluded.slots",
        (g.user_id, week, json.dumps(slots, ensure_ascii=False)),
    )
    db.commit()
    return jsonify({"week": week, "slots": slots}), 200


@api_bp.route("/api/availability", methods=["GET"])
@login_required
def availability_get():
    """Devuelve la disponibilidad registrada del usuario actual."""
    rows = get_db().execute(
        "SELECT semana, slots FROM availability WHERE user_id = ? ORDER BY semana",
        (g.user_id,),
    ).fetchall()
    result = [
        {"week": row["semana"], "slots": json.loads(row["slots"])}
        for row in rows
    ]
    return jsonify({"availability": result}), 200


# --------------------------------------------------------------------------
# Reuniones
# --------------------------------------------------------------------------

def _weak_topics_for_user(user_id):
    """Temas 'a reforzar' del usuario, ordenados por score ascendente.

    ``not_seen`` cuenta como el más débil (score -1), para que aparezca primero.
    """
    rows = get_db().execute(
        "SELECT topic_id, estado, score FROM user_topics "
        "WHERE user_id = ? AND estado IN ('not_seen', 'learning')",
        (user_id,),
    ).fetchall()
    ordered = sorted(rows, key=lambda r: (r["score"] if r["score"] is not None else -1, r["topic_id"]))
    return [r["topic_id"] for r in ordered]


def _qualified_monitors(week):
    """Usuarios calificados para enseñar cada tema: maestros y maestros en espera
    (aprobado + material propio) con disponibilidad — la cola de tutores (M13)."""
    rows = get_db().execute(
        "SELECT ut.user_id, ut.topic_id FROM user_topics ut "
        "JOIN availability a ON a.user_id = ut.user_id AND a.semana = ? "
        "WHERE (ut.estado = 'mastered' AND ut.mentor_rounds >= 1) "
        "   OR (ut.estado = 'test_passed' AND ut.evidence IS NOT NULL AND ut.evidence != '')",
        (week,),
    ).fetchall()
    by_topic = {}
    for row in rows:
        by_topic.setdefault(row["topic_id"], []).append(row["user_id"])
    return by_topic


@api_bp.route("/api/meetings/generate", methods=["POST"])
@login_required
def meetings_generate():
    """Genera las reuniones de una semana usando :func:`plan_meetings`.

    Solo el coordinador puede generar. Devuelve las reuniones creadas.
    """
    if not _is_coordinator():
        return jsonify({"error": "Solo el coordinador puede generar la semana."}), 403

    week = request.args.get("week") or _current_week()
    db = get_db()

    # Usuarios con disponibilidad esa semana.
    avail_rows = db.execute(
        "SELECT user_id, slots FROM availability WHERE semana = ?", (week,)
    ).fetchall()
    availability = {
        row["user_id"]: json.loads(row["slots"]) for row in avail_rows
    }

    # Perfil de debilidades de cada usuario disponible.
    users = []
    for user_id in availability:
        weak = _weak_topics_for_user(user_id)
        if weak:
            users.append({"user_id": user_id, "weak_topics": weak})

    groups = plan_meetings(users, availability, max_size=MAX_PARTICIPANTS)
    groups = assign_monitors(groups, _qualified_monitors(week))

    created = []
    for group in groups:
        fecha, hora = _meeting_date_from_slot(week, group["slot"])
        monitor_id = group["monitor_id"]
        estado = "full" if len(group["user_ids"]) >= MAX_PARTICIPANTS else "open"

        cur = db.execute(
            "INSERT INTO meetings (fecha, hora_inicio, duracion_min, topic_id, monitor_id, "
            "estado, week, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (fecha, hora, 120, group["topic_id"], monitor_id, estado, week, _now()),
        )
        meeting_id = cur.lastrowid

        for user_id in group["user_ids"]:
            db.execute(
                "INSERT INTO meeting_participants (meeting_id, user_id, asistio) "
                "VALUES (?, ?, NULL)",
                (meeting_id, user_id),
            )

        # Recompensa de la vacuación: el monitor suma una ronda más de mentoría.
        if monitor_id is not None:
            st = _user_state(monitor_id, group["topic_id"])
            _upsert_user_state(
                monitor_id, group["topic_id"],
                mentor_rounds=st["mentor_rounds"] + 1,
            )
        db.commit()

        created.append(
            {
                "id": meeting_id,
                "week": week,
                "fecha": fecha,
                "hora_inicio": hora,
                "duracion_min": 120,
                "topic_id": group["topic_id"],
                "monitor_id": monitor_id,
                "estado": estado,
                "participants": group["user_ids"],
            }
        )

    return jsonify({"week": week, "meetings": created}), 201


@api_bp.route("/api/meetings", methods=["GET"])
@login_required
def meetings_list():
    """Lista las reuniones de una semana (por defecto la actual)."""
    week = request.args.get("week") or _current_week()
    db = get_db()
    rows = db.execute(
        "SELECT m.*, t.titulo, t.slug AS topic_slug, b.nombre AS branch_nombre, "
        "b.slug AS branch_slug, mu.username AS monitor_username "
        "FROM meetings m "
        "JOIN topics t ON t.id = m.topic_id "
        "JOIN branches b ON b.id = t.branch_id "
        "LEFT JOIN users mu ON mu.id = m.monitor_id "
        "WHERE m.week = ? ORDER BY m.id",
        (week,),
    ).fetchall()

    result = []
    for row in rows:
        participants = db.execute(
            "SELECT mp.user_id, u.username, mp.asistio "
            "FROM meeting_participants mp JOIN users u ON u.id = mp.user_id "
            "WHERE mp.meeting_id = ? ORDER BY mp.user_id",
            (row["id"],),
        ).fetchall()
        result.append(
            {
                "id": row["id"],
                "week": row["week"],
                "fecha": row["fecha"],
                "hora_inicio": row["hora_inicio"],
                "duracion_min": row["duracion_min"],
                "topic_id": row["topic_id"],
                "topic_titulo": row["titulo"],
                "topic_slug": row["topic_slug"],
                "branch": row["branch_slug"],
                "branch_nombre": row["branch_nombre"],
                "monitor_id": row["monitor_id"],
                "monitor_username": row["monitor_username"],
                "estado": row["estado"],
                "participants": [
                    {"id": p["user_id"], "username": p["username"], "asistio": p["asistio"]}
                    for p in participants
                ],
                "participants_count": len(participants),
            }
        )
    return jsonify({"week": week, "meetings": result}), 200


@api_bp.route("/api/meetings/<int:meeting_id>/join", methods=["POST"])
@login_required
def meeting_join(meeting_id):
    """Inscribe al usuario actual en una reunión.

    Si la reunión ya tiene 8 participantes, responde 409.
    """
    db = get_db()
    meeting = db.execute(
        "SELECT * FROM meetings WHERE id = ?", (meeting_id,)
    ).fetchone()
    if meeting is None:
        return jsonify({"error": "La reunión no existe."}), 404

    existing = db.execute(
        "SELECT 1 FROM meeting_participants WHERE meeting_id = ? AND user_id = ?",
        (meeting_id, g.user_id),
    ).fetchone()
    if existing:
        return jsonify({"message": "Ya estás inscrito.", "id": meeting_id}), 200

    count = db.execute(
        "SELECT COUNT(*) AS n FROM meeting_participants WHERE meeting_id = ?",
        (meeting_id,),
    ).fetchone()["n"]
    if count >= MAX_PARTICIPANTS:
        return jsonify({"error": "La reunión está llena."}), 409

    db.execute(
        "INSERT INTO meeting_participants (meeting_id, user_id, asistio) VALUES (?, ?, NULL)",
        (meeting_id, g.user_id),
    )
    # Actualizar estado de la reunión si se llega al máximo.
    new_count = count + 1
    if new_count >= MAX_PARTICIPANTS:
        db.execute("UPDATE meetings SET estado = 'full' WHERE id = ?", (meeting_id,))
    db.commit()
    return jsonify({"message": "Inscrito.", "id": meeting_id, "participants": new_count}), 200


@api_bp.route("/api/meetings/<int:meeting_id>/attend", methods=["POST"])
@login_required
def meeting_attend(meeting_id):
    """El monitor (o el coordinador) marca asistencias de la reunión.

    Cuerpo opcional con ``user_id`` y ``asistio``; si no se indica ``user_id``,
    marca a todos los participantes con el valor de ``asistio`` (por defecto
    se asume asistencia = true). Al completar la sesión, la reunión pasa a
    ``done``.
    """
    db = get_db()
    meeting = db.execute(
        "SELECT * FROM meetings WHERE id = ?", (meeting_id,)
    ).fetchone()
    if meeting is None:
        return jsonify({"error": "La reunión no existe."}), 404

    if not _is_coordinator() and meeting["monitor_id"] != g.user_id:
        return jsonify({"error": "Solo el monitor o el coordinador marcan asistencias."}), 403

    data = request.get_json(silent=True) or {}
    asistio = 1 if data.get("asistio", True) else 0

    if data.get("user_id") is not None:
        db.execute(
            "UPDATE meeting_participants SET asistio = ? WHERE meeting_id = ? AND user_id = ?",
            (asistio, meeting_id, data["user_id"]),
        )
    else:
        db.execute(
            "UPDATE meeting_participants SET asistio = ? WHERE meeting_id = ?",
            (asistio, meeting_id),
        )

    db.execute("UPDATE meetings SET estado = 'done' WHERE id = ?", (meeting_id,))
    db.commit()
    return jsonify({"message": "Asistencias marcadas.", "id": meeting_id, "estado": "done"}), 200


@api_bp.route("/api/meetings/monitor-queue", methods=["GET"])
@login_required
def meetings_monitor_queue():
    """Temas que necesitan monitor: reuniones abiertas sin monitor en la semana."""
    week = request.args.get("week") or _current_week()
    db = get_db()
    rows = db.execute(
        "SELECT m.topic_id, t.titulo, t.slug, b.slug AS branch_slug, b.nombre AS branch_nombre, "
        "COUNT(*) AS open_count "
        "FROM meetings m "
        "JOIN topics t ON t.id = m.topic_id "
        "JOIN branches b ON b.id = t.branch_id "
        "WHERE m.week = ? AND m.estado = 'open' AND m.monitor_id IS NULL "
        "GROUP BY m.topic_id, t.titulo, t.slug, b.slug, b.nombre "
        "ORDER BY m.topic_id",
        (week,),
    ).fetchall()

    qualified = _qualified_monitors(week)
    result = []
    for row in rows:
        result.append(
            {
                "topic_id": row["topic_id"],
                "topic": row["titulo"],
                "slug": row["slug"],
                "branch": row["branch_slug"],
                "branch_nombre": row["branch_nombre"],
                "open_meetings": row["open_count"],
                "qualified_monitors": qualified.get(row["topic_id"], []),
            }
        )
    return jsonify({"week": week, "queue": result}), 200


# --------------------------------------------------------------------------
# Monitores calificados
# --------------------------------------------------------------------------

@api_bp.route("/api/monitors", methods=["GET"])
@login_required
def monitors():
    """Usuarios calificados (tema aprobado + mentor_rounds>=1) por rama.

    ``?branch=slug`` filtra por rama.
    """
    branch_slug = request.args.get("branch")
    db = get_db()
    params = ()
    sql = (
        "SELECT ut.user_id, ut.topic_id, t.titulo, t.slug AS topic_slug, "
        "b.slug AS branch_slug, b.nombre AS branch_nombre "
        "FROM user_topics ut "
        "JOIN topics t ON t.id = ut.topic_id "
        "JOIN branches b ON b.id = t.branch_id "
        "WHERE ut.estado IN ('test_passed', 'mastered') AND ut.mentor_rounds >= 1"
    )
    if branch_slug:
        sql += " AND b.slug = ?"
        params = (branch_slug,)
    sql += " ORDER BY b.slug, ut.topic_id, ut.user_id"
    rows = db.execute(sql, params).fetchall()

    by_topic = {}
    for row in rows:
        entry = by_topic.setdefault(
            row["topic_id"],
            {
                "topic_id": row["topic_id"],
                "topic": row["titulo"],
                "slug": row["topic_slug"],
                "branch": row["branch_slug"],
                "branch_nombre": row["branch_nombre"],
                "users": [],
            },
        )
        entry["users"].append(
            {"id": row["user_id"], "username": _username(row["user_id"])}
        )

    return jsonify({"monitors": list(by_topic.values())}), 200


def _username(user_id):
    row = get_db().execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
    return row["username"] if row else None

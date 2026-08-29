"""
Talleres de Aprendizaje — la unidad de enseñanza de CUALQUIER skill.

Un taller es un grupo pequeño (5-12 personas, teoría OEV §1.7) donde un
facilitador (que ganó su nodo por vacuación) enseña un skill del árbol.
Los talleres se auto-organizan desde el Foro Abierto: no necesitan permiso.

La regla de oro (la vacuación, Educación Siamesa §3g): el skill se gana
produciendo material de enseñanza + mentoría a nuevos aprendices — la
validación es la transferencia. La concesión pasa por la TRIADA:
mentor (facilitador) + par (aprendiz) + oráculo con veto; todo verificador
es verificable (rotación + veto + disidente).

El veredicto lo calcula el motor puro (maxocontracts.skills.py); aquí solo
se persiste con su trazabilidad completa (T13), sin rankings por persona ni
cronometrajes (guardarraíles anti-gamificación).

Endpoints:
- POST /workshops                — crear un taller (el creador facilita).
- GET  /workshops                — listar (status, con cupos y fila).
- GET  /workshops/<id>           — detalle (enrolados, obras, award propio).
- POST /workshops/<id>/enroll    — inscribirse (cupos 5-12, sin ranking).
- POST /workshops/<id>/outputs   — publicar obra de salida (material | obra).
- POST /workshops/<id>/grant-skill — concesión de skill: regla de oro + triada.
- POST /workshops/<id>/close     — cerrar el taller (facilitador).
"""

import json
import logging
from typing import Any, Dict, List, Optional

from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .utils import get_db

from maxocontracts.skills import TriadaVotos, evaluar_concesion
from maxocontracts.tree import is_valid_node_id

logger = logging.getLogger(__name__)

workshops_bp = Blueprint("workshops", __name__, url_prefix="/workshops")

MIN_CAPACITY = 5
MAX_CAPACITY = 12
OUTPUT_KINDS = ("material", "obra")  # material = enseñanza abierta; obra = hecho aplicado
WORKSHOP_STATUSES = ("open", "running", "closed")
AWARD_OUTCOMES = ("awaiting_triada", "awarded", "rejected")
MAX_TITLE = 200
MAX_DESCRIPTION = 3000


def _enrollment_count(db, workshop_id: int) -> int:
    row = db.execute(
        "SELECT COUNT(*) FROM workshop_enrollments WHERE workshop_id = ?",
        (workshop_id,),
    ).fetchone()
    return int(row[0]) if row else 0


def _workshop_to_dict(db, row: Any, include_outputs: bool = False) -> Dict[str, Any]:
    enrolled = _enrollment_count(db, row["id"])
    facilitator = db.execute(
        "SELECT name FROM users WHERE id = ?", (row["facilitator_id"],)
    ).fetchone()
    base = {
        "id": row["id"],
        "title": row["title"],
        "skill_node": row["skill_node"],
        "description": row["description"],
        "status": row["status"],
        "capacity": row["capacity"],
        "enrolled_count": enrolled,
        "facilitator": {
            "user_id": row["facilitator_id"],
            "name": facilitator["name"] if facilitator else "desconocido",
        },
        "created_at": row["created_at"],
    }
    if include_outputs:
        outputs = db.execute(
            """
            SELECT wo.*, u.name FROM workshop_outputs wo
            JOIN users u ON u.id = wo.user_id
            WHERE wo.workshop_id = ?
            ORDER BY wo.created_at ASC, wo.id ASC
            """,
            (row["id"],),
        ).fetchall()
        base["outputs"] = [
            {
                "id": o["id"],
                "kind": o["kind"],
                "title": o["title"],
                "url": o["url"],
                "body": o["body"],
                "author": {"user_id": o["user_id"], "name": o["name"]},
                "created_at": o["created_at"],
            }
            for o in outputs
        ]
    return base


def init_workshops_tables(app) -> None:
    """Crea las tablas de talleres si no existen (schema idempotente)."""
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS workshops (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              title TEXT NOT NULL,
              skill_node TEXT NOT NULL,
              description TEXT,
              facilitator_id INTEGER NOT NULL,
              capacity INTEGER NOT NULL DEFAULT 12,
              status TEXT NOT NULL DEFAULT 'open'
                CHECK(status IN ('open', 'running', 'closed')),
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (user_id) REFERENCES users(id),
              FOREIGN KEY (facilitator_id) REFERENCES users(id)
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS workshop_enrollments (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              workshop_id INTEGER NOT NULL,
              user_id INTEGER NOT NULL,
              status TEXT NOT NULL DEFAULT 'apprentice'
                CHECK(status IN ('apprentice', 'advanced')),
              enrolled_at TEXT DEFAULT CURRENT_TIMESTAMP,
              UNIQUE(workshop_id, user_id),
              FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
              FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS workshop_outputs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              workshop_id INTEGER NOT NULL,
              user_id INTEGER NOT NULL,
              kind TEXT NOT NULL CHECK(kind IN ('material', 'obra')),
              title TEXT NOT NULL,
              url TEXT,
              body TEXT,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
              FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS skill_awards (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              workshop_id INTEGER NOT NULL,
              user_id INTEGER NOT NULL,
              skill_node TEXT NOT NULL,
              outcome TEXT NOT NULL
                CHECK(outcome IN ('awaiting_triada', 'awarded', 'rejected')),
              mentor_ok INTEGER NOT NULL DEFAULT 0,
              peer_ok INTEGER NOT NULL DEFAULT 0,
              oracle_veto INTEGER NOT NULL DEFAULT 0,
              mentoria_horas REAL NOT NULL DEFAULT 0,
              obra_count INTEGER NOT NULL DEFAULT 0,
              material_count INTEGER NOT NULL DEFAULT 0,
              vacua_json TEXT NOT NULL,
              triada_json TEXT NOT NULL,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              UNIQUE(workshop_id, user_id),
              FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
              FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        db.commit()


@workshops_bp.route("", methods=["POST"])
@token_required
def create_workshop(current_user):
    """Crear un taller (5-12 personas). El creador es el facilitador."""
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    skill_node = (data.get("skill_node") or "").strip()
    description = (data.get("description") or "").strip()
    try:
        capacity = int(data.get("capacity", MAX_CAPACITY))
    except (TypeError, ValueError):
        return jsonify({"error": "capacity debe ser un entero"}), 400

    if not title:
        return jsonify({"error": "title es requerido"}), 400
    if len(title) > MAX_TITLE:
        return jsonify({"error": f"title no puede superar {MAX_TITLE} caracteres"}), 400
    if not skill_node:
        return jsonify({"error": "skill_node es requerido (nodo del árbol de habilidades)"}), 400
    if not is_valid_node_id(skill_node):
        return jsonify(
            {
                "error": "skill_node debe ser un nodo del árbol: 'rama' o 'rama/nodo' "
                "(slugs minúsculos, sin espacios ni apostrofes)"
            }
        ), 400
    if len(description) > MAX_DESCRIPTION:
        return jsonify(
            {"error": f"description no puede superar {MAX_DESCRIPTION} caracteres"}
        ), 400
    if capacity < MIN_CAPACITY or capacity > MAX_CAPACITY:
        return jsonify(
            {"error": f"capacity debe estar entre {MIN_CAPACITY} y {MAX_CAPACITY}"}
        ), 400

    uid = current_user.get("user_id")
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO workshops (user_id, title, skill_node, description, facilitator_id, capacity)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (uid, title, skill_node, description, uid, capacity),
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM workshops WHERE id = ?", (cur.lastrowid,)
    ).fetchone()
    return jsonify({"success": True, "workshop": _workshop_to_dict(db, row)}), 201


@workshops_bp.route("", methods=["GET"])
@token_required
def list_workshops(current_user):
    """Listar talleres (se muestra estado y cupo; nunca ranking de personas)."""
    status = (request.args.get("status") or "").strip()
    if status and status not in WORKSHOP_STATUSES:
        return jsonify({"error": "status inválido"}), 400
    try:
        limit = min(max(int(request.args.get("limit", 50)), 1), 100)
    except ValueError:
        return jsonify({"error": "limit debe ser un entero"}), 400

    db = get_db()
    if status:
        rows = db.execute(
            "SELECT * FROM workshops WHERE status = ? ORDER BY created_at DESC, id DESC LIMIT ?",
            (status, limit),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM workshops ORDER BY created_at DESC, id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    workshops = [_workshop_to_dict(db, r) for r in rows]
    return jsonify({"success": True, "count": len(workshops), "workshops": workshops})


@workshops_bp.route("/tree", methods=["GET"])
@token_required
def skill_tree(current_user):
    """El tejido visible: ramas canónicas del árbol de habilidades (T13).

    El árbol es patrimonio accesible (el conocimiento pasado es patrimonio,
    no necesita 60 ms de permiso); aquí se expone como ESTADO, nunca como
    ranking de personas (anti-gamificación: el mapa no compara a nadie).
    """
    from maxocontracts.tree import build_canonical_tree

    tree = build_canonical_tree()
    branches = []
    total = 0
    for branch in tree.branches():
        nodes = []
        for n in tree.nodes_by_branch(branch):
            nodes.append(
                {
                    "id": n.id,
                    "name": n.name,
                    "branch": n.branch,
                    "prereq_ids": list(n.prereq_ids),
                    "dificultad": n.dificultad,
                    "description": n.description,
                }
            )
            total += 1
        branches.append({"branch": branch, "count": len(nodes), "nodes": nodes})
    return jsonify(
        {
            "success": True,
            "tree": {
                "branches": branches,
                "total_nodes": total,
                "note": "El tejido es infinito y forkable: cualquier rama nueva puede nacer de la comunidad (con_node).",
            },
        }
    )


@workshops_bp.route("/<int:workshop_id>", methods=["GET"])
@token_required
def get_workshop(current_user, workshop_id):
    """Detalle del taller: obras públicas y el award del usuario actual (T13)."""
    db = get_db()
    row = db.execute("SELECT * FROM workshops WHERE id = ?", (workshop_id,)).fetchone()
    if row is None:
        return jsonify({"error": "taller no encontrado"}), 404
    workshop = _workshop_to_dict(db, row, include_outputs=True)
    uid = current_user.get("user_id")
    award = db.execute(
        "SELECT * FROM skill_awards WHERE workshop_id = ? AND user_id = ?",
        (workshop_id, uid),
    ).fetchone()
    workshop["my_award"] = (
        {
            "outcome": award["outcome"],
            "skill_node": award["skill_node"],
            "mentoria_horas": award["mentoria_horas"],
            "obra_count": award["obra_count"],
            "material_count": award["material_count"],
            "created_at": award["created_at"],
        }
        if award
        else None
    )
    # Lista de enrolados (T13): la triada no se hace a ciegas; el facilitador
    # ve quién vacua. Estado, no ranking.
    workshop["enrollments"] = [
        {"user_id": r["user_id"], "name": r["name"]}
        for r in db.execute(
            """
            SELECT e.user_id, u.name FROM workshop_enrollments e
            JOIN users u ON u.id = e.user_id
            WHERE e.workshop_id = ?
            ORDER BY e.enrolled_at ASC, e.user_id ASC
            """,
            (workshop_id,),
        ).fetchall()
    ]
    return jsonify({"success": True, "workshop": workshop})


@workshops_bp.route("/<int:workshop_id>/enroll", methods=["POST"])
@token_required
def enroll_workshop(current_user, workshop_id):
    """Inscribirse como aprendiz (no hay más examen de entrada que la plaza)."""
    db = get_db()
    row = db.execute("SELECT * FROM workshops WHERE id = ?", (workshop_id,)).fetchone()
    if row is None:
        return jsonify({"error": "taller no encontrado"}), 404
    if row["status"] != "open":
        return jsonify({"error": "el taller no está abierto"}), 400

    uid = current_user.get("user_id")
    if uid == row["facilitator_id"]:
        return jsonify({"error": "el facilitador ya facilita este taller"}), 400

    existing = db.execute(
        "SELECT 1 FROM workshop_enrollments WHERE workshop_id = ? AND user_id = ?",
        (workshop_id, uid),
    ).fetchone()
    if existing:
        return jsonify({"error": "ya estás inscrito en este taller"}), 409

    if _enrollment_count(db, workshop_id) >= row["capacity"]:
        return jsonify({"error": "el taller llegó a su cupo"}), 409

    db.execute(
        "INSERT INTO workshop_enrollments (workshop_id, user_id) VALUES (?, ?)",
        (workshop_id, uid),
    )
    db.commit()
    return jsonify({"success": True, "message": "inscrito como aprendiz"})


@workshops_bp.route("/<int:workshop_id>/outputs", methods=["POST"])
@token_required
def add_output(current_user, workshop_id):
    """Publicar una obra de salida (material abierto | obra aplicada)."""
    data = request.get_json() or {}
    kind = (data.get("kind") or "").strip()
    title = (data.get("title") or "").strip()
    url = (data.get("url") or "").strip()
    body = (data.get("body") or "").strip()[:5000]

    if kind not in OUTPUT_KINDS:
        return jsonify({"error": "kind inválido", "allowed": list(OUTPUT_KINDS)}), 400
    if not title:
        return jsonify({"error": "title es requerido"}), 400

    db = get_db()
    row = db.execute("SELECT * FROM workshops WHERE id = ?", (workshop_id,)).fetchone()
    if row is None:
        return jsonify({"error": "taller no encontrado"}), 404

    uid = current_user.get("user_id")
    is_facilitator = uid == row["facilitator_id"]
    is_enrolled = bool(
        db.execute(
            "SELECT 1 FROM workshop_enrollments WHERE workshop_id = ? AND user_id = ?",
            (workshop_id, uid),
        ).fetchone()
    )
    if not (is_facilitator or is_enrolled):
        return jsonify({"error": "debes estar inscrito en el taller para publicar obras"}), 403

    cur = db.execute(
        """
        INSERT INTO workshop_outputs (workshop_id, user_id, kind, title, url, body)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (workshop_id, uid, kind, title, url or None, body or None),
    )
    db.commit()
    return jsonify({"success": True, "output_id": cur.lastrowid}), 201


@workshops_bp.route("/<int:workshop_id>/grant-skill", methods=["POST"])
@token_required
def grant_skill(current_user, workshop_id):
    """Concesión de skill: regla de oro (motor) + triada (mentor/par/oráculo).

    Solo el facilitador concede. La triada se registra completa (T13);
    el oráculo tiene veto, no voto. Guardarraíles: nada de ranking por
    persona y ningún cronometraje del ensayo-error.
    """
    data = request.get_json() or {}
    try:
        mentoria_horas = float(data.get("mentoria_horas", 0.0))
    except (TypeError, ValueError):
        return jsonify({"error": "mentoria_horas debe ser un número"}), 400
    if mentoria_horas < 0:
        return jsonify({"error": "mentoria_horas no puede ser negativa"}), 400

    # La triada: el facilitador firma como mentor; el par y el oráculo votan.
    votos = TriadaVotos(
        mentor_ok=bool(data.get("mentor_ok", False)),
        peer_ok=bool(data.get("peer_ok", False)),
        oracle_veto=bool(data.get("oracle_veto", False)),
    )

    db = get_db()
    row = db.execute("SELECT * FROM workshops WHERE id = ?", (workshop_id,)).fetchone()
    if row is None:
        return jsonify({"error": "taller no encontrado"}), 404
    uid = current_user.get("user_id")
    if uid != row["facilitator_id"] and not bool(current_user.get("is_admin")):
        return jsonify({"error": "solo el facilitador puede conceder el skill"}), 403

    target_user = data.get("user_id")  # el aprendiz que vacua
    if target_user is None:
        return jsonify({"error": "user_id del aprendiz es requerido"}), 400
    try:
        target_user = int(target_user)
    except (TypeError, ValueError):
        return jsonify({"error": "user_id debe ser un entero"}), 400

    enrolled = db.execute(
        "SELECT 1 FROM workshop_enrollments WHERE workshop_id = ? AND user_id = ?",
        (workshop_id, target_user),
    ).fetchone()
    if not enrolled:
        return jsonify({"error": "el aprendiz no está inscrito en este taller"}), 400

    obra_count = int(
        db.execute(
            "SELECT COUNT(*) FROM workshop_outputs WHERE workshop_id = ? AND user_id = ? AND kind = 'obra'",
            (workshop_id, target_user),
        ).fetchone()[0]
    )
    material_count = int(
        db.execute(
            "SELECT COUNT(*) FROM workshop_outputs WHERE workshop_id = ? AND user_id = ? AND kind = 'material'",
            (workshop_id, target_user),
        ).fetchone()[0]
    )
    obra_aplicada = obra_count >= 1
    material_publicado = material_count >= 1

    veredicto = evaluar_concesion(
        obra_aplicada=obra_aplicada,
        material_publicado=material_publicado,
        mentoria_horas=mentoria_horas,
        votos=votos,
    )

    existing = db.execute(
        "SELECT id FROM skill_awards WHERE workshop_id = ? AND user_id = ?",
        (workshop_id, target_user),
    ).fetchone()
    if existing:
        db.execute(
            """
            UPDATE skill_awards
            SET outcome = ?, mentor_ok = ?, peer_ok = ?, oracle_veto = ?,
                mentoria_horas = ?, obra_count = ?, material_count = ?,
                vacua_json = ?, triada_json = ?
            WHERE id = ?
            """,
            (
                veredicto["outcome"],
                int(veredicto["triada"]["aprobada"] and votos.mentor_ok),
                int(votos.peer_ok),
                int(votos.oracle_veto),
                mentoria_horas,
                obra_count,
                material_count,
                json.dumps(veredicto["vacua"], ensure_ascii=False),
                json.dumps(veredicto["triada"], ensure_ascii=False),
                existing["id"],
            ),
        )
    else:
        db.execute(
            """
            INSERT INTO skill_awards (
              workshop_id, user_id, skill_node, outcome, mentor_ok, peer_ok,
              oracle_veto, mentoria_horas, obra_count, material_count,
              vacua_json, triada_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                workshop_id,
                target_user,
                row["skill_node"],
                veredicto["outcome"],
                int(votos.mentor_ok),
                int(votos.peer_ok),
                int(votos.oracle_veto),
                mentoria_horas,
                obra_count,
                material_count,
                json.dumps(veredicto["vacua"], ensure_ascii=False),
                json.dumps(veredicto["triada"], ensure_ascii=False),
            ),
        )
    db.commit()

    return jsonify(
        {
            "success": True,
            "award": {
                "workshop_id": workshop_id,
                "user_id": target_user,
                "skill_node": row["skill_node"],
                "outcome": veredicto["outcome"],
                "vacua_faltantes": veredicto["vacua"]["faltantes"],
                "triada_bloqueos": veredicto["triada"]["bloqueos"],
            },
        }
    )


@workshops_bp.route("/<int:workshop_id>/close", methods=["POST"])
@token_required
def close_workshop(current_user, workshop_id):
    """Cerrar el taller (el facilitador; un taller se cierra, no se borra)."""
    db = get_db()
    row = db.execute("SELECT * FROM workshops WHERE id = ?", (workshop_id,)).fetchone()
    if row is None:
        return jsonify({"error": "taller no encontrado"}), 404
    uid = current_user.get("user_id")
    if uid != row["facilitator_id"] and not bool(current_user.get("is_admin")):
        return jsonify({"error": "solo el facilitador puede cerrar el taller"}), 403
    db.execute(
        "UPDATE workshops SET status = 'closed', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (workshop_id,),
    )
    db.commit()
    updated = db.execute("SELECT * FROM workshops WHERE id = ?", (workshop_id,)).fetchone()
    return jsonify({"success": True, "workshop": _workshop_to_dict(db, updated)})

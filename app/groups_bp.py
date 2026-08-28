"""
Grupos de Solución de Necesidades (ECEs) y Células Madre.

La estructura triádica del aprendizaje (OEV §1.7) tiene su tercer cuerpo en
estos grupos: una necesidad real entra de la comunidad (desde el Foro
Abierto o el matching) y un grupo la resuelve aplicando lo aprendido en los
Talleres; cada grupo siembra aprendizaje (documenta y forma).

Las Células Madre son el meta-grupo cuyo oficio es formar otros grupos
(la máquina fractal en su tercer nivel): cada grupo registra su matriz y
la célula madre gana el nodo "facilitación" al ver florecer una réplica.

Guardarraíles: la trazabilidad es registrable y pública (T13); la
coordinación no es mandato (la célula coordina, no manda); nada de
rankings por persona.

Endpoints:
- POST /groups            — crear (solution_group | mother_cell).
- GET  /groups            — listar (con filas y tipo).
- GET  /groups/<id>       — detalle (miembros, hijos, nodos ganados).
- POST /groups/<id>/join  — unirse.
- POST /groups/<id>/child — registrar un grupo hijo (réplica fractal).
- POST /groups/<id>/close — cerrar (coordinador).
"""

import logging
from typing import Any, Dict, List, Optional

from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .utils import get_db

logger = logging.getLogger(__name__)

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")

GROUP_KINDS = ("solution_group", "mother_cell")
GROUP_STATUSES = ("active", "closed")
MAX_NAME = 160
MAX_DESCRIPTION = 3000


def _group_to_dict(db, row: Any, include_members: bool = False) -> Dict[str, Any]:
    members = db.execute(
        """
        SELECT egm.user_id, egm.role, u.name
        FROM edu_group_members egm JOIN users u ON u.id = egm.user_id
        WHERE egm.group_id = ? ORDER BY egm.joined_at ASC, egm.id ASC
        """,
        (row["id"],),
    ).fetchall()
    children = db.execute(
        """
        SELECT eg.id, eg.name, eg.kind, eg.status
        FROM edu_group_children egc JOIN edu_groups eg ON eg.id = egc.child_id
        WHERE egc.parent_id = ? ORDER BY egc.created_at ASC
        """,
        (row["id"],),
    ).fetchall()
    nodes = db.execute(
        "SELECT skill_node, evidence, created_at FROM group_skill_nodes WHERE group_id = ?",
        (row["id"],),
    ).fetchall()
    creator = db.execute(
        "SELECT name FROM users WHERE id = ?", (row["user_id"],)
    ).fetchone()

    result: Dict[str, Any] = {
        "id": row["id"],
        "kind": row["kind"],
        "name": row["name"],
        "description": row["description"],
        "need_title": row["need_title"],
        "need_id": row["need_id"],
        "status": row["status"],
        "member_count": len(members),
        "creator": {"user_id": row["user_id"], "name": creator["name"] if creator else "desconocido"},
        "children": [
            {"id": c["id"], "name": c["name"], "kind": c["kind"], "status": c["status"]}
            for c in children
        ],
        "skill_nodes": [
            {
                "skill_node": n["skill_node"],
                "evidence": n["evidence"],
                "created_at": n["created_at"],
            }
            for n in nodes
        ],
        "created_at": row["created_at"],
    }
    if include_members:
        result["members"] = [
            {"user_id": m["user_id"], "name": m["name"], "role": m["role"]}
            for m in members
        ]
    return result


def init_groups_tables(app) -> None:
    """Crea las tablas de grupos educativos si no existen (schema idempotente)."""
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS edu_groups (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              kind TEXT NOT NULL CHECK(kind IN ('solution_group', 'mother_cell')),
              name TEXT NOT NULL,
              description TEXT,
              need_title TEXT,
              need_id INTEGER,
              status TEXT NOT NULL DEFAULT 'active'
                CHECK(status IN ('active', 'closed')),
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS edu_group_members (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              group_id INTEGER NOT NULL,
              user_id INTEGER NOT NULL,
              role TEXT NOT NULL DEFAULT 'member'
                CHECK(role IN ('member', 'coordinator')),
              joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
              UNIQUE(group_id, user_id),
              FOREIGN KEY (group_id) REFERENCES edu_groups(id) ON DELETE CASCADE,
              FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS edu_group_children (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              parent_id INTEGER NOT NULL,
              child_id INTEGER NOT NULL,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              UNIQUE(parent_id, child_id),
              FOREIGN KEY (parent_id) REFERENCES edu_groups(id) ON DELETE CASCADE,
              FOREIGN KEY (child_id) REFERENCES edu_groups(id) ON DELETE CASCADE
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS group_skill_nodes (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              group_id INTEGER NOT NULL,
              skill_node TEXT NOT NULL,
              evidence TEXT NOT NULL,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              UNIQUE(group_id, skill_node),
              FOREIGN KEY (group_id) REFERENCES edu_groups(id) ON DELETE CASCADE
            )
            """
        )
        db.commit()


@groups_bp.route("", methods=["POST"])
@token_required
def create_group(current_user):
    """Crear un grupo de solución (ECE) o una célula madre.

    Un grupo de solución nace de una necesidad real (título obligatorio);
    una célula madre no la necesita: su oficio es formar grupos.
    """
    data = request.get_json() or {}
    kind = (data.get("kind") or "").strip()
    name = (data.get("name") or "").strip()
    description = (data.get("description") or "").strip()
    need_title = (data.get("need_title") or "").strip()
    need_id = data.get("need_id")
    parent_group_id = data.get("parent_group_id")

    if kind not in GROUP_KINDS:
        return jsonify({"error": "kind inválido", "allowed": list(GROUP_KINDS)}), 400
    if not name:
        return jsonify({"error": "name es requerido"}), 400
    if len(name) > MAX_NAME:
        return jsonify({"error": f"name no puede superar {MAX_NAME} caracteres"}), 400
    if len(description) > MAX_DESCRIPTION:
        return jsonify(
            {"error": f"description no puede superar {MAX_DESCRIPTION} caracteres"}
        ), 400
    if kind == "solution_group" and not need_title:
        return jsonify(
            {"error": "need_title es requerido: el ECE nace de una necesidad real"}
        ), 400
    if need_id is not None and (not isinstance(need_id, int) or need_id <= 0):
        return jsonify({"error": "need_id debe ser un entero positivo"}), 400

    uid = current_user.get("user_id")
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO edu_groups (user_id, kind, name, description, need_title, need_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (uid, kind, name, description, need_title or None, need_id),
    )
    group_id = cur.lastrowid
    db.execute(
        "INSERT INTO edu_group_members (group_id, user_id, role) VALUES (?, ?, 'coordinator')",
        (group_id, uid),
    )

    # Fractalidad: si nace dentro de una célula madre, se registra la réplica
    # y la madre gana el nodo "facilitación" (la validación es la transferencia).
    if parent_group_id is not None:
        parent = db.execute(
            "SELECT * FROM edu_groups WHERE id = ?", (parent_group_id,)
        ).fetchone()
        if parent is None:
            db.rollback()
            return jsonify({"error": "célula madre no encontrada"}), 404
        if parent["kind"] != "mother_cell":
            db.rollback()
            return jsonify({"error": "el grupo padre debe ser una célula madre"}), 400
        db.execute(
            "INSERT INTO edu_group_children (parent_id, child_id) VALUES (?, ?)",
            (parent_group_id, group_id),
        )
        db.execute(
            """
            INSERT OR IGNORE INTO group_skill_nodes (group_id, skill_node, evidence)
            VALUES (?, 'facilitacion', ?)
            """,
            (
                parent_group_id,
                f"replica '{name}' (grupo {group_id}) registrada {group_id}",
            ),
        )
    db.commit()

    row = db.execute("SELECT * FROM edu_groups WHERE id = ?", (group_id,)).fetchone()
    return jsonify({"success": True, "group": _group_to_dict(db, row)}), 201


@groups_bp.route("", methods=["GET"])
@token_required
def list_groups(current_user):
    """Listar grupos (solución y células madre), sin rankings de personas."""
    kind = (request.args.get("kind") or "").strip()
    if kind and kind not in GROUP_KINDS:
        return jsonify({"error": "kind inválido"}), 400
    db = get_db()
    if kind:
        rows = db.execute(
            "SELECT * FROM edu_groups WHERE kind = ? ORDER BY created_at DESC, id DESC",
            (kind,),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM edu_groups ORDER BY created_at DESC, id DESC"
        ).fetchall()
    groups = [_group_to_dict(db, r) for r in rows]
    return jsonify({"success": True, "count": len(groups), "groups": groups})


@groups_bp.route("/<int:group_id>", methods=["GET"])
@token_required
def get_group(current_user, group_id):
    """Detalle con miembros, réplicas y nodos ganados (T13)."""
    db = get_db()
    row = db.execute("SELECT * FROM edu_groups WHERE id = ?", (group_id,)).fetchone()
    if row is None:
        return jsonify({"error": "grupo no encontrado"}), 404
    return jsonify(
        {"success": True, "group": _group_to_dict(db, row, include_members=True)}
    )


@groups_bp.route("/<int:group_id>/join", methods=["POST"])
@token_required
def join_group(current_user, group_id):
    """Unirse a un grupo (la puerta es el foro; no hay examen de entrada)."""
    db = get_db()
    row = db.execute("SELECT * FROM edu_groups WHERE id = ?", (group_id,)).fetchone()
    if row is None:
        return jsonify({"error": "grupo no encontrado"}), 404
    if row["status"] != "active":
        return jsonify({"error": "el grupo está cerrado"}), 400

    uid = current_user.get("user_id")
    existing = db.execute(
        "SELECT 1 FROM edu_group_members WHERE group_id = ? AND user_id = ?",
        (group_id, uid),
    ).fetchone()
    if existing:
        return jsonify({"error": "ya eres miembro de este grupo"}), 409

    db.execute(
        "INSERT INTO edu_group_members (group_id, user_id, role) VALUES (?, ?, 'member')",
        (group_id, uid),
    )
    db.commit()
    return jsonify({"success": True, "message": "miembro del grupo"})


@groups_bp.route("/<int:group_id>/child", methods=["POST"])
@token_required
def register_child(current_user, group_id):
    """Registrar una réplica (grupo hijo) y recompensar el nodo de la madre.

    La célula madre gana 'facilitación' al ver florecer una réplica: cada
    grupo formado registra su matriz (trazabilidad fractal del OEV).
    """
    data = request.get_json() or {}
    child_id = data.get("child_group_id")
    if child_id is None:
        return jsonify({"error": "child_group_id es requerido"}), 400
    try:
        child_id = int(child_id)
    except (TypeError, ValueError):
        return jsonify({"error": "child_group_id debe ser un entero"}), 400

    db = get_db()
    parent = db.execute("SELECT * FROM edu_groups WHERE id = ?", (group_id,)).fetchone()
    if parent is None:
        return jsonify({"error": "grupo madre no encontrado"}), 404
    if parent["kind"] != "mother_cell":
        return jsonify({"error": "solo una célula madre puede registrar réplicas"}), 400

    uid = current_user.get("user_id")
    is_member = db.execute(
        "SELECT 1 FROM edu_group_members WHERE group_id = ? AND user_id = ?",
        (group_id, uid),
    ).fetchone()
    if not is_member and not bool(current_user.get("is_admin")):
        return jsonify({"error": "debes ser miembro de la célula madre"}), 403

    child = db.execute("SELECT * FROM edu_groups WHERE id = ?", (child_id,)).fetchone()
    if child is None:
        return jsonify({"error": "grupo hijo no encontrado"}), 404
    if child_id == group_id:
        return jsonify({"error": "un grupo no puede ser réplica de sí mismo"}), 400

    existing = db.execute(
        "SELECT 1 FROM edu_group_children WHERE parent_id = ? AND child_id = ?",
        (group_id, child_id),
    ).fetchone()
    if existing:
        return jsonify({"error": "la réplica ya estaba registrada"}), 409

    db.execute(
        "INSERT INTO edu_group_children (parent_id, child_id) VALUES (?, ?)",
        (group_id, child_id),
    )
    db.execute(
        """
        INSERT OR IGNORE INTO group_skill_nodes (group_id, skill_node, evidence)
        VALUES (?, 'facilitacion', ?)
        """,
        (
            group_id,
            f"replica '{child['name']}' (grupo {child_id}) registrada",
        ),
    )
    db.commit()
    return jsonify({"success": True, "message": "réplica registrada"})


@groups_bp.route("/<int:group_id>/close", methods=["POST"])
@token_required
def close_group(current_user, group_id):
    """Cerrar un grupo (el coordinador; un grupo se cierra, no se borra)."""
    db = get_db()
    row = db.execute("SELECT * FROM edu_groups WHERE id = ?", (group_id,)).fetchone()
    if row is None:
        return jsonify({"error": "grupo no encontrado"}), 404
    uid = current_user.get("user_id")
    is_coordinator = bool(
        db.execute(
            "SELECT 1 FROM edu_group_members WHERE group_id = ? AND user_id = ? AND role = 'coordinator'",
            (group_id, uid),
        ).fetchone()
    )
    if not is_coordinator and not bool(current_user.get("is_admin")):
        return jsonify({"error": "solo el coordinador puede cerrar el grupo"}), 403
    db.execute(
        "UPDATE edu_groups SET status = 'closed', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (group_id,),
    )
    db.commit()
    updated = db.execute("SELECT * FROM edu_groups WHERE id = ?", (group_id,)).fetchone()
    return jsonify({"success": True, "group": _group_to_dict(db, updated)})

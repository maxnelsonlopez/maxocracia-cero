"""
Foro Abierto — la plaza del conocimiento de la Maxocracia.

El Foro Abierto es el punto de entrada de la estructura triádica del
aprendizaje (OEV, docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md
§1.7): cualquier persona propone un tema, hace una pregunta, ofrece un
taller o levanta una necesidad. Sin matrícula, sin credencial, sin juez de
entrada: la ignorancia bienvenida (A2) y la voz disidente con silla (T12).

Del foro nacen los tres cuerpos del aprendizaje:
- preguntas -> Talleres de Aprendizaje (workshops_bp).
- necesidades -> Grupos de Solución (groups_bp, ECEs).
- personas  -> Células (mother cells).

Este blueprint NO duplica las necesidades de forms_bp (participant_needs):
el post de tipo `need` puede vincularla por `need_id` (referencia, no copia)
y /forum/needs es la puerta hacia el matching de necesidades.

Reglas de diseño (teoría):
- Sin ratings por persona, sin rankings: el foro expone estado, no jerarquía.
- Ningún endpoint borra contenidos ajenos: el autor cierra el suyo, un admin
  puede cerrar por moderación (spam/cumplimiento legal), nunca por opinión.
- Todo queda registrado (T13: autor, fechas, estado, resolución auditable).

Endpoints:
- POST   /forum/posts               — publicar (topic|question|workshop_offer|need).
- GET    /forum/posts               — listar con filtros (type, tag, status).
- GET    /forum/posts/<id>          — detalle (T13).
- POST   /forum/posts/<id>/close    — cerrar (autor o admin; resolución opcional).
- GET    /forum/needs               — necesidades abiertas (puerta al matching).
"""

import json
import logging
from typing import Any, Dict, List, Optional

from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .utils import get_db

logger = logging.getLogger(__name__)

forum_bp = Blueprint("forum", __name__, url_prefix="/forum")

# Tipos canónicos del Foro Abierto (estructura triádica, §1.7).
KINDS: Dict[str, str] = {
    "topic": "Tema",
    "question": "Pregunta",
    "workshop_offer": "Oferta de taller",
    "need": "Necesidad educativa",
}

STATUSES = ("open", "closed", "resolved")

MAX_TITLE = 200
MAX_BODY = 5000
MAX_TAGS = 10
MAX_TAG_LEN = 40


def _parse_tags(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    try:
        value = json.loads(raw)
        return value if isinstance(value, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _post_to_dict(db: Any, row: Any) -> Dict[str, Any]:
    """Serialización T13 de un post del foro (procedencia y estado legibles)."""
    replies_count = db.execute(
        "SELECT COUNT(*) FROM forum_replies WHERE post_id = ?",
        (row["id"],),
    ).fetchone()[0]
    return {
        "id": row["id"],
        "kind": row["kind"],
        "kind_label": KINDS.get(row["kind"], row["kind"]),
        "title": row["title"],
        "body": row["body"],
        "tags": _parse_tags(row["tags"]),
        "status": row["status"],
        "need_id": row["need_id"],
        "in_plaza": row["need_id"] is not None,
        "reply_count": int(replies_count or 0),
        "author": {
            "user_id": row["user_id"],
            "name": row["name"],
        },
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _link_forum_need_to_matching(db: Any, uid: int, body: str) -> Optional[int]:
    """Puente siamés (M8): la necesidad del foro sangra al matching.

    Si el autor tiene Formulario CERO (participante), se crea/vincula la
    necesidad en `participant_needs` — la MISMA tabla que consume la Plaza
    de Apoyo (Cap. 12.3.1 + bombeo vital: el SDV protege la vida para que
    la EIR la eleve; la necesidad educativa entra por la comunidad y la
    solución vuelve al hilo).

    Devuelve el `need_id` vinculado, o None si el autor no tiene
    participante (el post queda standalone con aviso honesto).
    """
    user = db.execute("SELECT email FROM users WHERE id = ?", (uid,)).fetchone()
    if user is None:
        return None
    participant = db.execute(
        "SELECT id FROM participants WHERE email = ?", (user["email"],)
    ).fetchone()
    if participant is None:
        return None
    pid = participant["id"]

    # No duplicar: si ya existe una necesidad activa idéntica, se referencia.
    existing = db.execute(
        """
        SELECT id FROM participant_needs
        WHERE participant_id = ? AND description = ? AND status = 'active'
        """,
        (pid, body),
    ).fetchone()
    if existing:
        return existing["id"]

    cur = db.execute(
        """
        INSERT INTO participant_needs (
          participant_id, description, categories, urgency, human_dimensions, status
        ) VALUES (?, ?, ?, 'Media', ?, 'active')
        """,
        (
            pid,
            body,
            json.dumps(["educacion"], ensure_ascii=False),
            json.dumps(["crecimiento_aprendizaje"], ensure_ascii=False),
        ),
    )
    db.commit()
    return cur.lastrowid


def init_forum_tables(app) -> None:
    """Crea la tabla del foro si no existe (schema idempotente, patrón init_*)."""
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS forum_posts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              kind TEXT NOT NULL CHECK(kind IN ('topic', 'question', 'workshop_offer', 'need')),
              title TEXT NOT NULL,
              body TEXT NOT NULL,
              tags TEXT,
              status TEXT NOT NULL DEFAULT 'open'
                CHECK(status IN ('open', 'closed', 'resolved')),
              need_id INTEGER,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_forum_posts_kind ON forum_posts(kind);"
        )
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_forum_posts_status ON forum_posts(status);"
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS forum_replies (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              post_id INTEGER NOT NULL,
              user_id INTEGER NOT NULL,
              body TEXT NOT NULL,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (post_id) REFERENCES forum_posts(id) ON DELETE CASCADE,
              FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_forum_replies_post ON forum_replies(post_id);"
        )
        db.commit()


@forum_bp.route("/posts", methods=["POST"])
@token_required
def create_post(current_user):
    """Publicar en la plaza (la ignorancia bienvenida: no hay examen de entrada)."""
    data = request.get_json() or {}
    kind = (data.get("kind") or "").strip()
    title = (data.get("title") or "").strip()
    body = (data.get("body") or "").strip()
    tags = data.get("tags") or []
    need_id = data.get("need_id")

    if kind not in KINDS:
        return (
            jsonify(
                {
                    "error": "kind inválido",
                    "allowed": sorted(KINDS.keys()),
                }
            ),
            400,
        )
    if not title:
        return jsonify({"error": "title es requerido"}), 400
    if len(title) > MAX_TITLE:
        return jsonify({"error": f"title no puede superar {MAX_TITLE} caracteres"}), 400
    if not body:
        return jsonify({"error": "body es requerido"}), 400
    if len(body) > MAX_BODY:
        return jsonify({"error": f"body no puede superar {MAX_BODY} caracteres"}), 400
    if not isinstance(tags, list):
        return jsonify({"error": "tags debe ser una lista"}), 400
    if len(tags) > MAX_TAGS:
        return jsonify({"error": f"máximo {MAX_TAGS} tags"}), 400
    tags = [str(t).strip()[:MAX_TAG_LEN] for t in tags if str(t).strip()]
    if need_id is not None and kind != "need":
        return jsonify({"error": "need_id solo aplica a posts de tipo need"}), 400

    uid = current_user.get("user_id")
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO forum_posts (user_id, kind, title, body, tags, need_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (uid, kind, title, body, json.dumps(tags, ensure_ascii=False), need_id),
    )

    # Puente siamés: la necesidad educativa del foro sangra a la Plaza de
    # Apoyo (la misma participant_needs que consume el matching), cuando el
    # autor tiene Formulario CERO; el cierre con resolución del hilo es el
    # retorno de la solución (la necesidad entra, la solución vuelve).
    linked_need_id = None
    if kind == "need" and need_id is None:
        linked_need_id = _link_forum_need_to_matching(db, uid, body)
        if linked_need_id is not None:
            db.execute(
                "UPDATE forum_posts SET need_id = ? WHERE id = ?",
                (linked_need_id, cur.lastrowid),
            )
    db.commit()
    row = db.execute(
        """
        SELECT fp.*, u.name FROM forum_posts fp
        JOIN users u ON u.id = fp.user_id
        WHERE fp.id = ?
        """,
        (cur.lastrowid,),
    ).fetchone()
    return jsonify({"success": True, "post": _post_to_dict(db, row)}), 201


@forum_bp.route("/posts", methods=["GET"])
@token_required
def list_posts(current_user):
    """Listar la plaza con filtros opcionales (type, tag, status, q, limit)."""
    kind = (request.args.get("type") or "").strip()
    tag = (request.args.get("tag") or "").strip()
    status = (request.args.get("status") or "").strip()
    term = (request.args.get("q") or "").strip()
    try:
        limit = min(max(int(request.args.get("limit", 50)), 1), 100)
    except ValueError:
        return jsonify({"error": "limit debe ser un entero"}), 400

    clauses, params = [], []
    if kind:
        if kind not in KINDS:
            return (
                jsonify({"error": "type inválido", "allowed": sorted(KINDS.keys())}),
                400,
            )
        clauses.append("fp.kind = ?")
        params.append(kind)
    if status:
        if status not in STATUSES:
            return jsonify({"error": "status inválido"}), 400
        clauses.append("fp.status = ?")
        params.append(status)
    # El filtro por tag es determinista: el tag vive serializado en la columna tags.
    if tag:
        clauses.append("fp.tags LIKE ?")
        params.append(f'%"{tag}"%')
    # Búsqueda textual literal (título o cuerpo): los comodines de LIKE se
    # escapan para que el término sea literal y no un pattern (T13: la plaza
    # se busca y se entiende; nada se interpreta de más).
    if term:
        escaped = (
            term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        )
        pattern = f"%{escaped.lower()}%"
        clauses.append(
            "(LOWER(fp.title) LIKE ? ESCAPE '\\' OR LOWER(fp.body) LIKE ? ESCAPE '\\')"
        )
        params.extend([pattern, pattern])

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    db = get_db()
    rows = db.execute(
        f"""
        SELECT fp.*, u.name FROM forum_posts fp
        JOIN users u ON u.id = fp.user_id
        {where}
        ORDER BY fp.created_at DESC, fp.id DESC
        LIMIT ?
        """,
        (*params, limit),
    ).fetchall()
    posts = [_post_to_dict(db, r) for r in rows]
    return jsonify({"success": True, "count": len(posts), "posts": posts})


@forum_bp.route("/posts/<int:post_id>", methods=["GET"])
@token_required
def get_post(current_user, post_id):
    """Detalle T13 de un post."""
    db = get_db()
    row = db.execute(
        """
        SELECT fp.*, u.name FROM forum_posts fp
        JOIN users u ON u.id = fp.user_id
        WHERE fp.id = ?
        """,
        (post_id,),
    ).fetchone()
    if row is None:
        return jsonify({"error": "post no encontrado"}), 404
    return jsonify({"success": True, "post": _post_to_dict(db, row)})


@forum_bp.route("/posts/<int:post_id>/replies", methods=["POST"])
@token_required
def add_reply(current_user, post_id):
    """Responder en la plaza: la conversación que la hace viva.

    La ignorancia bienvenida y la disidencia con silla: toda voz responde,
    sin credencial. Los posts cerrados/resueltos no reciben respuestas
    nuevas (el cierre es el fin declarado de la conversación).
    """
    data = request.get_json() or {}
    body = (data.get("body") or "").strip()

    if not body:
        return jsonify({"error": "body es requerido"}), 400
    if len(body) > MAX_BODY:
        return jsonify({"error": f"body no puede superar {MAX_BODY} caracteres"}), 400

    db = get_db()
    post = db.execute("SELECT * FROM forum_posts WHERE id = ?", (post_id,)).fetchone()
    if post is None:
        return jsonify({"error": "post no encontrado"}), 404
    if post["status"] != "open":
        return jsonify({"error": "el post está cerrado: su conversación ya cerró"}), 400

    uid = current_user.get("user_id")
    cur = db.execute(
        "INSERT INTO forum_replies (post_id, user_id, body) VALUES (?, ?, ?)",
        (post_id, uid, body),
    )
    db.commit()
    reply = db.execute(
        "SELECT fr.*, u.name FROM forum_replies fr JOIN users u ON u.id = fr.user_id WHERE fr.id = ?",
        (cur.lastrowid,),
    ).fetchone()
    return (
        jsonify(
            {
                "success": True,
                "reply": {
                    "id": reply["id"],
                    "post_id": reply["post_id"],
                    "body": reply["body"],
                    "author": {"user_id": reply["user_id"], "name": reply["name"]},
                    "created_at": reply["created_at"],
                },
            }
        ),
        201,
    )


@forum_bp.route("/posts/<int:post_id>/replies", methods=["GET"])
@token_required
def list_replies(current_user, post_id):
    """Listar las respuestas de un post (la conversación es pública, T13)."""
    db = get_db()
    post = db.execute("SELECT * FROM forum_posts WHERE id = ?", (post_id,)).fetchone()
    if post is None:
        return jsonify({"error": "post no encontrado"}), 404
    rows = db.execute(
        """
        SELECT fr.*, u.name FROM forum_replies fr
        JOIN users u ON u.id = fr.user_id
        WHERE fr.post_id = ?
        ORDER BY fr.created_at ASC, fr.id ASC
        """,
        (post_id,),
    ).fetchall()
    replies = [
        {
            "id": r["id"],
            "post_id": r["post_id"],
            "body": r["body"],
            "author": {"user_id": r["user_id"], "name": r["name"]},
            "created_at": r["created_at"],
        }
        for r in rows
    ]
    return jsonify({"success": True, "count": len(replies), "replies": replies})


@forum_bp.route("/posts/<int:post_id>/close", methods=["POST"])
@token_required
def close_post(current_user, post_id):
    """Cerrar un post (resuelto si la persona declara su salida).

    Solo el autor o un admin. La plaza no borra: cierra (T12: la disidencia
    tiene silla; el cierre registra resolución auditable).
    """
    data = request.get_json() or {}
    resolution = (data.get("resolution") or "").strip()[:1000]

    db = get_db()
    row = db.execute("SELECT * FROM forum_posts WHERE id = ?", (post_id,)).fetchone()
    if row is None:
        return jsonify({"error": "post no encontrado"}), 404

    uid = current_user.get("user_id")
    is_admin = bool(current_user.get("is_admin"))
    if row["user_id"] != uid and not is_admin:
        return jsonify({"error": "No tienes autorización"}), 403

    new_status = "resolved" if resolution else "closed"
    db.execute(
        """
        UPDATE forum_posts
        SET status = ?, body = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (new_status, resolution or row["body"], post_id),
    )
    db.commit()
    updated = db.execute(
        "SELECT fp.*, u.name FROM forum_posts fp JOIN users u ON u.id = fp.user_id WHERE fp.id = ?",
        (post_id,),
    ).fetchone()
    return jsonify({"success": True, "post": _post_to_dict(db, updated)})


@forum_bp.route("/needs", methods=["GET"])
@token_required
def forum_needs(current_user):
    """Necesidades abiertas del foro — la puerta hacia el matching/Grupos de Solución."""
    db = get_db()
    rows = db.execute(
        """
        SELECT fp.*, u.name FROM forum_posts fp
        JOIN users u ON u.id = fp.user_id
        WHERE fp.kind = 'need' AND fp.status = 'open'
        ORDER BY fp.created_at DESC, fp.id DESC
        """
    ).fetchall()
    posts = [_post_to_dict(db, r) for r in rows]
    return jsonify({"success": True, "count": len(posts), "posts": posts})

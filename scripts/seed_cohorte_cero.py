# -*- coding: utf-8 -*-
"""
Seed de la Cohorte Cero: 50+ MaxoContratos reales para alimentar el
dashboard /admin/contracts y GET /contracts/stats.

Contenido:
- 20 contratos de aseo compartido (cohorte-aseo-NN)
- 15 contratos de prestamo sin usura (cohorte-prestamo-NN)
- 15 contratos de comida colaborativa (cohorte-comida-NN)

Cada contrato: 2 partes humanas (user-N), 2 terminos balanceados
(T17: DO y GIVE equivalentes, VHV t iguales), categoria en
maxo_contract_meta (meta_key='category'), estado active.

Además:
- 12 usuarios semilla (cohorte.N@maxocracia.local) + participantes de
  Formulario CERO con perfiles de aseo/prestamo/comida (urgencia Baja/Media
  para no escalar la escalera de protección).
- Check-ins reales con fechas variadas (tendencia temporal de γ) insertados
  con SQL directo (el API no permite backdating) y γ final adoptado por el
  participante del contrato.
- NPS de muestra (promotores/pasivos/detractores).
- Backdating de created_at/eventos con SQL directo (aceptable en seed).

Idempotente: si `cohorte-<cat>-NN` ya existe, se salta.

Uso:  .venv\\Scripts\\python.exe scripts\\seed_cohorte_cero.py [--db ruta]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

os.environ.setdefault("SECRET_KEY", "seed-cohorte-cero")

from werkzeug.security import generate_password_hash

from app import create_app
from app.jwt_utils import create_token
from app.utils import get_db

CATEGORIAS = [
    ("aseo", 20),
    ("prestamo", 15),
    ("comida", 15),
]

N_USUARIOS = 12
NOMBRES = [
    "Aurora",
    "Bruno",
    "Carmen",
    "Diego",
    "Elena",
    "Fabián",
    "Gabriela",
    "Hugo",
    "Irene",
    "Julián",
    "Karla",
    "Luis",
]

PASS = "Cohorte2026!"

# VHV por categoría: t igual para ambas partes (T17 balanceado), total < 8h
# -> sin flag de asimetría. Penalty γ pequeño (Ola 3C) dentro de [0, 0.5].
ESPECIFICACIONES = {
    "aseo": {
        "t": 1.0,
        "desc": "Rotación de aseo compartido",
        "t1": "{a} limpia la cocina compartida cada lunes durante una hora.",
        "t2": "{b} limpia el baño compartido cada viernes durante una hora.",
    },
    "prestamo": {
        "t": 1.0,
        "desc": "Préstamo sin usura",
        "t1": "{a} entrega a {b} un préstamo de cien maxos sin interés.",
        "t2": "{b} devuelve a {a} los cien maxos completos antes de treinta días.",
    },
    "comida": {
        "t": 1.5,
        "desc": "Comida colaborativa",
        "t1": "{a} cocina la cena colaborativa para cuatro personas los sábados.",
        "t2": "{b} compra los ingredientes y lava la vajilla de la cena.",
    },
}

# Semanas de despliegue: 0..7 semanas atrás (ventana de 8 semanas del stats)
SEMANAS = [7, 6, 5, 4, 3, 2, 1, 0]


def _ts(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _now():
    return datetime.now()


def crear_usuarios(db):
    """Crea los 12 usuarios semilla (idempotente por email) y devuelve {n: id}."""
    ids = {}
    for n in range(1, N_USUARIOS + 1):
        email = f"cohorte.{n}@maxocracia.local"
        db.execute(
            "INSERT OR IGNORE INTO users (email, name, alias, password_hash, city, neighborhood, trust_level) "
            "VALUES (?, ?, ?, ?, ?, ?, 1)",
            (
                email,
                NOMBRES[n - 1],
                f"Semilla {n:02d}",
                generate_password_hash(PASS),
                "Bogotá",
                "La Perseverancia",
            ),
        )
        row = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        ids[n] = row["id"]
    db.commit()
    return ids


def crear_participantes_cero(db, ids):
    """Registra los participantes de Formulario CERO con perfiles rotativos.

    Urgencia Baja/Media a propósito: una necesidad activa con urgencia 'Alta'
    escalaría la escalera de protección a 'assisted' (paráfrasis + oráculo).
    """
    perfiles = [
        ("aseo", "Tiempo para aseo comunitario", "Apoyo con aseo compartido"),
        ("prestamo", "Tiempo y recursos", "Préstamo sin usura entre vecinos"),
        ("comida", "Cocina y tiempo", "Comida colaborativa"),
    ]
    insertados = 0
    for n, uid in ids.items():
        cat, offer, need = perfiles[(n - 1) % 3]
        db.execute(
            "INSERT OR IGNORE INTO participants "
            "(name, email, city, neighborhood, offer_description, need_description, "
            " need_urgency, offer_categories, need_categories, consent_given, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'active')",
            (
                NOMBRES[n - 1],
                f"cohorte.{n}@maxocracia.local",
                "Bogotá",
                "La Perseverancia",
                offer,
                need,
                "Baja" if n % 2 else "Media",
                json.dumps([cat, "tiempo"]),
                json.dumps([cat]),
            ),
        )
        insertados += 1
    db.commit()
    return insertados


def headers(uid):
    token = create_token({"user_id": uid})
    return {"Authorization": f"Bearer {token}"}


def post(client, path, uid, payload, esperado=(200, 201)):
    res = client.post(path, headers=headers(uid), json=payload)
    if res.status_code not in esperado:
        cuerpo = res.get_json(silent=True) or res.data[:300].decode("utf-8", "replace")
        raise RuntimeError(
            f"POST {path} -> {res.status_code} esperado {esperado}: {json.dumps(cuerpo, ensure_ascii=False)[:500]}"
        )
    return res.get_json(silent=True) or {}


def _aceptar_terminos(client, cid, ua, ub):
    """Ambas partes firman ambos términos (el AVA exige aceptación de todos)."""
    for term in (f"{cid}-t1", f"{cid}-t2"):
        post(client, f"/contracts/{cid}/accept", ua, {"term_id": term, "user_id": ua})
        post(client, f"/contracts/{cid}/accept", ub, {"term_id": term, "user_id": ub})


def crear_contrato(client, db, cat, idx, ids, planificacion):
    """Crea, acepta, activa y categoriza un contrato de la cohorte.

    Devuelve (contrato_id, user_a, user_b, plan_ts) o None si ya existía.
    """
    cid = f"cohorte-{cat}-{idx:02d}"
    fila = db.execute(
        "SELECT state FROM maxo_contracts WHERE contract_id = ?", (cid,)
    ).fetchone()
    if fila:
        if fila["state"] == "active":
            return None
        # Reparación idempotente: un contrato pendiente de una ejecución
        # anterior se completa (ambas partes firman ambos términos).
        spec = ESPECIFICACIONES[cat]
        a = 1 + ((idx - 1) % N_USUARIOS)
        b = 1 + ((idx + 3) % N_USUARIOS)
        if a == b:
            b = 1 + ((idx + 5) % N_USUARIOS)
        ua, ub = ids[a], ids[b]
        _aceptar_terminos(client, cid, ua, ub)
        post(client, f"/contracts/{cid}/activate", ua, {})
        offset_dias = SEMANAS[(idx - 1) % len(SEMANAS)] * 7 + (idx % 3)
        planificacion[cid] = (_now() - timedelta(days=offset_dias), a, b)
        return "reparado"

    spec = ESPECIFICACIONES[cat]
    a = 1 + ((idx - 1) % N_USUARIOS)
    b = 1 + ((idx + 3) % N_USUARIOS)
    if a == b:
        b = 1 + ((idx + 5) % N_USUARIOS)
    ua, ub = ids[a], ids[b]

    t = spec["t"]
    creador = ua
    payload = {
        "contract_id": cid,
        "civil_description": f"{spec['desc']} entre {NOMBRES[a - 1]} y {NOMBRES[b - 1]}",
        "participants": [
            {"user_id": ua, "wellness": 1.1},
            {"user_id": ub, "wellness": 1.1},
        ],
        "terms": [
            {
                "term_id": f"{cid}-t1",
                "civil_text": spec["t1"].format(a=NOMBRES[a - 1], b=NOMBRES[b - 1]),
                "vhv": {"t": t, "v": 0, "h": 0},
                "assigned_participant_id": f"user-{ua}",
                "penalty_gamma": 0.05,
            },
            {
                "term_id": f"{cid}-t2",
                "civil_text": spec["t2"].format(a=NOMBRES[a - 1], b=NOMBRES[b - 1]),
                "vhv": {"t": t, "v": 0, "h": 0},
                "assigned_participant_id": f"user-{ub}",
                "penalty_gamma": 0.05,
            },
        ],
    }
    post(client, "/contracts/", creador, payload, esperado=(201,))
    _aceptar_terminos(client, cid, ua, ub)
    post(client, f"/contracts/{cid}/activate", creador, {})
    post(client, f"/contracts/{cid}/meta", creador, {"key": "category", "value": cat})

    # Fecha planificada de creación: rampa de 8 semanas (tendencias)
    offset_dias = SEMANAS[(idx - 1) % len(SEMANAS)] * 7 + (idx % 3)
    creado_en = _now() - timedelta(days=offset_dias)
    planificacion[cid] = (creado_en, a, b)
    return cid, ua, ub, creado_en


def insertar_checkins(db, cid, ua, ub, creado_en, idx):
    """3 check-ins por parte con fechas variadas (SQL directo: backdating).

    El último latido es el γ real adoptado por maxo_contract_participants.
    Cada 4º contrato muestra una caída (el dolor no espera); cada 10º termina
    bajo 1.0 (alerta INV1 realista del dashboard).
    """
    offsets = [
        (idx % 4 == 0, [1.18, 0.92, 1.08], [1.10, 1.02, 1.12]),  # caída + recuperación
        (idx % 10 == 0, [1.10, 0.98, 0.95], [1.05, 1.00, 1.06]),  # final bajo 1.0
    ]
    caida, serie_a, serie_b = next(
        (o for o in offsets if o[0]), (False, [1.05, 1.10, 1.16], [1.02, 1.08, 1.12])
    )
    ahora = _now()
    offset_dias = max(0, (ahora - creado_en).days)
    for n, (pid, serie, otro_uid) in enumerate(
        ((f"user-{ua}", serie_a, ub), (f"user-{ub}", serie_b, ua))
    ):
        for j, wellness in enumerate(serie):
            # días atrás desde hoy: escalonado, en el pasado y tras la creación
            # (j=0 es el latido más antiguo; serie en orden cronológico)
            dias_atras = min(1 + (idx % 5) + n * 6 + (2 - j) * 5, offset_dias)
            ts = _ts(ahora - timedelta(days=dias_atras))
            db.execute(
                "INSERT INTO maxo_contract_checkins "
                "(contract_id, participant_id, wellness, source, reported_by, created_at) "
                "VALUES (?, ?, ?, 'checkin', ?, ?)",
                (cid, pid, wellness, f"user-{otro_uid}", ts),
            )
        ultimo = serie[-1]
        ts_ultimo = _ts(ahora - timedelta(days=min(1 + (idx % 5) + n * 6, offset_dias)))
        db.execute(
            "UPDATE maxo_contract_participants SET wellness_value = ?, reported_by = ?, reported_at = ? "
            "WHERE contract_id = ? AND participant_id = ?",
            (ultimo, f"user-{otro_uid}", ts_ultimo, cid, pid),
        )
    db.commit()


def insertar_nps(client, db, cid, ua, ub, idx):
    """NPS de muestra: cada 2º contrato responde la parte A y cada 3º la B."""
    puntajes_a = [9, 9, 8, 9, 7, 6]
    puntajes_b = [10, 8, 9, 10, 9, 7]
    if idx % 2 == 0:
        post(
            client,
            f"/contracts/{cid}/nps",
            ua,
            {
                "participant_id": f"user-{ua}",
                "score": puntajes_a[idx % 6],
                "comment": "La rotación fluyó sin fricción",
            },
        )
    if idx % 3 == 0:
        post(
            client,
            f"/contracts/{cid}/nps",
            ub,
            {"participant_id": f"user-{ub}", "score": puntajes_b[idx % 6]},
        )


def backdatar(client, planificacion):
    """Reescribe created_at de contratos y eventos (SQL directo) para que el
    dashboard muestre una rampa temporal real de la cohorte.

    Además inserta los eventos de activación (state_changed -> ACTIVE) que el
    sync de eventos de _save_contract descarta cuando el log en memoria es más
    corto que el histórico persistido (carga sin bitácora): el trends del
    dashboard se alimenta de esos eventos.
    """
    with client.application.app_context():
        db = get_db()
        for cid, (creado_en, creador, _) in planificacion.items():
            base = creado_en
            db.execute(
                "UPDATE maxo_contracts SET created_at = ?, updated_at = ? WHERE contract_id = ?",
                (_ts(base), _ts(base), cid),
            )
            eventos = db.execute(
                "SELECT id, event_type, metadata_json FROM maxo_contract_events WHERE contract_id = ?",
                (cid,),
            ).fetchall()
            hay_activacion = False
            for ev in eventos:
                et = ev["event_type"]
                if et == "contract_created":
                    ts = base + timedelta(hours=0)
                elif et in ("participant_added", "term_added"):
                    ts = base + timedelta(hours=1)
                elif et in ("term_accept_signed", "term_accepted"):
                    ts = base + timedelta(hours=12)
                elif et == "state_changed":
                    meta = json.loads(ev["metadata_json"] or "{}")
                    destino = meta.get("to")
                    if destino == "ACTIVE":
                        hay_activacion = True
                    ts = base + timedelta(hours=24 if destino == "ACTIVE" else 12)
                elif et == "contract_activated":
                    ts = base + timedelta(hours=24)
                    hay_activacion = True
                elif et == "checkin_reported":
                    ts = base + timedelta(hours=30)
                else:
                    ts = base + timedelta(hours=6)
                db.execute(
                    "UPDATE maxo_contract_events SET created_at = ? WHERE id = ?",
                    (_ts(ts), ev["id"]),
                )
            if not hay_activacion:
                ts = base + timedelta(hours=24)
                db.execute(
                    "INSERT INTO maxo_contract_events (contract_id, event_type, description, metadata_json, created_at) "
                    "VALUES (?, 'state_changed', 'Activación del contrato', ?, ?)",
                    (
                        cid,
                        json.dumps(
                            {
                                "actor_id": f"user-{creador}",
                                "from": "PENDING",
                                "to": "ACTIVE",
                            }
                        ),
                        _ts(ts),
                    ),
                )
            db.execute(
                "UPDATE maxo_contract_participants SET created_at = ? WHERE contract_id = ?",
                (_ts(base), cid),
            )
        db.commit()


def main():
    parser = argparse.ArgumentParser(description="Seed Cohorte Cero (50+ contratos)")
    parser.add_argument("--db", default=None, help="Ruta a la BD (default: comun.db)")
    args = parser.parse_args()

    app = create_app(db_path=args.db)
    client = app.test_client()

    with app.app_context():
        db = get_db()

        print("== Seed Cohorte Cero ==")
        ids = crear_usuarios(db)
        print(f"Usuarios semilla: {len(ids)} (emails cohorte.N@maxocracia.local)")
        print(f"Participantes Formulario CERO: {crear_participantes_cero(db, ids)}")

        planificacion = {}
        resumen = {
            cat: {"creados": 0, "omitidos": 0, "reparados": 0} for cat, _ in CATEGORIAS
        }
        total_checkins = 0
        for cat, cantidad in CATEGORIAS:
            for idx in range(1, cantidad + 1):
                creado = crear_contrato(client, db, cat, idx, ids, planificacion)
                if creado is None:
                    resumen[cat]["omitidos"] += 1
                    continue
                if creado == "reparado":
                    resumen[cat]["reparados"] += 1
                    continue
                cid, ua, ub, creado_en = creado
                resumen[cat]["creados"] += 1
                insertar_checkins(db, cid, ua, ub, creado_en, idx)
                total_checkins += 6
                insertar_nps(client, db, cid, ua, ub, idx)

        # Conciliar contratos ya existentes: backdatar también debe corregir
        # e insertar sus eventos de activación (idempotente en re-ejecuciones).
        filas = db.execute(
            "SELECT contract_id, created_at, creator_user_id FROM maxo_contracts "
            "WHERE contract_id LIKE 'cohorte-%'"
        ).fetchall()
        for fila in filas:
            cid = fila["contract_id"]
            if cid in planificacion:
                continue
            try:
                creado_en = datetime.strptime(fila["created_at"], "%Y-%m-%d %H:%M:%S")
            except (TypeError, ValueError):
                creado_en = _now()
            planificacion[cid] = (creado_en, fila["creator_user_id"] or 1, None)

        backdatar(client, planificacion)

        # Autocompletar categoría: todo contrato cohorte-<cat>-NN debe tener
        # su meta 'category' (cubre reparaciones de ejecuciones anteriores).
        for cat, _ in CATEGORIAS:
            db.execute(
                "INSERT OR IGNORE INTO maxo_contract_meta (contract_id, meta_key, meta_value) "
                "SELECT contract_id, 'category', ? FROM maxo_contracts "
                "WHERE contract_id LIKE 'cohorte-' || ? || '-%'",
                (cat, cat),
            )
        db.commit()

        total_creados = sum(r["creados"] for r in resumen.values())
        total_omitidos = sum(r["omitidos"] for r in resumen.values())

        contratos_db = db.execute(
            "SELECT COUNT(*) FROM maxo_contracts WHERE contract_id LIKE 'cohorte-%'"
        ).fetchone()[0]
        checkins_db = db.execute(
            "SELECT COUNT(*) FROM maxo_contract_checkins WHERE contract_id LIKE 'cohorte-%'"
        ).fetchone()[0]
        nps_db = db.execute(
            "SELECT COUNT(*) FROM maxo_contract_nps WHERE contract_id LIKE 'cohorte-%'"
        ).fetchone()[0]
        activos_db = db.execute(
            "SELECT COUNT(*) FROM maxo_contracts WHERE contract_id LIKE 'cohorte-%' AND state = 'active'"
        ).fetchone()[0]

        print()
        print("== Resumen por categoría ==")
        for cat, _ in CATEGORIAS:
            fila = db.execute(
                "SELECT COUNT(*) FROM maxo_contract_meta WHERE meta_key = 'category' AND meta_value = ?",
                (cat,),
            ).fetchone()[0]
            print(
                f"  {cat:9s}: creados={resumen[cat]['creados']:2d}  omitidos={resumen[cat]['omitidos']:2d}  reparados={resumen[cat]['reparados']:2d}  (en meta={fila})"
            )
        print()
        print(
            f"Contratos creados en esta ejecución: {total_creados}  (omitidos por idempotencia: {total_omitidos})"
        )
        print(f"Contratos cohorte en BD: {contratos_db}  (activos: {activos_db})")
        print(f"Check-ins insertados: {total_checkins}  (en BD cohorte: {checkins_db})")
        print(f"NPS registrados: {nps_db}")


if __name__ == "__main__":
    main()

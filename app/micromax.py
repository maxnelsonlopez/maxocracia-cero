import json
import math
import random
import sqlite3
import string
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional


def _ensure_column(cur, table: str, ddl: str):
    """Adds a column if it does not exist yet (idempotent migration for existing DBs)."""
    try:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {ddl}")
    except sqlite3.OperationalError:
        pass  # column already exists


def init_micromax_tables(app):
    """
    Initializes MicroMaxocracia tables in SQLite.
    Called on app startup.
    """
    db_path = app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        # 1. Households
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS micromax_households (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                invite_code TEXT UNIQUE NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # 2. Members
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS micromax_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id INTEGER NOT NULL,
                user_id INTEGER UNIQUE,
                name TEXT NOT NULL,
                monthly_income REAL DEFAULT 0,
                work_hours REAL DEFAULT 0,
                travel_hours REAL DEFAULT 0,
                sleep_hours REAL DEFAULT 56,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (household_id) REFERENCES micromax_households(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """
        )

        # 3. CDD Logs (Domestic Direct Contributions)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS micromax_cdd_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                task_name TEXT NOT NULL,
                duration_hours REAL NOT NULL,
                effort_factor REAL NOT NULL,
                mental_factor REAL NOT NULL,
                scope_factor REAL NOT NULL,
                attention_factor REAL DEFAULT 1.0,
                fragmentation_factor REAL DEFAULT 1.0,
                loneliness_factor REAL DEFAULT 1.0,
                calculated_vhv REAL NOT NULL,
                logged_date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (member_id) REFERENCES micromax_members(id) ON DELETE CASCADE
            )
        """
        )

        # 4. Safety Surveys (ESI Checklist)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS micromax_safety_surveys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL UNIQUE,
                score INTEGER NOT NULL,
                answers_json TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (member_id) REFERENCES micromax_members(id) ON DELETE CASCADE
            )
        """
        )

        # 5. Audits
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS micromax_audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id INTEGER NOT NULL,
                audit_date TEXT NOT NULL,
                conflicts_count INTEGER NOT NULL,
                weapon_count INTEGER NOT NULL,
                accusations_count INTEGER NOT NULL,
                threats_count INTEGER NOT NULL,
                s1_hours REAL DEFAULT 0,
                s2_score REAL DEFAULT 0,
                s3_score REAL DEFAULT 0,
                s4_score REAL DEFAULT 0,
                s5_score REAL DEFAULT 0,
                duration_weeks INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (household_id) REFERENCES micromax_households(id) ON DELETE CASCADE
            )
        """
        )

        # Indices
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_micromax_members_household ON micromax_members(household_id)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_micromax_cdd_member ON micromax_cdd_logs(member_id)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_micromax_cdd_date ON micromax_cdd_logs(logged_date)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_micromax_audits_household ON micromax_audits(household_id)"
        )

        # Migracion canonica (Cap. 16.5): vector VHV [T,V,R] opcional en CDD y
        # CEH por TVI vendido en la configuracion del miembro. Idempotente.
        _ensure_column(cur, "micromax_cdd_logs", "v_ucv REAL DEFAULT 0")
        _ensure_column(cur, "micromax_cdd_logs", "r_units REAL DEFAULT 0")
        _ensure_column(cur, "micromax_cdd_logs", "r_notes TEXT DEFAULT ''")
        _ensure_column(cur, "micromax_members", "ceh_mode TEXT DEFAULT 'bridge'")
        _ensure_column(cur, "micromax_members", "hourly_rate REAL DEFAULT 0")

        # 6. Check-ins de gamma domestica (Cap. 16.5 s16.5.6 - INV1-Hogar):
        #    el latido del hogar. Politica asimetrica del Puente A aplicada al fractal.
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS micromax_checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                gamma REAL NOT NULL,
                note TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (member_id) REFERENCES micromax_members(id) ON DELETE CASCADE
            )
        """
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_micromax_checkins_member ON micromax_checkins(member_id)"
        )

        conn.commit()
    except Exception as e:
        app.logger.error(f"Error initializing MicroMaxocracia tables: {e}")
    finally:
        conn.close()


class MicroMaxManager:
    """
    Manager class to handle MicroMaxocracia operations using SQLite database.
    """

    def _get_db_connection(self):
        from .utils import get_db

        return get_db()

    def create_household(self, name: str) -> Dict:
        """Creates a new household and generates a unique 6-character invite code."""
        if not name or not name.strip():
            raise ValueError("Household name cannot be empty.")

        conn = self._get_db_connection()
        cursor = conn.cursor()

        # Generate unique invite code
        invite_code = ""
        for _ in range(10):  # Try 10 times to avoid collision
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            cursor.execute(
                "SELECT 1 FROM micromax_households WHERE invite_code = ?", (code,)
            )
            if not cursor.fetchone():
                invite_code = code
                break

        if not invite_code:
            raise ValueError("Failed to generate a unique invite code. Try again.")

        cursor.execute(
            "INSERT INTO micromax_households (name, invite_code) VALUES (?, ?)",
            (name.strip(), invite_code),
        )
        household_id = cursor.lastrowid
        conn.commit()

        return {"id": household_id, "name": name.strip(), "invite_code": invite_code}

    def join_household(self, invite_code: str, user_id: int, user_name: str) -> Dict:
        """Joins an existing household using an invite code."""
        if not invite_code:
            raise ValueError("Invite code is required.")

        conn = self._get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, invite_code FROM micromax_households WHERE invite_code = ?",
            (invite_code.strip().upper(),),
        )
        household = cursor.fetchone()
        if not household:
            raise ValueError("Invalid invite code. Household not found.")

        household_id = household["id"]

        # Join as member
        cursor.execute(
            """
            INSERT INTO micromax_members (household_id, user_id, name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET household_id = excluded.household_id, name = excluded.name
        """,
            (household_id, user_id, user_name),
        )
        conn.commit()

        # Get member profile
        cursor.execute("SELECT * FROM micromax_members WHERE user_id = ?", (user_id,))
        member = cursor.fetchone()

        return {"household": dict(household), "member": dict(member)}

    def get_member(self, user_id: int) -> Optional[Dict]:
        """Gets member profile by user ID."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM micromax_members WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_household_members(self, household_id: int) -> List[Dict]:
        """Gets all members in a household."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM micromax_members WHERE household_id = ?", (household_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def _get_shielded_member_ids(self, household_id: int) -> set:
        """Modo Escudo Domestico (Cap. 16.5): ids de miembros con ESI en rojo (score >= 3).

        Sus cifras se ocultan a los DEMAS miembros del hogar; ella siempre ve las suyas
        y las del hogar completo. El registro propio nunca se bloquea ni se borra.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT m.id FROM micromax_members m
            JOIN micromax_safety_surveys s ON s.member_id = m.id
            WHERE m.household_id = ? AND s.score >= 3
            """,
            (household_id,),
        )
        return {row["id"] for row in cursor.fetchall()}

    def update_member_config(
        self,
        user_id: int,
        monthly_income: float,
        work_hours: float,
        travel_hours: float,
        sleep_hours: float,
        ceh_mode: str = "bridge",
        hourly_rate: float = 0.0,
    ) -> Dict:
        """Updates work/life economic configuration for a household member.

        Cap. 16.5: `ceh_mode` ('bridge' = % fiat, 'canonical' = TVI vendido) y
        `hourly_rate` (tarifa horaria vital declarada) habilitan la contabilidad
        canonica cuando todo el hogar la adopta.
        """
        if monthly_income < 0 or work_hours < 0 or travel_hours < 0 or sleep_hours < 0:
            raise ValueError("Parameters cannot be negative.")
        if hourly_rate < 0:
            raise ValueError("Hourly rate cannot be negative.")
        if ceh_mode not in ("bridge", "canonical"):
            raise ValueError("ceh_mode must be 'bridge' or 'canonical'.")
        if (work_hours + travel_hours + sleep_hours) > 168:
            raise ValueError(
                "Total hours (work + travel + sleep) cannot exceed 168 hours in a week."
            )

        conn = self._get_db_connection()
        cursor = conn.cursor()

        # Verify user is a member
        member = self.get_member(user_id)
        if not member:
            raise ValueError("User is not a member of any MicroMaxocracia household.")

        cursor.execute(
            """
            UPDATE micromax_members
            SET monthly_income = ?, work_hours = ?, travel_hours = ?, sleep_hours = ?,
                ceh_mode = ?, hourly_rate = ?
            WHERE user_id = ?
        """,
            (
                monthly_income,
                work_hours,
                travel_hours,
                sleep_hours,
                ceh_mode,
                hourly_rate,
                user_id,
            ),
        )
        conn.commit()

        return self.get_member(user_id)

    def log_cdd(
        self,
        user_id: int,
        task_name: str,
        duration_hours: float,
        effort_factor: float,
        mental_factor: float,
        scope_factor: float,
        attention_factor: float = 1.0,
        fragmentation_factor: float = 1.0,
        loneliness_factor: float = 1.0,
        logged_date: Optional[str] = None,
        v_ucv: float = 0.0,
        r_units: float = 0.0,
        r_notes: str = "",
    ) -> Dict:
        """Logs a direct contribution (CDD) task with VHV & FIC calculation.

        Cap. 16.5 (compatibilidad canonica): `v_ucv` (vidas afectadas, ej. cuidado de
        personas) y `r_units`/`r_notes` (recursos del hogar) completan el vector
        [T, V, R] junto a `duration_hours` (T). El escalar ponderado sigue calculandose
        igual para el equilibrio — el hecho queda limpio y comparable con el sistema general.
        `r_units` NEGATIVO = credito regenerativo (EVV 1.2 s4.3): cuidado ecosistemico
        que devuelve mas de lo que toma (s16.5.14, Reino Natural como conviviente).
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if duration_hours <= 0 or duration_hours > 24:
            raise ValueError("Task duration must be between 0 and 24 hours.")
        if v_ucv < 0:
            raise ValueError("V component (lives affected) cannot be negative.")
        # Cap. 16.5 s16.5.14 / EVV 1.2 s4.3: r_units NEGATIVO = credito regenerativo
        # (devolver mas de lo tomado: arboladas, humedales, suelos). V no puede ser
        # negativo: una vida afectada no se des-afecta en la misma cuenta.

        # Ponderation boundaries check
        if not (1.0 <= effort_factor <= 2.0):
            raise ValueError("Effort factor must be between 1.0 and 2.0")
        if not (1.0 <= mental_factor <= 1.5):
            raise ValueError("Mental load factor must be between 1.0 and 1.5")
        if not (1.0 <= scope_factor <= 2.0):
            raise ValueError("Scope factor must be between 1.0 and 2.0")
        if not (1.0 <= attention_factor <= 2.0):
            raise ValueError("Attention factor must be between 1.0 and 2.0")
        if not (1.0 <= fragmentation_factor <= 1.8):
            raise ValueError("Fragmentation factor must be between 1.0 and 1.8")
        if not (1.0 <= loneliness_factor <= 1.5):
            raise ValueError("Loneliness factor must be between 1.0 and 1.5")

        conn = self._get_db_connection()
        cursor = conn.cursor()

        member = self.get_member(user_id)
        if not member:
            raise ValueError("User is not registered in a MicroMaxocracia household.")

        # Modo Escudo Domestico (Cap. 16.5): una encuesta ESI en rojo JAMAS bloquea
        # el registro propio. Hacer visible el trabajo invisible es mas necesario
        # en riesgo, no menos. Lo que el escudo modula es la exposicion (las cifras
        # de quien esta protegida se ocultan a los demas miembros), nunca la voz.

        # Formula VHV calculation
        vhi_base = effort_factor * mental_factor * scope_factor
        fic = attention_factor * fragmentation_factor * loneliness_factor
        calculated_vhv = round(duration_hours * vhi_base * fic, 4)

        if not logged_date:
            logged_date = datetime.now(timezone.utc).date().isoformat()

        cursor.execute(
            """
            INSERT INTO micromax_cdd_logs (
                member_id, task_name, duration_hours, effort_factor, mental_factor, scope_factor,
                attention_factor, fragmentation_factor, loneliness_factor, calculated_vhv,
                logged_date, v_ucv, r_units, r_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                member["id"],
                task_name.strip(),
                duration_hours,
                effort_factor,
                mental_factor,
                scope_factor,
                attention_factor,
                fragmentation_factor,
                loneliness_factor,
                calculated_vhv,
                logged_date,
                v_ucv,
                r_units,
                (r_notes or "").strip(),
            ),
        )
        log_id = cursor.lastrowid
        conn.commit()

        return {
            "id": log_id,
            "member_id": member["id"],
            "task_name": task_name.strip(),
            "duration_hours": duration_hours,
            "calculated_vhv": calculated_vhv,
            "logged_date": logged_date,
            "vhv_vector": {"T": duration_hours, "V": v_ucv, "R": r_units},
            "r_notes": (r_notes or "").strip(),
        }

    def get_cdd_logs(
        self, user_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict]:
        """Lists logged CDD tasks for the current member."""
        member = self.get_member(user_id)
        if not member:
            return []

        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM micromax_cdd_logs
            WHERE member_id = ?
            ORDER BY logged_date DESC, id DESC
            LIMIT ? OFFSET ?
        """,
            (member["id"], limit, offset),
        )
        return [dict(row) for row in cursor.fetchall()]

    def save_safety_survey(
        self, user_id: int, answers: Dict[str, bool], wants_support: Optional[bool] = None
    ) -> Dict:
        """Saves ESI safety survey, counts score and activates Modo Escudo when red.

        Cap. 16.5: el rojo ya no bloquea el registro propio (Derecho al Registro
        Protegido). `wants_support` es un opt-in PRIVADO de la persona para que la
        Red de Apoyo pueda ofrecerle acompanamiento/asesoria/recursos; jamas se
        expone al resto del hogar.
        """
        if len(answers) != 6:
            raise ValueError("ESI Safety survey must contain exactly 6 questions.")

        member = self.get_member(user_id)
        if not member:
            raise ValueError("User is not registered in a MicroMaxocracia household.")

        # Count true answers (only the 6 questions count toward the score)
        score = sum(1 for v in answers.values() if v is True)

        payload = dict(answers)
        if wants_support is not None:
            payload["_wants_support"] = bool(wants_support)
        answers_str = json.dumps(payload)

        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO micromax_safety_surveys (member_id, score, answers_json)
            VALUES (?, ?, ?)
            ON CONFLICT(member_id) DO UPDATE SET score = excluded.score, answers_json = excluded.answers_json
        """,
            (member["id"], score, answers_str),
        )
        conn.commit()

        return {
            "member_id": member["id"],
            "score": score,
            "answers": answers,
            "wants_support": bool(wants_support) if wants_support is not None else False,
            "protection_mode": "shielded" if score >= 3 else "standard",
            "blocked": False,
            "can_log": True,
        }

    def get_safety_survey(self, user_id: int) -> Optional[Dict]:
        """Gets ESI survey for a member (self-view only)."""
        member = self.get_member(user_id)
        if not member:
            return None

        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM micromax_safety_surveys WHERE member_id = ?", (member["id"],)
        )
        row = cursor.fetchone()
        if not row:
            return None

        payload = json.loads(row["answers_json"])
        wants_support = bool(payload.pop("_wants_support", False))

        return {
            "id": row["id"],
            "member_id": row["member_id"],
            "score": row["score"],
            "answers": payload,
            "wants_support": wants_support,
            "protection_mode": "shielded" if row["score"] >= 3 else "standard",
            "created_at": row["created_at"],
        }

    def log_audit(
        self,
        user_id: int,
        audit_date: str,
        conflicts_count: int,
        weapon_count: int,
        accusations_count: int,
        threats_count: int,
        s1_hours: float = 0,
        s2_score: float = 0,
        s3_score: float = 0,
        s4_score: float = 0,
        s5_score: float = 0,
        duration_weeks: int = 4,
    ) -> Dict:
        """Logs a household audit session."""
        member = self.get_member(user_id)
        if not member:
            raise ValueError("User is not registered in a MicroMaxocracia household.")

        if duration_weeks <= 0:
            raise ValueError("Audit duration must be at least 1 week.")

        conn = self._get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO micromax_audits (
                household_id, audit_date, conflicts_count, weapon_count, accusations_count, threats_count,
                s1_hours, s2_score, s3_score, s4_score, s5_score, duration_weeks
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                member["household_id"],
                audit_date,
                conflicts_count,
                weapon_count,
                accusations_count,
                threats_count,
                s1_hours,
                s2_score,
                s3_score,
                s4_score,
                s5_score,
                duration_weeks,
            ),
        )
        audit_id = cursor.lastrowid
        conn.commit()

        return {
            "id": audit_id,
            "household_id": member["household_id"],
            "audit_date": audit_date,
            "conflicts_count": conflicts_count,
        }

    def get_audits(self, user_id: int) -> List[Dict]:
        """Gets all logged audits for the member's household."""
        member = self.get_member(user_id)
        if not member:
            return []

        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM micromax_audits
            WHERE household_id = ?
            ORDER BY audit_date DESC, id DESC
        """,
            (member["household_id"],),
        )
        return [dict(row) for row in cursor.fetchall()]

    def calculate_three_accounts(
        self,
        household_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        requester_user_id: Optional[int] = None,
    ) -> Dict:
        """Calculates CDD, CEH, TED, and Equilibrium values for members in a household.

        Modo Escudo (Cap. 16.5): las cifras de un miembro con ESI en rojo se ocultan a
        los DEMAS miembros (sus valores salen de los totales y de las cuotas para que
        nada sea inferible). Ella misma siempre ve el hogar completo, incluidas sus
        propias cifras.
        """
        members = self.get_household_members(household_id)
        if not members:
            return {"members": [], "totals": {}}

        conn = self._get_db_connection()
        cursor = conn.cursor()

        shielded_ids = self._get_shielded_member_ids(household_id)

        requester_member_id = None
        if requester_user_id is not None:
            for m in members:
                if m["user_id"] == requester_user_id:
                    requester_member_id = m["id"]
                    break

        def _visible(member_id: int) -> bool:
            return member_id not in shielded_ids or member_id == requester_member_id

        # Fetch CDD sums
        member_cdds = {}
        for m in members:
            query = "SELECT SUM(calculated_vhv) as vhv_sum FROM micromax_cdd_logs WHERE member_id = ?"
            params = [m["id"]]
            if start_date:
                query += " AND logged_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND logged_date <= ?"
                params.append(end_date)

            cursor.execute(query, tuple(params))
            row = cursor.fetchone()
            member_cdds[m["id"]] = row["vhv_sum"] if row["vhv_sum"] is not None else 0.0

        # TED: 168 - work - travel - sleep (fallback sleep 56)
        member_teds = {}
        for m in members:
            ted = (
                168.0 - m["work_hours"] - m["travel_hours"] - (m["sleep_hours"] or 56.0)
            )
            member_teds[m["id"]] = max(ted, 0.0)  # Cannot have negative energy

        # Totals computed ONLY over visible members (nothing inferable by difference)
        visible_members = [m for m in members if _visible(m["id"])]
        total_cdd = sum(member_cdds[m["id"]] for m in visible_members)
        total_income = sum(m["monthly_income"] or 0 for m in visible_members)
        total_ted = sum(member_teds[m["id"]] for m in visible_members)

        # CEH canonica (Cap. 16.5): TVI vendido cuando TODOS los miembros con ingresos
        # usan modo canonical con tarifa horaria vital declarada; si no, fallback fiat.
        def _member_mode(m):
            return m.get("ceh_mode") or "bridge"

        contributing = [m for m in visible_members if (m.get("monthly_income") or 0) > 0]
        ceh_unit = (
            "tvi"
            if contributing
            and all(
                _member_mode(m) == "canonical"
                and (m.get("hourly_rate") or 0) > 0
                for m in contributing
            )
            else "fiat"
        )

        def _ceh_value(m) -> float:
            income = m.get("monthly_income") or 0.0
            if ceh_unit == "tvi":
                return income / (m.get("hourly_rate") or 0.0)
            return float(income)

        total_ceh = sum(_ceh_value(m) for m in visible_members)

        # Ponderations (p1/p2/p3 en la rama canonica Cap. 16.5; alias historicos aqui)
        p1, p2, p3 = 0.6, 0.3, 0.1

        member_results = []
        for m in members:
            if not _visible(m["id"]):
                member_results.append(
                    {
                        "id": m["id"],
                        "name": m["name"],
                        "user_id": m["user_id"],
                        "cdd": None,
                        "cdd_share": None,
                        "income": None,
                        "ceh_share": None,
                        "ted": None,
                        "ted_share": None,
                        "equilibrio": None,
                        "protegido": True,
                    }
                )
                continue

            cdd = member_cdds[m["id"]]
            income = m.get("monthly_income") or 0.0
            ted = member_teds[m["id"]]

            cdd_share = cdd / total_cdd if total_cdd > 0 else 0.0
            ceh_value = _ceh_value(m)
            ceh_share = ceh_value / total_ceh if total_ceh > 0 else 0.0
            ted_share = ted / total_ted if total_ted > 0 else 0.0

            equilibrio = (p1 * cdd_share) + (p2 * ceh_share) + (p3 * ted_share)

            member_results.append(
                {
                    "id": m["id"],
                    "name": m["name"],
                    "user_id": m["user_id"],
                    "cdd": round(cdd, 2),
                    "cdd_share": round(cdd_share * 100, 2),
                    "income": income,
                    "ceh_mode": _member_mode(m),
                    "ceh_value": round(ceh_value, 4),
                    "ceh_share": round(ceh_share * 100, 2),
                    "ted": round(ted, 2),
                    "ted_share": round(ted_share * 100, 2),
                    "equilibrio": round(equilibrio * 100, 2),
                    "protegido": m["id"] in shielded_ids,
                }
            )

        return {
            "members": member_results,
            "totals": {
                "total_cdd": round(total_cdd, 2),
                "total_income": total_income,
                "total_ted": round(total_ted, 2),
                "total_ceh": round(total_ceh, 4),
                "ceh_unit": ceh_unit,
            },
            "pesos": {"p1": p1, "p2": p2, "p3": p3},
        }

    def log_checkin(self, user_id: int, gamma: float, note: str = "") -> Dict:
        """Check-in de bienestar domestico (Cap. 16.5 s16.5.6).

        Canon del sistema: gamma con tope [0.5, 1.5] (blindaje Ola 3A). INV1-Hogar:
        una CAIDA bajo 1.0 se escucha siempre — la respuesta marca inv1=True para que
        la persona y el hogar la vean. Bajo Modo Escudo, el angusto de quien esta
        protegida JAMAS se emite a los demas convivientes (solo ella la ve).
        """
        if not (0.5 <= gamma <= 1.5):
            raise ValueError("Gamma must be between 0.5 and 1.5.")

        member = self.get_member(user_id)
        if not member:
            raise ValueError("User is not registered in a MicroMaxocracia household.")

        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO micromax_checkins (member_id, gamma, note) VALUES (?, ?, ?)",
            (member["id"], gamma, (note or "").strip()),
        )
        checkin_id = cursor.lastrowid
        conn.commit()

        return {
            "id": checkin_id,
            "member_id": member["id"],
            "gamma": gamma,
            "note": (note or "").strip(),
            "inv1": gamma < 1.0,
        }

    def get_checkins(self, user_id: int, limit: int = 30) -> List[Dict]:
        """Serie temporal de gamma propia."""
        member = self.get_member(user_id)
        if not member:
            return []

        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, gamma, note, created_at FROM micromax_checkins
            WHERE member_id = ?
            ORDER BY id DESC
            LIMIT ?
        """,
            (member["id"], limit),
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_household_wellbeing(
        self, household_id: int, requester_user_id: Optional[int] = None
    ) -> Dict:
        """Ultimo gamma por miembro + alerta INV1-Hogar, respetando el Modo Escudo.

        La vista de cada quien computa solo miembros visibles: el angusto de un
        protegido nunca cruza la pantalla de sus convivientes.
        """
        members = self.get_household_members(household_id)
        shielded_ids = self._get_shielded_member_ids(household_id)

        requester_member_id = None
        if requester_user_id is not None:
            for m in members:
                if m["user_id"] == requester_user_id:
                    requester_member_id = m["id"]
                    break

        def _visible(member_id: int) -> bool:
            return member_id not in shielded_ids or member_id == requester_member_id

        conn = self._get_db_connection()
        cursor = conn.cursor()

        results = []
        inv1_alert = False
        for m in members:
            cursor.execute(
                """
                SELECT gamma FROM micromax_checkins WHERE member_id = ?
                ORDER BY id DESC LIMIT 1
            """,
                (m["id"],),
            )
            row = cursor.fetchone()
            latest_gamma = row["gamma"] if row else None

            if not _visible(m["id"]):
                results.append(
                    {
                        "member_id": m["id"],
                        "name": m["name"],
                        "gamma": None,
                        "protegido": True,
                        "inv1": None,
                    }
                )
                continue

            member_inv1 = latest_gamma is not None and latest_gamma < 1.0
            if member_inv1:
                inv1_alert = True
            results.append(
                {
                    "member_id": m["id"],
                    "name": m["name"],
                    "gamma": latest_gamma,
                    "protegido": m["id"] in shielded_ids,
                    "inv1": member_inv1,
                }
            )

        return {"members": results, "inv1_hogar_alert": inv1_alert}

    def get_support_offers(self, user_id: int) -> Dict:
        """Puente Red de Apoyo (Cap. 16.5 s16.5.12) — solo con opt-in privado activo.

        Ofertas antes que busquedas: devuelve los recursos comunitarios abiertos,
        ordenados por afinidad con las senales ESI de la persona (que nunca salen
        del canal). Nada aqui revela hogar ni respuestas a terceros: es una lectura
        personal de la abundancia de la red.
        """
        member = self.get_member(user_id)
        survey = self.get_safety_survey(user_id)
        if not member or not survey or not survey.get("wants_support"):
            # Mensaje neutro: no filtra estado ni existencia de encuesta
            raise PermissionError(
                "Este canal requiere tu consentimiento de apoyo (opt-in privado en la encuesta ESI)."
            )

        answers = survey.get("answers", {})
        signal_map = {
            "q1": ["emocional", "acompanamiento"],
            "q2": ["financiero", "legal"],
            "q3": ["legal", "emergencia"],
            "q4": ["comunitario", "testigos"],
            "q5": ["acompanamiento", "comunitario"],
            "q6": ["emocional", "terapia"],
        }
        signal_categories = []
        for q, cats in signal_map.items():
            if answers.get(q) is True:
                for c in cats:
                    if c not in signal_categories:
                        signal_categories.append(c)

        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, description, category, created_at FROM resources WHERE available = 1 ORDER BY created_at DESC"
        )
        rows = [dict(r) for r in cursor.fetchall()]

        def _affinity(resource: Dict) -> List[str]:
            hay = " ".join(
                str(resource.get(k) or "") for k in ("title", "description", "category")
            ).lower()
            return [c for c in signal_categories if c in hay]

        matched, others = [], []
        for r in rows:
            reasons = _affinity(r)
            item = dict(r)
            if reasons:
                item["match_reasons"] = reasons
                matched.append(item)
            else:
                others.append(item)

        return {
            "signal_categories": signal_categories,
            "offers": matched + others,
            "note": "Ofertas antes que busquedas (Cap. 16.5 s16.5.12): reclama desde tu perfil, sin declarar necesidad publica.",
        }

    def calculate_toxicity_indices(
        self, household_id: int, requester_user_id: Optional[int] = None
    ) -> Dict:
        """Calculates relational health indices (ICE, IDB, IDP) and Detox warnings.

        Modo Escudo (Cap. 16.5): el IDP se calcula solo con las cifras visibles para
        quien consulta (las de un miembro protegido no se filtran por inferencia).
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()

        # Get audits sorted by date
        cursor.execute(
            """
            SELECT * FROM micromax_audits
            WHERE household_id = ?
            ORDER BY audit_date DESC
            LIMIT 5
        """,
            (household_id,),
        )
        audits = [dict(row) for row in cursor.fetchall()]

        if not audits:
            return {
                "ice": 0.0,
                "idb": 0.0,
                "idp": 0.0,
                "detox_triggered": False,
                "reasons": ["Sin auditorías registradas"],
                "alerts": {"ice": False, "idb": False, "idp": False},
            }

        latest_audit = audits[0]

        # 1. ICE (Índice de Conflicto Escalado)
        # ICE = (Conflictos auditoría / Baseline) * (1 + Puntos)
        baseline_conflicts = 2.0  # Assumed default pre-MicroMax baseline
        weapon_pts = latest_audit["weapon_count"] * 2.0
        accusation_pts = latest_audit["accusations_count"] * 1.0
        threats_pts = latest_audit["threats_count"] * 3.0

        factor_intensidad = 1.0 + weapon_pts + accusation_pts + threats_pts
        ice = (latest_audit["conflicts_count"] / baseline_conflicts) * factor_intensidad

        # 2. IDB (Índice de Deterioro de Bienestar)
        # IDB = Sum(w_i * S_i)
        idb = (
            2.0 * latest_audit["s1_hours"]
            + 1.5 * latest_audit["s2_score"]
            + 1.8 * latest_audit["s3_score"]
            + 2.0 * latest_audit["s4_score"]
            + 1.5 * latest_audit["s5_score"]
        )

        # 3. IDP (Índice de Desequilibrio Persistente)
        # IDP = (SD de CDD semanal / Media de CDD) * semanas
        duration_weeks = latest_audit["duration_weeks"]

        # Fetch CDD logged in this audit period
        members = self.get_household_members(household_id)

        shielded_ids = self._get_shielded_member_ids(household_id)
        requester_member_id = None
        if requester_user_id is not None:
            for m in members:
                if m["user_id"] == requester_user_id:
                    requester_member_id = m["id"]
                    break

        def _visible(member_id: int) -> bool:
            return member_id not in shielded_ids or member_id == requester_member_id

        visible_members = [m for m in members if _visible(m["id"])]

        # Find start and end date of latest audit period
        end_date = latest_audit["audit_date"]
        try:
            end_dt = datetime.fromisoformat(end_date)
            start_dt = end_dt - timedelta(weeks=duration_weeks)
            start_date = start_dt.date().isoformat()
        except ValueError:
            # Fallback if parsing failed
            start_date = None

        cdd_weekly_averages = []
        for m in visible_members:
            query = "SELECT SUM(calculated_vhv) as vhv_sum FROM micromax_cdd_logs WHERE member_id = ?"
            params = [m["id"]]
            if start_date:
                query += " AND logged_date >= ? AND logged_date <= ?"
                params.extend([start_date, end_date])
            cursor.execute(query, tuple(params))
            row = cursor.fetchone()
            total_cdd = row["vhv_sum"] if row["vhv_sum"] is not None else 0.0
            cdd_weekly_averages.append(total_cdd / duration_weeks)

        mean_cdd = (
            sum(cdd_weekly_averages) / len(cdd_weekly_averages)
            if cdd_weekly_averages
            else 0.0
        )

        # Sample standard deviation
        def sample_std(values, mean):
            n = len(values)
            if n <= 1 or mean == 0.0:
                return 0.0
            variance = sum((x - mean) ** 2 for x in values) / (n - 1)
            return math.sqrt(variance)

        std_cdd = sample_std(cdd_weekly_averages, mean_cdd)
        idp = (std_cdd / mean_cdd) * duration_weeks if mean_cdd > 0 else 0.0

        # Detox Protocol conditions
        ice_alert = ice >= 3.0
        idb_alert = idb >= 5.0
        idp_alert = idp >= 0.4 and duration_weeks >= 8
        # Make idp_alert default to true if IDP is just structurally high for any audit duration
        if idp >= 0.5:
            idp_alert = True

        alert_count = sum([1 if x else 0 for x in [ice_alert, idb_alert, idp_alert]])
        detox_triggered = alert_count >= 2

        reasons = []
        if ice_alert:
            reasons.append(
                f"ICE ({round(ice, 2)}) supera umbral 3.0 (Conflictos altos o uso coercitivo del ledger)"
            )
        if idb_alert:
            reasons.append(
                f"IDB ({round(idb, 2)}) supera umbral 5.0 (Ansiedad o deterioro de bienestar)"
            )
        if idp_alert:
            reasons.append(
                f"IDP ({round(idp, 2)}) indica desequilibrio doméstico persistente sin corregir"
            )

        return {
            "ice": round(ice, 2),
            "idb": round(idb, 2),
            "idp": round(idp, 2),
            "detox_triggered": detox_triggered,
            "reasons": reasons,
            "alerts": {"ice": ice_alert, "idb": idb_alert, "idp": idp_alert},
        }

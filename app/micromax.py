import json
import math
import random
import sqlite3
import string
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional


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

    def update_member_config(
        self,
        user_id: int,
        monthly_income: float,
        work_hours: float,
        travel_hours: float,
        sleep_hours: float,
    ) -> Dict:
        """Updates work/life economic configuration for a household member."""
        if monthly_income < 0 or work_hours < 0 or travel_hours < 0 or sleep_hours < 0:
            raise ValueError("Parameters cannot be negative.")
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
            SET monthly_income = ?, work_hours = ?, travel_hours = ?, sleep_hours = ?
            WHERE user_id = ?
        """,
            (monthly_income, work_hours, travel_hours, sleep_hours, user_id),
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
    ) -> Dict:
        """Logs a direct contribution (CDD) task with VHV & FIC calculation."""
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if duration_hours <= 0 or duration_hours > 24:
            raise ValueError("Task duration must be between 0 and 24 hours.")

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

        # ESI Checklist blockage verification
        cursor.execute(
            "SELECT score FROM micromax_safety_surveys WHERE member_id = ?",
            (member["id"],),
        )
        survey = cursor.fetchone()
        if survey and survey["score"] >= 3:
            raise ValueError(
                "MicroMaxocracia Access Blocked: ESI Checklist score is too high (safety threshold crossed)."
            )

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
                attention_factor, fragmentation_factor, loneliness_factor, calculated_vhv, logged_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

    def save_safety_survey(self, user_id: int, answers: Dict[str, bool]) -> Dict:
        """Saves ESI safety survey, counts score and triggers blocking rules."""
        if len(answers) != 6:
            raise ValueError("ESI Safety survey must contain exactly 6 questions.")

        member = self.get_member(user_id)
        if not member:
            raise ValueError("User is not registered in a MicroMaxocracia household.")

        # Count true answers
        score = sum(1 for v in answers.values() if v is True)
        answers_str = json.dumps(answers)

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
            "blocked": score >= 3,
        }

    def get_safety_survey(self, user_id: int) -> Optional[Dict]:
        """Gets ESI survey for a member."""
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

        return {
            "id": row["id"],
            "member_id": row["member_id"],
            "score": row["score"],
            "answers": json.loads(row["answers_json"]),
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
    ) -> Dict:
        """Calculates CDD, CEH, TED, and Equilibrium values for members in a household."""
        members = self.get_household_members(household_id)
        if not members:
            return {"members": [], "totals": {}}

        conn = self._get_db_connection()
        cursor = conn.cursor()

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

        total_cdd = sum(member_cdds.values())
        total_income = sum(m["monthly_income"] for m in members)

        # Calculate TED: 168 - work - travel - sleep
        # If sleep is not configured, fallback to 56 hours
        member_teds = {}
        for m in members:
            ted = (
                168.0 - m["work_hours"] - m["travel_hours"] - (m["sleep_hours"] or 56.0)
            )
            member_teds[m["id"]] = max(ted, 0.0)  # Cannot have negative energy

        total_ted = sum(member_teds.values())

        # Ponderations
        alpha, beta, gamma = 0.6, 0.3, 0.1

        member_results = []
        for m in members:
            cdd = member_cdds[m["id"]]
            income = m["monthly_income"]
            ted = member_teds[m["id"]]

            cdd_share = cdd / total_cdd if total_cdd > 0 else 0.0
            ceh_share = income / total_income if total_income > 0 else 0.0
            ted_share = ted / total_ted if total_ted > 0 else 0.0

            equilibrio = (alpha * cdd_share) + (beta * ceh_share) + (gamma * ted_share)

            member_results.append(
                {
                    "id": m["id"],
                    "name": m["name"],
                    "user_id": m["user_id"],
                    "cdd": round(cdd, 2),
                    "cdd_share": round(cdd_share * 100, 2),
                    "income": income,
                    "ceh_share": round(ceh_share * 100, 2),
                    "ted": round(ted, 2),
                    "ted_share": round(ted_share * 100, 2),
                    "equilibrio": round(equilibrio * 100, 2),
                }
            )

        return {
            "members": member_results,
            "totals": {
                "total_cdd": round(total_cdd, 2),
                "total_income": total_income,
                "total_ted": round(total_ted, 2),
            },
        }

    def calculate_toxicity_indices(self, household_id: int) -> Dict:
        """Calculates relational health indices (ICE, IDB, IDP) and Detox warnings."""
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
        for m in members:
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

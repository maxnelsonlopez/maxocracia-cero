import sqlite3
from datetime import datetime
from typing import Dict, List


class TVIManager:
    def __init__(self, db_path: str = "comun.db"):
        self.db_path = db_path

    def _get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _check_overlap(
        self, user_id: int, start_dt: datetime, end_dt: datetime, exclude_id: int = None
    ) -> bool:
        """
        Checks if the given time range overlaps with any existing TVI entry for the user.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 1 FROM tvi_entries
            WHERE user_id = ?
            AND (
                (start_time < ? AND end_time > ?) OR  -- Overlaps start
                (start_time < ? AND end_time > ?) OR  -- Overlaps end
                (start_time >= ? AND end_time <= ?)   -- Contained within
            )
        """
        params = [
            user_id,
            end_dt.isoformat(),
            start_dt.isoformat(),
            end_dt.isoformat(),
            start_dt.isoformat(),
            start_dt.isoformat(),
            end_dt.isoformat(),
        ]

        if exclude_id:
            query += " AND id != ?"
            params.append(exclude_id)

        cursor.execute(query, tuple(params))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def log_tvi(
        self,
        user_id: int,
        start_time: str,
        end_time: str,
        category: str,
        description: str = None,
    ) -> Dict:
        """
        Logs a new TVI entry. Enforces T0 (Uniqueness/No Overlap).
        """
        try:
            start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("Invalid date format. Use ISO8601.")

        if end_dt <= start_dt:
            raise ValueError("End time must be after start time.")

        duration_seconds = int((end_dt - start_dt).total_seconds())

        if self._check_overlap(user_id, start_dt, end_dt):
            raise ValueError(
                "TVI Overlap Detected: Axiom T0 Violation. You cannot live two moments at once."
            )

        conn = self._get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO tvi_entries (user_id, start_time, end_time, duration_seconds, category, description)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    start_dt.isoformat(),
                    end_dt.isoformat(),
                    duration_seconds,
                    category,
                    description,
                ),
            )
            tvi_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.close()
            raise ValueError(f"Database Integrity Error: {str(e)}")

        conn.close()

        return {
            "id": tvi_id,
            "user_id": user_id,
            "start_time": start_dt.isoformat(),
            "end_time": end_dt.isoformat(),
            "duration_seconds": duration_seconds,
            "category": category,
            "description": description,
        }

    def get_user_tvis(
        self, user_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict]:
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tvi_entries WHERE user_id = ? ORDER BY start_time DESC LIMIT ? OFFSET ?",
            (user_id, limit, offset),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def calculate_ccp(
        self, user_id: int, start_date: str = None, end_date: str = None
    ) -> Dict:
        """
        Calculates the Coeficiente de Coherencia Personal (CCP).
        CCP = (Investment + Leisure) / (Total Time - Maintenance)
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()

        query = "SELECT category, SUM(duration_seconds) as total_seconds FROM tvi_entries WHERE user_id = ?"
        params = [user_id]

        if start_date:
            query += " AND start_time >= ?"
            params.append(start_date)
        if end_date:
            query += " AND end_time <= ?"
            params.append(end_date)

        query += " GROUP BY category"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()

        stats = {row["category"]: row["total_seconds"] for row in rows}

        total_seconds = sum(stats.values())
        maintenance = stats.get("MAINTENANCE", 0)
        investment = stats.get("INVESTMENT", 0)
        leisure = stats.get("LEISURE", 0)
        # Waste and Work are part of total but not numerator of CCP usually,
        # though 'Work' might be Investment depending on definition.
        # For this implementation: Investment + Leisure are 'Coherent' time.

        discretionary_time = total_seconds - maintenance

        if discretionary_time <= 0:
            ccp = 0.0
        else:
            ccp = (investment + leisure) / discretionary_time

        return {
            "ccp": round(ccp, 4),
            "stats": stats,
            "total_seconds": total_seconds,
            "discretionary_seconds": discretionary_time,
        }

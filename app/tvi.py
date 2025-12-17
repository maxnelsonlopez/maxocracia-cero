import sqlite3
from datetime import datetime
from typing import Dict, List, Optional


class TVIManager:
    def __init__(self, db_path: str = "comun.db"):
        self.db_path = db_path

    def _get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _check_overlap(
        self,
        user_id: int,
        start_dt: datetime,
        end_dt: datetime,
        exclude_id: Optional[int] = None,
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
        description: Optional[str] = None,
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
        self,
        user_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict:
        """
        Calculates the Coeficiente de Coherencia Personal (CCP).
        CCP = (Investment + Leisure) / (Total Time - Maintenance)
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()

        query = "SELECT category, SUM(duration_seconds) as total_seconds FROM tvi_entries WHERE user_id = ?"
        params: List[object] = [user_id]

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

    def get_community_stats(self) -> Dict:
        """
        Calculates aggregate TVI metrics for the entire community.
        Returns total time distribution and average CCP.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()

        # 1. Total time distribution by category
        cursor.execute(
            """
            SELECT category, SUM(duration_seconds) as total_seconds
            FROM tvi_entries
            GROUP BY category
            """
        )
        rows = cursor.fetchall()
        distribution = {row["category"]: row["total_seconds"] for row in rows}

        # 2. Average CCP
        # Calculate CCP for each user, then average
        cursor.execute("SELECT DISTINCT user_id FROM tvi_entries")
        users = [row["user_id"] for row in cursor.fetchall()]

        total_ccp = 0.0
        ccp_count = 0

        for uid in users:
            stats = self.calculate_ccp(uid)
            # Only count users with valid discretionary time to avoid skew users with 0 data
            if stats["discretionary_seconds"] > 0:
                total_ccp += stats["ccp"]
                ccp_count += 1

        avg_ccp = round(total_ccp / ccp_count, 4) if ccp_count > 0 else 0.0

        conn.close()

        return {
            "distribution": distribution,
            "average_ccp": avg_ccp,
            "active_users_count": ccp_count,
            "total_hours_logged": sum(distribution.values()) / 3600.0,
        }

    def calculate_ttvi_from_tvis(
        self,
        user_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category_filter: Optional[str] = None,
    ) -> Dict:
        """
        Calculate TTVI (Tiempo Total Vital Indexado) from registered TVI entries.
        
        This method integrates TVI data with VHV calculations by providing:
        - Direct hours (WORK, INVESTMENT categories)
        - Inherited hours (can be calculated from tools/infrastructure TVIs)
        - Future hours (estimated from patterns or explicit FUTURE category)
        
        Args:
            user_id: User ID to calculate TTVI for
            start_date: Optional start date filter (ISO8601)
            end_date: Optional end date filter (ISO8601)
            category_filter: Optional category filter (MAINTENANCE, INVESTMENT, WASTE, WORK, LEISURE)
            
        Returns:
            Dictionary with:
                - direct_hours: Hours from WORK and INVESTMENT categories
                - inherited_hours: Hours from infrastructure/tools (default 0, can be extended)
                - future_hours: Estimated future hours (default 0, can be extended)
                - total_hours: Sum of all components
                - breakdown_by_category: Hours per category
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT category, SUM(duration_seconds) as total_seconds
            FROM tvi_entries
            WHERE user_id = ?
        """
        params: List[object] = [user_id]

        if start_date:
            query += " AND start_time >= ?"
            params.append(start_date)
        if end_date:
            query += " AND end_time <= ?"
            params.append(end_date)
        if category_filter:
            query += " AND category = ?"
            params.append(category_filter)

        query += " GROUP BY category"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()

        breakdown_by_category = {}
        for row in rows:
            category = row["category"]
            seconds = row["total_seconds"]
            hours = seconds / 3600.0
            breakdown_by_category[category] = round(hours, 4)

        # Map categories to TTVI components according to Axiom T8
        # Direct hours: WORK and INVESTMENT (time directly invested)
        direct_seconds = (
            breakdown_by_category.get("WORK", 0) * 3600
            + breakdown_by_category.get("INVESTMENT", 0) * 3600
        )
        direct_hours = direct_seconds / 3600.0

        # Inherited hours: Can be calculated from infrastructure/tools TVIs
        # For now, default to 0 (can be extended to track tool usage)
        inherited_hours = 0.0

        # Future hours: Estimated maintenance/disposal time
        # For now, default to 0 (can be extended with predictive models)
        future_hours = 0.0

        # Total hours
        total_hours = (
            breakdown_by_category.get("MAINTENANCE", 0)
            + breakdown_by_category.get("INVESTMENT", 0)
            + breakdown_by_category.get("WASTE", 0)
            + breakdown_by_category.get("WORK", 0)
            + breakdown_by_category.get("LEISURE", 0)
        )

        return {
            "direct_hours": round(direct_hours, 4),
            "inherited_hours": round(inherited_hours, 4),
            "future_hours": round(future_hours, 4),
            "total_hours": round(total_hours, 4),
            "breakdown_by_category": breakdown_by_category,
        }

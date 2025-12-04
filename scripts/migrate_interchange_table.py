"""
Migration script to add Formulario A fields to interchange table.

This adds the following columns:
- coordination_method: How the exchange was coordinated
- requires_followup: Boolean flag if follow-up is needed
- followup_scheduled_date: When to do the follow-up

Run this after the database is initialized with the base schema.
"""

import sqlite3
import sys
from pathlib import Path


def migrate_interchange_table(db_path):
    """Add new columns to interchange table for Formulario A support."""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(interchange)")
        columns = [row[1] for row in cursor.fetchall()]

        migrations_applied = []

        # Add coordination_method if it doesn't exist
        if "coordination_method" not in columns:
            cursor.execute(
                """
                ALTER TABLE interchange 
                ADD COLUMN coordination_method TEXT 
                CHECK(coordination_method IN ('max_direct', 'participants_alone', 'intermediary', 'other'))
            """
            )
            migrations_applied.append("coordination_method")

        # Add requires_followup if it doesn't exist
        if "requires_followup" not in columns:
            cursor.execute(
                """
                ALTER TABLE interchange 
                ADD COLUMN requires_followup INTEGER DEFAULT 0
            """
            )
            migrations_applied.append("requires_followup")

        # Add followup_scheduled_date if it doesn't exist
        if "followup_scheduled_date" not in columns:
            cursor.execute(
                """
                ALTER TABLE interchange 
                ADD COLUMN followup_scheduled_date TEXT
            """
            )
            migrations_applied.append("followup_scheduled_date")

        conn.commit()

        if migrations_applied:
            print(f"✅ Successfully added columns: {', '.join(migrations_applied)}")
        else:
            print("✅ All columns already exist, no migration needed")

        return True

    except sqlite3.Error as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    # Default database path
    db_path = Path(__file__).parent.parent / "comun.db"

    # Allow custom path from command line
    if len(sys.argv) > 1:
        db_path = Path(sys.argv[1])

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        print("Please run the application first to initialize the database.")
        sys.exit(1)

    print(f"Running migration on: {db_path}")
    success = migrate_interchange_table(str(db_path))

    sys.exit(0 if success else 1)

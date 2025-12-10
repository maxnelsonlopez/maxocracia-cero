#!/usr/bin/env python3
"""
Migration script to add missing forms tables to existing database.

Run this if you get errors like:
  sqlite3.OperationalError: no such table: participants
  sqlite3.OperationalError: no such table: follow_ups

Usage:
    source .venv/bin/activate
    python scripts/migrate_forms_tables.py
"""

import os
import sqlite3
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "comun.db")


def migrate():
    """Add missing forms tables to database."""

    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        print("   Run 'python run.py' first to create the database.")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check which tables already exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = {row[0] for row in cursor.fetchall()}

    print(f"📊 Existing tables: {existing_tables}")

    tables_to_create = []

    # Participants table (Formulario CERO)
    if "participants" not in existing_tables:
        tables_to_create.append(
            (
                "participants",
                """
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                
                -- Personal Information
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                referred_by TEXT,
                phone_call TEXT,
                phone_whatsapp TEXT,
                telegram_handle TEXT,
                city TEXT NOT NULL,
                neighborhood TEXT NOT NULL,
                personal_values TEXT,
                
                -- Offers (What they can provide)
                offer_categories TEXT,
                offer_description TEXT NOT NULL,
                offer_human_dimensions TEXT,
                
                -- Needs (What they require)
                need_categories TEXT,
                need_description TEXT NOT NULL,
                need_urgency TEXT CHECK(need_urgency IN ('Alta', 'Media', 'Baja')),
                need_human_dimensions TEXT,
                
                -- Consent and metadata
                consent_given INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'paused'))
            )
        """,
            )
        )

    # Follow-ups table (Formulario B)
    if "follow_ups" not in existing_tables:
        tables_to_create.append(
            (
                "follow_ups",
                """
            CREATE TABLE IF NOT EXISTS follow_ups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                
                -- Identification
                follow_up_date TEXT NOT NULL,
                participant_id INTEGER NOT NULL,
                related_interchange_id INTEGER,
                
                -- Type of follow-up
                follow_up_type TEXT NOT NULL CHECK(follow_up_type IN (
                    'verification_completed',
                    'update_in_progress', 
                    'situation_evolution',
                    'new_urgent_need',
                    'need_resolved',
                    'spontaneous_feedback',
                    'routine_check'
                )),
                
                -- Current Status
                current_situation TEXT NOT NULL,
                need_level INTEGER CHECK(need_level BETWEEN 1 AND 5),
                situation_change TEXT CHECK(situation_change IN (
                    'improved_significantly',
                    'improved_slightly',
                    'same',
                    'worsened_slightly',
                    'worsened_significantly',
                    'first_evaluation'
                )),
                
                -- Active Interchanges
                active_interchanges_status TEXT CHECK(active_interchanges_status IN (
                    'receiving_help',
                    'giving_help',
                    'both',
                    'none',
                    'paused'
                )),
                interchanges_working_well TEXT CHECK(interchanges_working_well IN (
                    'very_well',
                    'minor_difficulties',
                    'significant_problems',
                    'needs_adjustment',
                    NULL
                )),
                
                -- New Opportunities
                new_needs_detected TEXT,
                new_offers_detected TEXT,
                
                -- Emotional Health
                emotional_state TEXT CHECK(emotional_state IN (
                    'very_good',
                    'good',
                    'neutral',
                    'worried',
                    'bad',
                    'alert_signs',
                    'could_not_evaluate',
                    NULL
                )),
                community_connection INTEGER CHECK(community_connection BETWEEN 1 AND 5 OR community_connection IS NULL),
                
                -- Required Actions
                actions_required TEXT,
                follow_up_priority TEXT NOT NULL CHECK(follow_up_priority IN (
                    'high',
                    'medium',
                    'low',
                    'closed'
                )),
                next_follow_up_date TEXT,
                
                -- Facilitator Notes
                facilitator_notes TEXT,
                learnings TEXT,
                
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE,
                FOREIGN KEY (related_interchange_id) REFERENCES interchange(id) ON DELETE SET NULL
            )
        """,
            )
        )

    if not tables_to_create:
        print("✅ All forms tables already exist!")
        conn.close()
        return True

    # Create missing tables
    for table_name, create_sql in tables_to_create:
        print(f"📝 Creating table: {table_name}")
        cursor.execute(create_sql)

    # Create indexes
    indexes = [
        (
            "idx_participants_email",
            "CREATE INDEX IF NOT EXISTS idx_participants_email ON participants(email)",
        ),
        (
            "idx_participants_city",
            "CREATE INDEX IF NOT EXISTS idx_participants_city ON participants(city)",
        ),
        (
            "idx_participants_status",
            "CREATE INDEX IF NOT EXISTS idx_participants_status ON participants(status)",
        ),
        (
            "idx_follow_ups_participant",
            "CREATE INDEX IF NOT EXISTS idx_follow_ups_participant ON follow_ups(participant_id)",
        ),
        (
            "idx_follow_ups_priority",
            "CREATE INDEX IF NOT EXISTS idx_follow_ups_priority ON follow_ups(follow_up_priority)",
        ),
        (
            "idx_follow_ups_date",
            "CREATE INDEX IF NOT EXISTS idx_follow_ups_date ON follow_ups(follow_up_date)",
        ),
    ]

    for idx_name, idx_sql in indexes:
        try:
            cursor.execute(idx_sql)
            print(f"   ✓ Index: {idx_name}")
        except sqlite3.OperationalError:
            pass  # Index might already exist

    conn.commit()
    conn.close()

    print(f"\n✅ Migration complete! Created {len(tables_to_create)} table(s).")
    print("   You can now use the forms system.")

    return True


if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)

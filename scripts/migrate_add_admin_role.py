#!/usr/bin/env python3
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "comun.db")


def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        print("Checking for is_admin column in users table...")
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]

        if "is_admin" not in columns:
            print("Adding is_admin column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
            print("Successfully added is_admin column.")

            # Make the first user an admin by default for convenience in this dev environment
            cursor.execute(
                "UPDATE users SET is_admin = 1 WHERE id = (SELECT min(id) FROM users)"
            )
            print("Promoted first user to admin.")
        else:
            print("is_admin column already exists.")

        conn.commit()
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()

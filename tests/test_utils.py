"""
Tests for utility functions.

Tests database connection management and initialization utilities.
"""

import os
import sqlite3
import tempfile

import pytest
from flask import Flask

from app.utils import close_db, get_db, init_db


@pytest.fixture
def app():
    """Create test Flask app."""
    db_fd, db_path = tempfile.mkstemp(prefix="test_utils_", suffix=".db")
    os.close(db_fd)

    app = Flask(__name__)
    app.config["DATABASE"] = db_path
    app.config["TESTING"] = True

    # Register teardown
    app.teardown_appcontext(close_db)

    yield app

    # Cleanup
    try:
        os.unlink(db_path)
    except OSError:
        pass


class TestGetDb:
    """Test get_db() function."""

    def test_get_db_creates_connection(self, app):
        """Test that get_db creates a new database connection."""
        with app.app_context():
            db = get_db()
            assert db is not None
            assert isinstance(db, sqlite3.Connection)

    def test_get_db_reuses_connection(self, app):
        """Test that get_db reuses connection in same context."""
        with app.app_context():
            db1 = get_db()
            db2 = get_db()
            assert db1 is db2  # Should be the same connection

    def test_get_db_sets_row_factory(self, app):
        """Test that get_db sets row_factory to sqlite3.Row."""
        with app.app_context():
            db = get_db()
            assert db.row_factory == sqlite3.Row

    def test_get_db_different_contexts(self, app):
        """Test that different app contexts get different connections."""
        with app.app_context():
            db1 = get_db()

        with app.app_context():
            db2 = get_db()
            assert db1 is not db2  # Different contexts, different connections


class TestCloseDb:
    """Test close_db() function."""

    def test_close_db_closes_connection(self, app):
        """Test that close_db closes the database connection."""
        with app.app_context():
            db = get_db()
            assert db is not None

            # Manually call close_db
            close_db(None)

            # Connection should be removed from g
            from flask import g

            assert "db" not in g

    def test_close_db_no_connection(self, app):
        """Test that close_db handles case when no connection exists."""
        with app.app_context():
            # Should not raise error
            close_db(None)


class TestInitDb:
    """Test init_db() function."""

    def test_init_db_creates_schema(self, app):
        """Test that init_db creates database schema."""
        db_path = app.config["DATABASE"]

        # Database should not exist or be empty
        if os.path.exists(db_path):
            os.unlink(db_path)

        # Set root_path to point to app directory
        app.root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app")

        with app.app_context():
            init_db()

        # Verify schema was created
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check that tables exist
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='users'
        """
        )
        assert cursor.fetchone() is not None

        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='interchange'
        """
        )
        assert cursor.fetchone() is not None

        conn.close()

    def test_init_db_with_app_context(self, app):
        """Test init_db works when called with app context."""
        db_path = app.config["DATABASE"]

        if os.path.exists(db_path):
            os.unlink(db_path)

        # Set root_path to point to app directory
        app.root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app")

        with app.app_context():
            init_db(app)

        # Verify schema was created
        assert os.path.exists(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "users" in tables
        conn.close()

    def test_init_db_without_app_context(self):
        """Test init_db when called without app context."""
        db_fd, db_path = tempfile.mkstemp(prefix="test_init_", suffix=".db")
        os.close(db_fd)

        app = Flask(__name__)
        app.config["DATABASE"] = db_path
        # Set root_path to point to app directory
        app.root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app")

        # Should work when passing app explicitly
        init_db(app)

        # Verify schema was created
        assert os.path.exists(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert len(tables) > 0
        conn.close()

        # Cleanup
        try:
            os.unlink(db_path)
        except OSError:
            pass

    def test_init_db_handles_existing_db(self, app):
        """Test that init_db can be called on existing database."""
        db_path = app.config["DATABASE"]

        # Set root_path to point to app directory
        app.root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app")

        with app.app_context():
            # Initialize first time
            init_db()

            # Initialize again (should not fail)
            init_db()

        # Verify database still exists and is valid
        assert os.path.exists(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        # Should not raise error
        conn.close()

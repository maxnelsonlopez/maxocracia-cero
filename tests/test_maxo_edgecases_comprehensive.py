"""
Tests adicionales para edge cases de maxo.py

Cubre casos límite y validaciones adicionales
"""

import pytest

from app.maxo import calculate_maxo_price, credit_user, get_balance


class TestMaxoEdgeCases:
    """Tests para edge cases de maxo.py."""

    def test_calculate_maxo_price_zero_values(self, app):
        """Test cálculo con valores cero."""
        with app.app_context():
            price = calculate_maxo_price(t_seconds=0.0, v_lives=0.0, r_resources=0.0)
            assert price == 0.0

    def test_calculate_maxo_price_negative_v_lives(self, app):
        """Test cálculo con v_lives negativo (rescate de vidas)."""
        with app.app_context():
            # V negativo podría representar rescate de vidas
            price = calculate_maxo_price(
                t_seconds=3600.0, v_lives=-0.5, r_resources=0.0
            )
            # El precio debe ser calculado correctamente incluso con V negativo
            assert isinstance(price, float)
            assert price >= 0.0  # El precio final no puede ser negativo

    def test_calculate_maxo_price_very_large_values(self, app):
        """Test cálculo con valores muy grandes."""
        with app.app_context():
            price = calculate_maxo_price(t_seconds=1e6, v_lives=1000.0, r_resources=1e6)
            assert isinstance(price, float)
            assert price >= 0.0

    def test_calculate_maxo_price_frg_cs_modifiers(self, app):
        """Test cálculo con modificadores FRG y CS."""
        with app.app_context():
            # Sin modificadores
            price_base = calculate_maxo_price(
                t_seconds=3600.0, v_lives=0.0, r_resources=100.0, frg=1.0, cs=1.0
            )

            # Con modificadores altos
            price_high = calculate_maxo_price(
                t_seconds=3600.0, v_lives=0.0, r_resources=100.0, frg=2.0, cs=2.0
            )

            # El precio debe ser mayor con modificadores altos
            assert price_high > price_base

    def test_get_balance_no_transactions(self, app):
        """Test get_balance sin transacciones."""
        with app.app_context():
            from werkzeug.security import generate_password_hash

            from app.utils import get_db

            db = get_db()
            db.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                (
                    "balance_test@example.com",
                    "Balance Test",
                    generate_password_hash("Pass123!"),
                ),
            )
            db.commit()
            user_id = db.execute(
                "SELECT id FROM users WHERE email = ?", ("balance_test@example.com",)
            ).fetchone()["id"]

            balance = get_balance(user_id)
            assert balance == 0.0

    def test_get_balance_with_transactions(self, app):
        """Test get_balance con transacciones."""
        with app.app_context():
            from werkzeug.security import generate_password_hash

            from app.utils import get_db

            db = get_db()
            db.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                (
                    "balance_test2@example.com",
                    "Balance Test 2",
                    generate_password_hash("Pass123!"),
                ),
            )
            db.commit()
            user_id = db.execute(
                "SELECT id FROM users WHERE email = ?", ("balance_test2@example.com",)
            ).fetchone()["id"]

            # Añadir créditos
            credit_user(user_id, 100.0, "Test credit 1")
            credit_user(user_id, 50.0, "Test credit 2")
            credit_user(user_id, -25.0, "Test debit")

            balance = get_balance(user_id)
            assert balance == 125.0

    def test_credit_user_with_reason(self, app):
        """Test credit_user con razón."""
        with app.app_context():
            from werkzeug.security import generate_password_hash

            from app.utils import get_db

            db = get_db()
            db.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                (
                    "credit_test@example.com",
                    "Credit Test",
                    generate_password_hash("Pass123!"),
                ),
            )
            db.commit()
            user_id = db.execute(
                "SELECT id FROM users WHERE email = ?", ("credit_test@example.com",)
            ).fetchone()["id"]

            credit_user(user_id, 75.0, "Test reason")

            # Verificar que se registró
            ledger = db.execute(
                "SELECT * FROM maxo_ledger WHERE user_id = ?", (user_id,)
            ).fetchone()
            assert ledger is not None
            assert ledger["change_amount"] == 75.0
            assert ledger["reason"] == "Test reason"

    def test_credit_user_negative_amount(self, app):
        """Test credit_user con cantidad negativa (débito)."""
        with app.app_context():
            from werkzeug.security import generate_password_hash

            from app.utils import get_db

            db = get_db()
            db.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                (
                    "debit_test@example.com",
                    "Debit Test",
                    generate_password_hash("Pass123!"),
                ),
            )
            db.commit()
            user_id = db.execute(
                "SELECT id FROM users WHERE email = ?", ("debit_test@example.com",)
            ).fetchone()["id"]

            # Añadir crédito primero
            credit_user(user_id, 100.0, "Initial credit")
            # Luego débito
            credit_user(user_id, -30.0, "Debit")

            balance = get_balance(user_id)
            assert balance == 70.0

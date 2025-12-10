import os
import tempfile

import pytest

from app import create_app
from app.maxo import calculate_maxo_price, get_vhv_parameters
from app.utils import get_db


@pytest.fixture
def app():
    # Create a temporary file for the DB
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(db_path)

    app.config.update({"TESTING": True})

    with app.app_context():
        # Initialize DB with schema
        from app import init_db

        init_db()

    yield app

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


def test_default_parameters_fallback(app):
    """Test that we get default parameters if DB is empty/fails."""
    with app.app_context():
        # Clear parameters table first
        db = get_db()
        db.execute("DELETE FROM vhv_parameters")
        db.commit()

        alpha, beta, gamma, delta = get_vhv_parameters()
        assert alpha == 100.0
        assert beta == 2000.0
        assert gamma == 1.0  # Default linear for safety
        assert delta == 100.0


def test_valuation_time_only(app):
    """Test price based only on Time (T)."""
    with app.app_context():
        # Alpha=100, Beta=2000, Gamma=1, Delta=100
        # 1 hour of time = 100 Maxos
        price = calculate_maxo_price(t_seconds=3600, v_lives=0, r_resources=0)
        assert price == 100.0

        # 30 mins = 50 Maxos
        price = calculate_maxo_price(t_seconds=1800, v_lives=0, r_resources=0)
        assert price == 50.0


def test_valuation_suffering_linear(app):
    """Test linear suffering (Gamma=1)."""
    with app.app_context():
        # V=1 life (e.g. 1 chicken in ethical farm)
        # Price = 0*T + 2000*1^1 + 0*R = 2000
        price = calculate_maxo_price(t_seconds=0, v_lives=1.0, r_resources=0)
        assert price == 2000.0


def test_valuation_suffering_exponential(app):
    """Test exponential suffering penalty (Gamma=2)."""
    with app.app_context():
        db = get_db()
        # Set Gamma to 2
        db.execute(
            "INSERT INTO vhv_parameters (alpha, beta, gamma, delta) VALUES (?, ?, ?, ?)",
            (100.0, 1000.0, 2.0, 100.0),
        )
        db.commit()

        # V=1 -> 1^2 = 1 -> 1000 * 1 = 1000
        price_1 = calculate_maxo_price(t_seconds=0, v_lives=1.0)
        assert price_1 == 1000.0

        # V=2 -> 2^2 = 4 -> 1000 * 4 = 4000
        # Linear would have been 2000. This proves exponential penalty.
        price_2 = calculate_maxo_price(t_seconds=0, v_lives=2.0)
        assert price_2 == 4000.0

        # V=10 -> 10^2 = 100 -> 1000 * 100 = 100,000!
        price_10 = calculate_maxo_price(t_seconds=0, v_lives=10.0)
        assert price_10 == 100000.0


def test_valuation_resources_multipliers(app):
    """Test resource component with FRG and CS multipliers."""
    with app.app_context():
        # Delta = 100

        # R=1 unit, basic
        price_basic = calculate_maxo_price(t_seconds=0, v_lives=0, r_resources=1.0)
        assert price_basic == 100.0

        # R=1 unit, Rare (FRG=2) and Critical (CS=5)
        # Effect = 1 * 2 * 5 = 10
        # Price = 100 * 10 = 1000
        price_critical = calculate_maxo_price(
            t_seconds=0, v_lives=0, r_resources=1.0, frg=2.0, cs=5.0
        )
        assert price_critical == 1000.0

import os
from flask import Flask
from .utils import init_db, close_db


def create_app(db_path=None):
    app = Flask(__name__)
    app.config['DATABASE'] = db_path or os.path.join(os.path.dirname(__file__), '..', 'comun.db')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

    # register teardown
    app.teardown_appcontext(close_db)

    # initialize database if not exists
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            init_db(app)

    # register blueprints
    from .auth import bp as auth_bp
    from .users import bp as users_bp
    from .interchanges import bp as interchanges_bp
    from .maxo_bp import bp as maxo_bp
    from .reputation_bp import bp as reputation_bp
    from .resources_bp import bp as resources_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(interchanges_bp)
    app.register_blueprint(maxo_bp)
    app.register_blueprint(reputation_bp)
    app.register_blueprint(resources_bp)

    # placeholder imports to ensure modules loaded
    # other optional blueprints can be imported here

    return app

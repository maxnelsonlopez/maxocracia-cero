import os

from flask import Flask, request

from .limiter import init_limiter
from .utils import close_db, init_db


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["DATABASE"] = db_path or os.path.join(
        os.path.dirname(__file__), "..", "comun.db"
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")

    # Inicializar rate limiter
    init_limiter(app)

    # Inicializar SQLAlchemy y Admin
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + app.config["DATABASE"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from .extensions import db

    db.init_app(app)

    from .admin import init_admin

    init_admin(app)

    # register teardown
    app.teardown_appcontext(close_db)

    # initialize database if not exists
    if not os.path.exists(app.config["DATABASE"]):
        with app.app_context():
            init_db(app)

    # register blueprints
    from .auth import bp as auth_bp
    from .contracts_bp import contracts_bp
    from .forms_bp import forms_bp
    from .interchanges import bp as interchanges_bp
    from .maxo_bp import bp as maxo_bp
    from .reputation_bp import bp as reputation_bp
    from .resources_bp import bp as resources_bp
    from .stripe_integration import stripe_bp
    from .subscriptions import subscriptions_bp
    from .tvi_bp import tvi_bp
    from .users import bp as users_bp
    from .vhv_bp import vhv_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(interchanges_bp)
    app.register_blueprint(reputation_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(maxo_bp)
    app.register_blueprint(vhv_bp)
    app.register_blueprint(tvi_bp)
    app.register_blueprint(forms_bp)
    app.register_blueprint(contracts_bp)
    app.register_blueprint(stripe_bp)
    app.register_blueprint(subscriptions_bp)

    # placeholder imports to ensure modules loaded
    # other optional blueprints can be imported here

    # Add security headers
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        # Content Security Policy - basic policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'"
        )

        # Strict Transport Security (always in tests, only over HTTPS in production)
        if request.is_secure or app.config.get("TESTING", False):
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response

    # serve a small static UI at /
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        from flask import send_from_directory
        
        dist_dir = os.path.join(os.path.dirname(__file__), "static", "dist")
        
        if not os.path.exists(dist_dir):
            # Fallback al static tradicional si no hay dist
            return send_from_directory(os.path.join(os.path.dirname(__file__), "static"), "index.html")

        # Intentar servir el archivo exacto (ej: /_next/static/...)
        if os.path.exists(os.path.join(dist_dir, path)) and not os.path.isdir(os.path.join(dist_dir, path)):
            return send_from_directory(dist_dir, path)
            
        # Intentar servir .html si existe (ej: /upgrade -> upgrade.html)
        html_file = f"{path}.html"
        if os.path.exists(os.path.join(dist_dir, html_file)):
            return send_from_directory(dist_dir, html_file)
            
        # Intentar servir index.html en la carpeta (ej: /admin -> admin/index.html)
        folder_index = os.path.join(path, "index.html")
        if os.path.exists(os.path.join(dist_dir, folder_index)):
            return send_from_directory(dist_dir, folder_index)

        # Si nada funciona, servir index.html (SPA Fallback)
        return send_from_directory(dist_dir, "index.html")

    @app.route("/favicon.ico")
    def favicon():
        from flask import Response

        return Response(status=204)

    return app

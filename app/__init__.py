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

    # Permitir CORS en desarrollo y para el dev server de Next.js
    from flask_cors import CORS
    CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://127.0.0.1:3000", os.environ.get("FRONTEND_URL", "")])

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
    from .subscriptions import subscriptions_bp, init_subscription_tables
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

    # Inicializar tablas específicas si no existen
    init_subscription_tables(app)

    # placeholder imports to ensure modules loaded
    # other optional blueprints can be imported here

    # Add security headers
    @app.after_request
    def add_security_headers(response):
        # print("DEBUG: Aplicando cabeceras de seguridad...")
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "img-src 'self' data: blob: https:; "
            "font-src 'self' data: https://fonts.gstatic.com; "
            "connect-src 'self' https://api.stripe.com ws://localhost:* wss://localhost:*;"
        )

        # Strict Transport Security (always in tests, only over HTTPS in production)
        if request.is_secure or app.config.get("TESTING", False):
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response

    # Serve Next.js SPA
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        from flask import send_from_directory, jsonify
        
        dist_dir = os.path.join(os.path.dirname(__file__), "static", "dist")
        
        # 1. Intentar servir el archivo exacto (ej: /_next/static/..., .txt, .js, etc.)
        target_path = os.path.join(dist_dir, path)
        if os.path.exists(target_path) and not os.path.isdir(target_path):
            return send_from_directory(dist_dir, path)

        # 2. Intentar servir .html si existe (ej: /upgrade -> upgrade.html)
        html_file = f"{path}.html"
        if os.path.exists(os.path.join(dist_dir, html_file)):
            return send_from_directory(dist_dir, html_file)
            
        # 3. Intentar servir index.html en la carpeta (ej: /admin/sdv -> admin/sdv/index.html)
        folder_index = os.path.join(path, "index.html")
        if os.path.exists(os.path.join(dist_dir, folder_index)):
            return send_from_directory(dist_dir, folder_index)

        # 4. Si llegamos aquí y el path coincide con un prefijo de API conocido,
        # devolvemos un 404 real (JSON si es posible) en lugar del SPA.
        api_prefixes = ["auth/", "api/", "subscriptions/", "forms/", "contracts/", "vhv/", "tvi/", "users/", "interchanges/"]
        if any(path.startswith(pref) for pref in api_prefixes):
            if "application/json" in request.headers.get("Accept", "") or path.startswith("api/"):
                return jsonify({"error": f"Endpoint '{path}' no encontrado"}), 404

        # 5. SPA Fallback: Servir el index.html principal para que Next.js router tome control
        return send_from_directory(dist_dir, "index.html")

    @app.errorhandler(404)
    def handle_not_found(e):
        # Si algo llega aquí es porque no coincidió con NINGUNA ruta (ni el catch_all)
        # o porque algún blueprint hizo abort(404)
        if request.path.startswith('/api/'):
            return jsonify({"error": "API route not found"}), 404
        # Re-intentar catch_all para ver si es una ruta de Next.js
        return catch_all(request.path.lstrip('/'))

    @app.route("/favicon.ico")
    def favicon():
        from flask import Response

        return Response(status=204)

    return app

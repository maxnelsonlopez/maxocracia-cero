import os

from flask import Flask, request

from .limiter import init_limiter
from .utils import close_db, init_db


def _dotform_to_dirform(path: str):
    """Convierte una ruta de payload RSC en forma de puntos a la forma
    de directorios usada por la exportación estática de Next.js.

    Ejemplos:
      admin/network/__next.admin.network.txt  -> admin/network/__next.admin/network.txt
      admin/network/__next.admin.network.__PAGE__.txt
        -> admin/network/__next.admin/network/__PAGE__.txt
      micromax/__next.micromax.txt            -> micromax/__next.micromax.txt

    Devuelve siempre barras "/" (independiente del sistema operativo).
    """
    head, _, tail = path.rpartition("/")
    if not tail.startswith("__next.") or not tail.endswith(".txt"):
        return None
    segments = tail[len("__next."):-len(".txt")].split(".")
    if not segments:
        return None
    first, rest = segments[0], segments[1:]
    parts = [head] if head else []
    parts.append(f"__next.{first}")
    parts.extend(rest)
    return "/".join(parts) + ".txt"


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
    from .micromax_bp import micromax_bp
    from .micromax import init_micromax_tables
    from .forms_manager import init_multi_offers_needs_tables
    from .contracts_bp import init_contracts_metrics_tables
    from .parties_bp import parties_bp

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
    app.register_blueprint(parties_bp)
    app.register_blueprint(stripe_bp)
    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(micromax_bp)

    # Inicializar tablas específicas si no existen
    init_subscription_tables(app)
    init_micromax_tables(app)
    init_multi_offers_needs_tables(app)
    init_contracts_metrics_tables(app)

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
        from werkzeug.exceptions import MethodNotAllowed, NotFound
        
        dist_dir = os.path.join(os.path.dirname(__file__), "static", "dist")
        
        # 1. Intentar servir el archivo exacto (ej: /_next/static/..., .txt, .js, etc.)
        target_path = os.path.join(dist_dir, path)
        if os.path.exists(target_path) and not os.path.isdir(target_path):
            return send_from_directory(dist_dir, path)

        # 1b. Payloads RSC de segmentos en forma de puntos (navegación cliente de Next).
        # La exportación estática los escribe como directorios (__next.admin/network.txt)
        # pero el router los solicita como __next.admin.network.txt.
        if "__next." in path and path.endswith(".txt"):
            dot_path = _dotform_to_dirform(path)
            if dot_path and os.path.exists(os.path.join(dist_dir, dot_path)):
                return send_from_directory(dist_dir, dot_path)

        # 2. Intentar servir .html si existe (ej: /upgrade -> upgrade.html)
        html_file = f"{path}.html"
        if os.path.exists(os.path.join(dist_dir, html_file)):
            return send_from_directory(dist_dir, html_file)
            
        # 3. Intentar servir index.html en la carpeta (ej: /admin/sdv -> admin/sdv/index.html)
        folder_index = os.path.join(path, "index.html")
        if os.path.exists(os.path.join(dist_dir, folder_index)):
            return send_from_directory(dist_dir, folder_index)

        # 4. Check if the path matches a registered backend route but with a different method.
        from werkzeug.routing import Map, Rule
        non_catch_all_rules = [
            Rule(rule.rule, methods=rule.methods, endpoint=rule.endpoint)
            for rule in app.url_map.iter_rules()
            if rule.endpoint != "catch_all" and rule.endpoint != "static"
        ]
        temp_map = Map(non_catch_all_rules)
        temp_adapter = temp_map.bind_to_environ(request.environ)
        try:
            temp_adapter.match()
        except MethodNotAllowed as e:
            # Re-raise to let Flask handle the 405 error
            raise e
        except NotFound:
            # Not matched by any registered route.
            pass

        # 5. Si llegamos aquí y el path coincide con un prefijo de API conocido,
        # devolvemos un 404 real en lugar del SPA.
        backend_prefixes = [
            "auth/", "api/", "subscriptions/", "forms/", "contracts/", 
            "vhv/", "tvi/", "users/", "interchanges/", "stripe/", 
            "reputation/", "resources/", "micromax/"
        ]
        if any(path.startswith(pref) for pref in backend_prefixes):
            return jsonify({"error": f"Endpoint '{path}' no encontrado"}), 404

        # 6. SPA Fallback: Servir el index.html principal para que Next.js router tome control
        if not app.config.get("TESTING") and os.path.exists(os.path.join(dist_dir, "index.html")):
            return send_from_directory(dist_dir, "index.html")
        
        return jsonify({"error": f"Endpoint '{path}' no encontrado"}), 404

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

"""
VHV Blueprint - API endpoints for Vector de Huella Vital calculator

Endpoints:
- POST /vhv/calculate - Calculate VHV for a product
- GET /vhv/products - List all products
- GET /vhv/products/<id> - Get product details
- GET /vhv/compare - Compare multiple products
- GET /vhv/parameters - Get current parameters
- PUT /vhv/parameters - Update parameters (requires auth)
"""

import json

from flask import Blueprint, g, jsonify, request

from .jwt_utils import token_required
from .maxo import clear_vhv_params_cache
from .tvi import TVIManager
from .utils import get_db
from .vhv_calculator import (
    CASE_STUDY_HUEVO_ETICO,
    CASE_STUDY_HUEVO_INDUSTRIAL,
    VHVCalculator,
)

vhv_bp = Blueprint("vhv", __name__, url_prefix="/vhv")
calculator = VHVCalculator()
tvi_manager = TVIManager()


@vhv_bp.route("/calculate", methods=["POST"])
def calculate():
    """
    Calculate VHV and Maxo price for a product.

    Request JSON:
        {
            "name": str,
            "category": str (optional),
            "description": str (optional),
            "t_direct_hours": float,
            "t_inherited_hours": float,
            "t_future_hours": float,
            "v_organisms_affected": float,
            "v_consciousness_factor": float,
            "v_suffering_factor": float,
            "v_abundance_factor": float,
            "v_rarity_factor": float,
            "r_minerals_kg": float,
            "r_water_m3": float,
            "r_petroleum_l": float,
            "r_land_hectares": float,
            "r_frg_factor": float,
            "r_cs_factor": float,
            "save": bool (optional, default False)
        }

    Response:
        {
            "vhv": {"T": float, "V": float, "R": float},
            "maxo_price": float,
            "breakdown": {...},
            "product_id": int (if saved)
        }
    """
    data = request.get_json()

    # Validate required fields
    required_fields = [
        "name",
        "t_direct_hours",
        "t_inherited_hours",
        "t_future_hours",
        "v_organisms_affected",
        "v_consciousness_factor",
        "v_suffering_factor",
        "v_abundance_factor",
        "v_rarity_factor",
        "r_minerals_kg",
        "r_water_m3",
        "r_petroleum_l",
        "r_land_hectares",
        "r_frg_factor",
        "r_cs_factor",
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Get current parameters
    db = get_db()
    params_row = db.execute(
        "SELECT alpha, beta, gamma, delta FROM vhv_parameters ORDER BY id DESC LIMIT 1"
    ).fetchone()

    if not params_row:
        return jsonify({"error": "No VHV parameters configured"}), 500

    alpha, beta, gamma, delta = params_row

    try:
        # Calculate VHV
        result = calculator.calculate_vhv(
            t_direct_hours=float(data["t_direct_hours"]),
            t_inherited_hours=float(data["t_inherited_hours"]),
            t_future_hours=float(data["t_future_hours"]),
            v_organisms_affected=float(data["v_organisms_affected"]),
            v_consciousness_factor=float(data["v_consciousness_factor"]),
            v_suffering_factor=float(data["v_suffering_factor"]),
            v_abundance_factor=float(data["v_abundance_factor"]),
            v_rarity_factor=float(data["v_rarity_factor"]),
            r_minerals_kg=float(data["r_minerals_kg"]),
            r_water_m3=float(data["r_water_m3"]),
            r_petroleum_l=float(data["r_petroleum_l"]),
            r_land_hectares=float(data["r_land_hectares"]),
            r_frg_factor=float(data["r_frg_factor"]),
            r_cs_factor=float(data["r_cs_factor"]),
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            delta=delta,
        )

        # Save product if requested
        product_id = None
        if data.get("save", False):
            cursor = db.execute(
                """
                INSERT INTO vhv_products (
                    name, category, description,
                    t_direct_hours, t_inherited_hours, t_future_hours,
                    v_organisms_affected, v_consciousness_factor, v_suffering_factor,
                    v_abundance_factor, v_rarity_factor,
                    r_minerals_kg, r_water_m3, r_petroleum_l, r_land_hectares,
                    r_frg_factor, r_cs_factor,
                    vhv_json, maxo_price,
                    created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["name"],
                    data.get("category", ""),
                    data.get("description", ""),
                    data["t_direct_hours"],
                    data["t_inherited_hours"],
                    data["t_future_hours"],
                    data["v_organisms_affected"],
                    data["v_consciousness_factor"],
                    data["v_suffering_factor"],
                    data["v_abundance_factor"],
                    data["v_rarity_factor"],
                    data["r_minerals_kg"],
                    data["r_water_m3"],
                    data["r_petroleum_l"],
                    data["r_land_hectares"],
                    data["r_frg_factor"],
                    data["r_cs_factor"],
                    json.dumps(result["vhv"]),
                    result["maxo_price"],
                    g.get("user_id"),  # Will be None if not authenticated
                ),
            )
            db.commit()
            product_id = cursor.lastrowid

            # Save calculation record
            db.execute(
                """
                INSERT INTO vhv_calculations (
                    product_id, user_id, parameters_snapshot, vhv_snapshot, maxo_price
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    product_id,
                    g.get("user_id"),
                    json.dumps(result["parameters_used"]),
                    json.dumps(result),
                    result["maxo_price"],
                ),
            )
            db.commit()

        response = {
            "vhv": result["vhv"],
            "maxo_price": result["maxo_price"],
            "breakdown": result["breakdown"],
            "parameters_used": result["parameters_used"],
        }

        if product_id:
            response["product_id"] = product_id

        return jsonify(response), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Calculation error: {str(e)}"}), 500


@vhv_bp.route("/products", methods=["GET"])
def get_products():
    """
    Get list of all products with their VHV.

    Query params:
        category: Filter by category (optional)
        limit: Max results (default 50)
        offset: Pagination offset (default 0)

    Response:
        {
            "products": [
                {
                    "id": int,
                    "name": str,
                    "category": str,
                    "vhv": {...},
                    "maxo_price": float,
                    "created_at": str
                }
            ],
            "total": int
        }
    """
    db = get_db()
    category = request.args.get("category")
    limit = min(int(request.args.get("limit", 50)), 100)
    offset = int(request.args.get("offset", 0))

    # Base query
    where_clause = ""
    params = []

    if category:
        where_clause = "WHERE category = ?"
        params.append(category)

    # Get total count
    count_query = f"SELECT COUNT(*) FROM vhv_products {where_clause}"
    total = db.execute(count_query, params).fetchone()[0]

    # Get products
    query = f"""
        SELECT id, name, category, description, vhv_json, maxo_price, created_at
        FROM vhv_products
        {where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])

    rows = db.execute(query, params).fetchall()

    products = []
    for row in rows:
        products.append(
            {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "description": row[3],
                "vhv": json.loads(row[4]) if row[4] else None,
                "maxo_price": row[5],
                "created_at": row[6],
            }
        )

    return jsonify({"products": products, "total": total}), 200


@vhv_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Get detailed information about a specific product.

    Response:
        All product fields including VHV breakdown
    """
    db = get_db()
    row = db.execute(
        """
        SELECT id, name, category, description,
               t_direct_hours, t_inherited_hours, t_future_hours,
               v_organisms_affected, v_consciousness_factor, v_suffering_factor,
               v_abundance_factor, v_rarity_factor,
               r_minerals_kg, r_water_m3, r_petroleum_l, r_land_hectares,
               r_frg_factor, r_cs_factor,
               vhv_json, maxo_price, created_at
        FROM vhv_products
        WHERE id = ?
        """,
        (product_id,),
    ).fetchone()

    if not row:
        return jsonify({"error": "Product not found"}), 404

    product = {
        "id": row[0],
        "name": row[1],
        "category": row[2],
        "description": row[3],
        "components": {
            "T": {
                "direct_hours": row[4],
                "inherited_hours": row[5],
                "future_hours": row[6],
            },
            "V": {
                "organisms_affected": row[7],
                "consciousness_factor": row[8],
                "suffering_factor": row[9],
                "abundance_factor": row[10],
                "rarity_factor": row[11],
            },
            "R": {
                "minerals_kg": row[12],
                "water_m3": row[13],
                "petroleum_l": row[14],
                "land_hectares": row[15],
                "frg_factor": row[16],
                "cs_factor": row[17],
            },
        },
        "vhv": json.loads(row[18]) if row[18] else None,
        "maxo_price": row[19],
        "created_at": row[20],
    }

    return jsonify(product), 200


@vhv_bp.route("/compare", methods=["GET"])
def compare_products():
    """
    Compare multiple products.

    Query params:
        ids: Comma-separated product IDs (e.g., "1,2,3")

    Response:
        {
            "products": [
                {product details with VHV},
                ...
            ],
            "comparison": {
                "cheapest": {...},
                "most_expensive": {...}
            }
        }
    """
    ids_param = request.args.get("ids")
    if not ids_param:
        return jsonify({"error": "Missing 'ids' parameter"}), 400

    try:
        ids = [int(id.strip()) for id in ids_param.split(",")]
    except ValueError:
        return jsonify({"error": "Invalid product IDs"}), 400

    if len(ids) < 2:
        return jsonify({"error": "At least 2 products required for comparison"}), 400

    db = get_db()
    placeholders = ",".join(["?" for _ in ids])
    query = f"""
        SELECT id, name, category, description, vhv_json, maxo_price
        FROM vhv_products
        WHERE id IN ({placeholders})
    """

    rows = db.execute(query, ids).fetchall()

    if len(rows) != len(ids):
        return jsonify({"error": "Some products not found"}), 404

    products = []
    for row in rows:
        products.append(
            {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "description": row[3],
                "vhv": json.loads(row[4]) if row[4] else None,
                "maxo_price": row[5],
            }
        )

    # Find cheapest and most expensive
    cheapest = min(products, key=lambda p: p["maxo_price"])
    most_expensive = max(products, key=lambda p: p["maxo_price"])

    return (
        jsonify(
            {
                "products": products,
                "comparison": {"cheapest": cheapest, "most_expensive": most_expensive},
            }
        ),
        200,
    )


@vhv_bp.route("/parameters", methods=["GET"])
def get_parameters():
    """
    Get current VHV valuation parameters.

    Response:
        {
            "alpha": float,
            "beta": float,
            "gamma": float,
            "delta": float,
            "updated_at": str,
            "notes": str
        }
    """
    db = get_db()
    row = db.execute(
        """
        SELECT alpha, beta, gamma, delta, updated_at, notes
        FROM vhv_parameters
        ORDER BY id DESC LIMIT 1
        """
    ).fetchone()

    if not row:
        return jsonify({"error": "No parameters configured"}), 500

    return (
        jsonify(
            {
                "alpha": row[0],
                "beta": row[1],
                "gamma": row[2],
                "delta": row[3],
                "updated_at": row[4],
                "notes": row[5],
            }
        ),
        200,
    )


@vhv_bp.route("/parameters", methods=["PUT"])
@token_required
def update_parameters(current_user):
    """
    Update VHV valuation parameters (requires authentication).

    Request JSON:
        {
            "alpha": float (optional),
            "beta": float (optional),
            "gamma": float (optional),
            "delta": float (optional),
            "notes": str (required)
        }

    Response:
        {
            "message": "Parameters updated successfully",
            "parameters": {...}
        }
    """
    data = request.get_json()

    if not data.get("notes"):
        return jsonify({"error": "Notes required for parameter changes"}), 400

    db = get_db()

    # Get current parameters
    current = db.execute(
        "SELECT alpha, beta, gamma, delta FROM vhv_parameters ORDER BY id DESC LIMIT 1"
    ).fetchone()

    if not current:
        return jsonify({"error": "No current parameters found"}), 500

    # Use current values if not provided
    alpha = float(data.get("alpha", current[0]))
    beta = float(data.get("beta", current[1]))
    gamma = float(data.get("gamma", current[2]))
    delta = float(data.get("delta", current[3]))

    # Validate axiomatic constraints
    try:
        if alpha <= 0:
            raise ValueError("α must be > 0 (axiom: cannot ignore time)")
        if beta <= 0:
            raise ValueError("β must be > 0 (axiom: cannot ignore life)")
        if gamma < 1:
            raise ValueError("γ must be ≥ 1 (axiom: cannot reward suffering)")
        if delta < 0:
            raise ValueError("δ must be ≥ 0 (axiom: cannot ignore resources)")

        # Insert new parameters
        db.execute(
            """
            INSERT INTO vhv_parameters (alpha, beta, gamma, delta, updated_by, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (alpha, beta, gamma, delta, current_user["id"], data["notes"]),
        )
        db.commit()

        # Clear cache to force refresh on next request
        clear_vhv_params_cache()

        return (
            jsonify(
                {
                    "message": "Parameters updated successfully",
                    "parameters": {
                        "alpha": alpha,
                        "beta": beta,
                        "gamma": gamma,
                        "delta": delta,
                    },
                }
            ),
            200,
        )

    except ValueError as e:
        return jsonify({"error": f"Axiom violation: {str(e)}"}), 400
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Failed to update parameters: {str(e)}"}), 500


@vhv_bp.route("/case-studies", methods=["GET"])
def get_case_studies():
    """
    Get predefined case studies from the paper.

    Response:
        {
            "case_studies": [
                {
                    "name": str,
                    "description": str,
                    "data": {...}
                }
            ]
        }
    """
    return (
        jsonify(
            {
                "case_studies": [
                    {
                        "name": "Huevo de Granja Ética",
                        "description": "Gallina con espacio adecuado, alimentación óptima",
                        "data": CASE_STUDY_HUEVO_ETICO,
                    },
                    {
                        "name": "Huevo de Granja Industrial",
                        "description": "Gallina en hacinamiento extremo, antibióticos masivos",
                        "data": CASE_STUDY_HUEVO_INDUSTRIAL,
                    },
                ]
            }
        ),
        200,
    )


@vhv_bp.route("/calculate-from-tvi", methods=["POST"])
@token_required
def calculate_from_tvi(current_user):
    """
    Calculate VHV using registered TVI entries for the T component.

    This endpoint integrates TVI (Tiempo Vital Indexado) with VHV calculations,
    allowing users to calculate the VHV of products/services using their
    actual time investment tracked in TVI entries.

    Request JSON:
        {
            "start_date": str (optional, ISO8601),
            "end_date": str (optional, ISO8601),
            "category_filter": str (optional, WORK/INVESTMENT/etc),
            "v_organisms_affected": float,
            "v_consciousness_factor": float,
            "v_suffering_factor": float,
            "v_abundance_factor": float,
            "v_rarity_factor": float,
            "r_minerals_kg": float,
            "r_water_m3": float,
            "r_petroleum_l": float,
            "r_land_hectares": float,
            "r_frg_factor": float,
            "r_cs_factor": float,
            "inherited_hours_override": float (optional),
            "future_hours_override": float (optional),
            "save": bool (optional, default False)
        }

    Response:
        {
            "vhv": {"T": float, "V": float, "R": float},
            "maxo_price": float,
            "breakdown": {...},
            "ttvi_breakdown": {
                "direct_hours": float,
                "inherited_hours": float,
                "future_hours": float,
                "breakdown_by_category": {...}
            }
        }
    """
    data = request.get_json()
    user_id = current_user["user_id"]

    # Validate required V and R fields
    required_fields = [
        "v_organisms_affected",
        "v_consciousness_factor",
        "v_suffering_factor",
        "v_abundance_factor",
        "v_rarity_factor",
        "r_minerals_kg",
        "r_water_m3",
        "r_petroleum_l",
        "r_land_hectares",
        "r_frg_factor",
        "r_cs_factor",
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Calculate TTVI from TVI entries
    try:
        ttvi_data = tvi_manager.calculate_ttvi_from_tvis(
            user_id=user_id,
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            category_filter=data.get("category_filter"),
        )
    except Exception as e:
        return jsonify({"error": f"Failed to calculate TTVI: {str(e)}"}), 500

    # Use overrides if provided, otherwise use calculated values
    direct_hours = ttvi_data["direct_hours"]
    inherited_hours = data.get("inherited_hours_override", ttvi_data["inherited_hours"])
    future_hours = data.get("future_hours_override", ttvi_data["future_hours"])

    # Get current parameters
    db = get_db()
    params_row = db.execute(
        "SELECT alpha, beta, gamma, delta FROM vhv_parameters ORDER BY id DESC LIMIT 1"
    ).fetchone()

    if not params_row:
        return jsonify({"error": "No VHV parameters configured"}), 500

    alpha, beta, gamma, delta = params_row

    try:
        # Calculate VHV using TVI-derived T component
        result = calculator.calculate_vhv(
            t_direct_hours=direct_hours,
            t_inherited_hours=inherited_hours,
            t_future_hours=future_hours,
            v_organisms_affected=float(data["v_organisms_affected"]),
            v_consciousness_factor=float(data["v_consciousness_factor"]),
            v_suffering_factor=float(data["v_suffering_factor"]),
            v_abundance_factor=float(data["v_abundance_factor"]),
            v_rarity_factor=float(data["v_rarity_factor"]),
            r_minerals_kg=float(data["r_minerals_kg"]),
            r_water_m3=float(data["r_water_m3"]),
            r_petroleum_l=float(data["r_petroleum_l"]),
            r_land_hectares=float(data["r_land_hectares"]),
            r_frg_factor=float(data["r_frg_factor"]),
            r_cs_factor=float(data["r_cs_factor"]),
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            delta=delta,
        )

        # Save product if requested
        product_id = None
        if data.get("save", False):
            cursor = db.execute(
                """
                INSERT INTO vhv_products (
                    name, category, description,
                    t_direct_hours, t_inherited_hours, t_future_hours,
                    v_organisms_affected, v_consciousness_factor, v_suffering_factor,
                    v_abundance_factor, v_rarity_factor,
                    r_minerals_kg, r_water_m3, r_petroleum_l, r_land_hectares,
                    r_frg_factor, r_cs_factor,
                    vhv_json, maxo_price,
                    created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get("name", "Product from TVI"),
                    data.get("category", ""),
                    data.get("description", "Calculated from TVI entries"),
                    direct_hours,
                    inherited_hours,
                    future_hours,
                    data["v_organisms_affected"],
                    data["v_consciousness_factor"],
                    data["v_suffering_factor"],
                    data["v_abundance_factor"],
                    data["v_rarity_factor"],
                    data["r_minerals_kg"],
                    data["r_water_m3"],
                    data["r_petroleum_l"],
                    data["r_land_hectares"],
                    data["r_frg_factor"],
                    data["r_cs_factor"],
                    json.dumps(result["vhv"]),
                    result["maxo_price"],
                    user_id,
                ),
            )
            db.commit()
            product_id = cursor.lastrowid

            # Save calculation record
            db.execute(
                """
                INSERT INTO vhv_calculations (
                    product_id, user_id, parameters_snapshot, vhv_snapshot, maxo_price
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    product_id,
                    user_id,
                    json.dumps(result["parameters_used"]),
                    json.dumps(result),
                    result["maxo_price"],
                ),
            )
            db.commit()

        response = {
            "vhv": result["vhv"],
            "maxo_price": result["maxo_price"],
            "breakdown": result["breakdown"],
            "parameters_used": result["parameters_used"],
            "ttvi_breakdown": ttvi_data,
        }

        if product_id:
            response["product_id"] = product_id

        return jsonify(response), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Calculation error: {str(e)}"}), 500

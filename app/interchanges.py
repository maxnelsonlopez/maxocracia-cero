from flask import Blueprint, request, jsonify
from .utils import get_db
from .maxo import credit_user, calculate_credit

bp = Blueprint('interchanges', __name__, url_prefix='/interchanges')


@bp.route('', methods=['GET'])
def list_interchanges():
    db = get_db()
    cur = db.execute('SELECT * FROM interchange ORDER BY created_at DESC LIMIT 200')
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)


@bp.route('', methods=['POST'])
def create_interchange():
    data = request.get_json() or {}
    interchange_id = data.get('interchange_id')
    giver_id = data.get('giver_id')
    receiver_id = data.get('receiver_id')
    description = data.get('description')
    uth_hours = float(data.get('uth_hours') or 0)
    impact_score = int(data.get('impact_resolution_score') or 0)
    uvc_score = data.get('uvc_score')
    urf_units = data.get('urf_units')
    try:
        uvc_score = float(uvc_score) if uvc_score is not None else None
    except Exception:
        uvc_score = None
    try:
        urf_units = float(urf_units) if urf_units is not None else None
    except Exception:
        urf_units = None
    db = get_db()
    try:
        db.execute('INSERT INTO interchange (interchange_id, date, giver_id, receiver_id, description, uth_hours, uvc_score, urf_units, impact_resolution_score) VALUES (?, DATE("now"), ?, ?, ?, ?, ?, ?, ?)',
                   (interchange_id, giver_id, receiver_id, description, uth_hours, uvc_score, urf_units, impact_score))
        db.commit()
    except Exception as e:
        # Don't expose internal error details to prevent information leakage
        return jsonify({'error': 'Failed to create interchange'}), 500

    # calculate simple Maxo credit and credit the giver (or receiver depending on rules)
    credit = calculate_credit(uth_hours=uth_hours, impact_score=impact_score, uvc_score=uvc_score, urf_units=urf_units)
    try:
        credit_user(giver_id, credit, f'Credit for interchange {interchange_id}')
    except Exception as e:
        # log but continue
        print('Failed to credit user:', e)

    return jsonify({'message': 'interchange created', 'credit': credit}), 201

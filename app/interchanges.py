from flask import Blueprint, request, jsonify
from .utils import get_db
from .maxo import credit_user

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
    db = get_db()
    try:
        db.execute('INSERT INTO interchange (interchange_id, date, giver_id, receiver_id, description, uth_hours, impact_resolution_score) VALUES (?, DATE("now"), ?, ?, ?, ?, ?)',
                   (interchange_id, giver_id, receiver_id, description, uth_hours, impact_score))
        db.commit()
    except Exception as e:
        # Don't expose internal error details to prevent information leakage
        return jsonify({'error': 'Failed to create interchange'}), 500

    # calculate simple Maxo credit and credit the giver (or receiver depending on rules)
    factor_uth = 1.0
    factor_impact = 0.5
    credit = uth_hours * factor_uth + impact_score * factor_impact
    try:
        credit_user(giver_id, credit, f'Credit for interchange {interchange_id}')
    except Exception as e:
        # log but continue
        print('Failed to credit user:', e)

    return jsonify({'message': 'interchange created', 'credit': credit}), 201

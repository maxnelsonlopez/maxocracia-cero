from flask import Blueprint, jsonify, request
from .utils import get_db

bp = Blueprint('resources', __name__, url_prefix='/resources')


@bp.route('', methods=['GET'])
def list_resources():
    db = get_db()
    cur = db.execute('SELECT id, user_id, title, category, available, created_at FROM resources ORDER BY created_at DESC LIMIT 100')
    items = [dict(row) for row in cur.fetchall()]
    return jsonify(items)


@bp.route('', methods=['POST'])
def create_resource():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    db = get_db()
    try:
        db.execute('INSERT INTO resources (user_id, title, description, category, available) VALUES (?, ?, ?, ?, ?)',
                   (user_id, title, description, category, 1))
        db.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'resource created'}), 201


@bp.route('/<int:res_id>/claim', methods=['POST'])
def claim_resource(res_id):
    # simple implementation: create an interchange record linking requester and owner
    data = request.get_json() or {}
    requester_id = data.get('requester_id')
    db = get_db()
    row = db.execute('SELECT * FROM resources WHERE id = ?', (res_id,)).fetchone()
    if not row:
        return jsonify({'error': 'resource not found'}), 404
    owner_id = row['user_id']
    db.execute('INSERT INTO interchange (interchange_id, date, giver_id, receiver_id, type, description) VALUES (?, DATE("now"), ?, ?, ?, ?)',
               (f'INT-{res_id}-{requester_id}', owner_id, requester_id, row['category'], row['description']))
    db.commit()
    return jsonify({'message': 'claim created'}), 201

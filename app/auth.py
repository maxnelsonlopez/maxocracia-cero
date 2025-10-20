from flask import Blueprint, request, jsonify, session
from .utils import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from .jwt_utils import create_token

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    alias = data.get('alias')
    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400
    db = get_db()
    try:
        db.execute('INSERT INTO users (email, name, alias, password_hash) VALUES (?, ?, ?, ?)',
                   (email, name, alias, generate_password_hash(password)))
        db.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'user created'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'invalid credentials'}), 401
    session.clear()
    session['user_id'] = user['id']
    token = create_token({'user_id': user['id'], 'email': user['email']})
    return jsonify({'message': 'logged in', 'user_id': user['id'], 'token': token})


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'logged out'})

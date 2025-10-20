import secrets
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from .utils import get_db

# use SECRET_KEY for HMAC if available
SECRET = os.environ.get('SECRET_KEY', 'dev-secret')

# Length of raw refresh token in bytes (will be hex-encoded)
RAW_TOKEN_BYTES = 32

def generate_refresh_token_raw() -> str:
    return secrets.token_hex(RAW_TOKEN_BYTES)

def hash_refresh_token(token: str) -> str:
    # HMAC-SHA256 using SECRET to derive token hash for storage
    return hmac.new(SECRET.encode('utf-8'), token.encode('utf-8'), hashlib.sha256).hexdigest()

def store_refresh_token(user_id: int, jti: str, raw_token: str, expires_in: Optional[int] = None):
    db = get_db()
    token_hash = hash_refresh_token(raw_token)
    issued_at = datetime.now(timezone.utc).isoformat()
    expires_at = None
    if expires_in:
        expires_at = (datetime.now(timezone.utc) + timedelta(seconds=expires_in)).isoformat()
    db.execute(
        "INSERT INTO refresh_tokens (user_id, jti, token_hash, issued_at, expires_at, revoked) VALUES (?, ?, ?, ?, ?, 0)",
        (user_id, jti, token_hash, issued_at, expires_at),
    )
    db.commit()

def revoke_refresh_token_by_jti(jti: str):
    db = get_db()
    db.execute("DELETE FROM refresh_tokens WHERE jti=?", (jti,))
    db.commit()

def revoke_user_tokens(user_id: int):
    db = get_db()
    db.execute("DELETE FROM refresh_tokens WHERE user_id=?", (user_id,))
    db.commit()

def find_refresh_token_record(jti: str):
    db = get_db()
    cur = db.execute("SELECT id, user_id, jti, token_hash, issued_at, expires_at, revoked FROM refresh_tokens WHERE jti=?", (jti,))
    row = cur.fetchone()
    return row

def verify_refresh_token_raw(jti: str, raw_token: str) -> bool:
    rec = find_refresh_token_record(jti)
    if not rec:
        return False
    if rec['revoked']:
        return False
    if rec['expires_at']:
        try:
            exp = datetime.fromisoformat(rec['expires_at'])
            if datetime.now(timezone.utc) > exp:
                return False
        except Exception:
            pass
    stored_hash = rec['token_hash']
    return hmac.compare_digest(stored_hash, hash_refresh_token(raw_token))

def rotate_refresh_token(old_jti: str, new_jti: str, new_raw_token: str, expires_in: Optional[int] = None):
    # Revoke old token and store new rotated token
    rec = find_refresh_token_record(old_jti)
    if not rec:
        return False
    revoke_refresh_token_by_jti(old_jti)
    store_refresh_token(rec['user_id'], new_jti, new_raw_token, expires_in)
    return True

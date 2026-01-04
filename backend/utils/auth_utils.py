import os
import uuid
import hashlib
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request
from db import SessionLocal
from models import User

# ======================
# SECRETS (NO .env REQUIRED IF INJECTED VIA K8S)
# ======================
JWT_SECRET = os.environ.get("JWT_SECRET")  # inject via K8s Secret or mounted file
JWT_ALG = "HS256"


if not JWT_SECRET :
    raise RuntimeError("JWT secret is not configured")

def utcnow():
    return datetime.now(timezone.utc)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
# ======================
# TOKEN EXPIRATION
# ======================
ACCESS_TOKEN_EXPIRES_MIN = int(os.getenv("ACCESS_TOKEN_MINUTES", "15"))
REFRESH_TOKEN_EXPIRES_DAYS = int(os.getenv("REFRESH_TOKEN_DAYS", "7"))

# ======================
# TOKEN GENERATORS
# ======================
def generate_access_token(user_id: int, is_admin: bool):
    now = utcnow()
    payload = {
        "user_id":user_id,
        "is_admin": bool(is_admin),
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MIN)).timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def generate_refresh_token(user_id):
    now = utcnow()
    jti = str(uuid.uuid4())
    expires_at = now + timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS)
    payload = {
        "user_id":user_id,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": jti,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
    return token, jti, expires_at

# ======================
# TOKEN VERIFIERS
# ======================
def verify_access_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        if payload.get("type") != "access":
            return None
        return payload
    except jwt.PyJWTError:
        return None


def verify_refresh_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        if payload.get("type") != "refresh":
            return None
        return payload
    except jwt.PyJWTError:
        return None

# ======================
# HEADER PARSER
# ======================
def get_token_from_request():
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    parts = auth.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]

# ======================
# DECORATORS
# ======================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        if not token:
            return {"error": "missing authorization token"}, 401

        payload = verify_access_token(token)
        if not payload:
            return {"error": "invalid or expired token"}, 401

        request.user_id = (payload["user_id"])
        request.is_admin = payload.get("is_admin", False)
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        if not token:
            return {"error": "missing authorization token"}, 401

        payload = verify_access_token(token)
        if not payload:
            return {"error": "invalid or expired token"}, 401

        if not payload.get("is_admin"):
            return {"error": "admin access required"}, 403

        request.user_id = payload["user_id"]
        request.is_admin = True
        return f(*args, **kwargs)
    return decorated


def optional_auth(f):
    """Decorator for optional authentication (doesn't fail if no token)"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        if token:
            payload = verify_access_token(token)
            if payload:
                request.user_id = payload['user_id']
                request.is_admin = payload.get('is_admin', False)
            else:
                request.user_id = None
                request.is_admin = False
        else:
            request.user_id = None
            request.is_admin = False
        return f(*args, **kwargs)
    return decorated

def require_active_user(f):
    """
    Allows only ACTIVE users to perform write operations.
    Admins bypass this check.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.is_admin:
            return f(*args, **kwargs)

        with SessionLocal() as s:
            user = s.query(User).filter(User.id == request.user_id).first()
            if not user:
                return {"error": "user not found"}, 404

            if user.status != "ACTIVE":
                return {
                    "error": "Your account is pending approval. "
                             "You will be notified by email once activated."
                }, 403

        return f(*args, **kwargs)
    return decorated


# Helper function to format dates
def format_date(date_obj):
    return date_obj.strftime('%Y-%m-%d') if date_obj else None

def format_datetime(dt_obj):
    return dt_obj.strftime('%Y-%m-%d %H:%M:%S') if dt_obj else None

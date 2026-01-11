from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from db import SessionLocal
from models import User, RefreshToken
from utils.auth_utils import generate_access_token, generate_refresh_token, verify_refresh_token, hash_token, token_required
from services.email_service import send_admin_new_user_email

auth_bp = Blueprint("auth", __name__)

# ============= AUTH ENDPOINTS =============
@auth_bp.post("/auth/register")
def register_request():
    """User requests registration - sent to admin"""
    data = request.get_json(force=True)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "username, email, and password required"}, 400

    with SessionLocal() as s:
        existing = s.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing:
            return {"error": "username or email already exists"}, 409
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            status="PENDING",
            is_active=False,
            is_admin=False
        )

        s.add(user)
        s.commit()
        try:
            send_admin_new_user_email(user)
        except Exception as e:
            print("Email failed: ", e)
        return {
            "message": "Registration submitted. Your account will be activated in a couple of days.",
            "requested_username": username,
            "requested_email": email,
            "status": user.status
        }, 202

@auth_bp.post("/auth/login")
def login():
    """User login with username and password"""
    data = request.get_json(force=True)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username and not email:
        return {"error": "username or email required"}, 400

    if not password :
        return {"error": "password required"}, 400

    with SessionLocal() as s:
        if username:
            user = s.query(User).filter(User.username == username).first()
        elif email:
            user = s.query(User).filter(User.email==email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {"error": "invalid username or password"}, 401
        if user.status != "ACTIVE":
            return {
                "error": "Your account is pending approval. You will be notified once activated."
            }, 403
        if not user.is_active:
            return {"error": "user is disabled"}, 403
        
        access = generate_access_token(user.id, user.is_admin)
        refresh, jti, exp = generate_refresh_token(user.id)

        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ua = request.headers.get("User-Agent")
        s.add(RefreshToken(
            user_id=user.id,
            jti=jti,
            token_hash=hash_token(refresh),
            expires_at=exp.replace(tzinfo=None),
            revoked=False,
            ip_address=ip,
            user_agent=ua
        ))
        user.last_login_at = datetime.utcnow()
        s.commit()
        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "Bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }
        }, 200
        

@auth_bp.post("/auth/refresh")
def refresh():
    data = request.get_json(force=True)
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return {"error": "refresh_token required"}, 400

    payload = verify_refresh_token(refresh_token)
    if not payload:
        return {"error": "invalid or expired refresh token"}, 401

    user_id = payload["user_id"]
    jti = payload.get("jti")
    presented_hash = hash_token(refresh_token)

    with SessionLocal() as s:
        rt = s.query(RefreshToken).filter(RefreshToken.jti == jti).first()
        if not rt:
            return {"error": "refresh token not recognized"}, 401
        if rt.revoked:
            return {"error": "refresh token revoked"}, 401
        if rt.token_hash != presented_hash:
            return {"error": "refresh token mismatch"}, 401
        
        user = s.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active or user.status != "ACTIVE":
            return {"error": "user not found or disabled"}, 401

        rt.revoked = True
        rt.revoked_at = datetime.utcnow()

        new_refresh, new_jti, new_exp = generate_refresh_token(user_id)
        rt.replaced_by_jti = new_jti

        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ua = request.headers.get("User-Agent")
        s.add(RefreshToken(
            user_id=user_id,
            jti=new_jti,
            token_hash=hash_token(new_refresh),
            expires_at=new_exp.replace(tzinfo=None),
            revoked=False,
            ip_address=ip,
            user_agent=ua
        ))
        access = generate_access_token(user_id, user.is_admin)
        s.commit()
        return {
            "access_token": access,
            "refresh_token": new_refresh,
            "token_type": "Bearer"
        }, 200

@auth_bp.post("/auth/logout")
def logout():
    data = request.get_json(force=True)
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return {"error": "refresh_token required"}, 400

    payload = verify_refresh_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        return {"error": "invalid refresh token"}, 401

    user_id = payload["user_id"]
    jti = payload.get("jti")

    with SessionLocal() as s:
        rt = s.query(RefreshToken).filter(RefreshToken.jti == jti).first()
        if rt:
            rt.revoked = True
            rt.revoked_at = datetime.utcnow()

        user = s.query(User).filter(User.id == user_id).first()
        if user:
            user.last_logout_at = datetime.utcnow()

        s.commit()

    return {"message": "logged out"}, 200


@auth_bp.post("/auth/logout-all")
@token_required
def logout_all():
    with SessionLocal() as s:
        s.query(RefreshToken).filter(
            RefreshToken.user_id == request.user_id,
            RefreshToken.revoked == False
        ).update(
            {"revoked": True, "revoked_at": datetime.utcnow()},
            synchronize_session=False
        )

        user = s.query(User).filter(User.id == request.user_id).first()
        if user:
            user.last_logout_at = datetime.utcnow()

        s.commit()

    return {"message": "logged out from all sessions"}, 200


@auth_bp.get("/me")
@token_required
def me():
    with SessionLocal() as s:
        user = s.query(User).filter(User.id == request.user_id).first()
        if not user:
            return {"error": "user not found"}, 404

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "status": user.status,
            "created_at": user.created_at.isoformat(),
            "approved_at": user.approved_at.isoformat() if user.approved_at else None,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
        }, 200

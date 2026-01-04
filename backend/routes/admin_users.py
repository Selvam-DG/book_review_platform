from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from db import SessionLocal
from models import User
from utils.auth_utils import admin_required, format_datetime
from datetime import datetime
from services.email_service import send_user_approved_email, send_user_rejected_email

admin_users_bp = Blueprint("admin_users", __name__)
# ============= ADMIN USER MANAGEMENT =============
@admin_users_bp.post("/admin/users")
@admin_required
def admin_create_user():
    """Admin creates a new user"""
    data = request.get_json(force=True)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    is_admin = data.get("is_admin", False)

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
            is_admin=is_admin
        )
        s.add(user)
        s.commit()
        s.refresh(user)
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": format_datetime(user.created_at)
        }, 201

@admin_users_bp.get("/admin/users")
@admin_required
def admin_list_users():
    """Admin lists all users"""
    with SessionLocal() as s:
        users = s.query(User).all()
        return jsonify([
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "is_admin": u.is_admin,
                "status": u.status,
                "created_at": format_datetime(u.created_at),
                "approved_at": format_datetime(u.approved_at)               
            }
            for u in users
        ]), 200

@admin_users_bp.delete("/admin/users/<int:user_id>")
@admin_required
def admin_delete_user(user_id: int):
    """Admin deletes a user"""
    with SessionLocal() as s:
        user = s.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "user not found"}, 404
        s.delete(user)
        s.commit()
        return {"message": "user deleted"}, 200




@admin_users_bp.post("/admin/users/<int:user_id>/approve")
@admin_required
def approve_user(user_id: int):
    with SessionLocal() as s:
        user = s.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "user not found"}, 404

        if user.status == "ACTIVE":
            return {"message": "user already active"}, 200

        user.status = "ACTIVE"
        user.approved_at = datetime.utcnow()
        user.approved_by = request.user_id
        user.is_active = True

        s.commit()
        try:
            send_user_approved_email(user)
        except Exception as e:
            print("Email failed: ", e)

        return {
            "message": "user approved",
            "user_id": user.id,
            "status": user.status
        }, 200

@admin_users_bp.post("/admin/users/<int:user_id>/reject")
@admin_required
def reject_user(user_id: int):
    with SessionLocal() as s:
        user = s.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "user not found"}, 404

        user.status = "REJECTED"
        s.commit()
        try:
            send_user_rejected_email(user)
        except Exception as e:
            print("Email failed: ", e)
        return {
            "message": "user rejected",
            "user_id": user.id,
            "status": user.status
        }, 200

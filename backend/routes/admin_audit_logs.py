from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import desc

from db import SessionLocal
from models import AuditLog, User
from utils.auth_utils import admin_required, format_datetime

admin_audit_logs_bp = Blueprint("admin_audit_logs", __name__)

@admin_audit_logs_bp.get("/admin/audit-logs")
@admin_required
def list_audit_logs():
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 20)), 100)

    action = request.args.get("action")
    entity_type = request.args.get("entity_type")
    actor_user_id = request.args.get("actor_user_id")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    with SessionLocal() as s:
        q = s.query(AuditLog).options(joinedload(AuditLog.actor_user))

        if action:
            q = q.filter(AuditLog.action == action)
        if entity_type:
            q = q.filter(AuditLog.entity_type == entity_type)
        if actor_user_id:
            q = q.filter(AuditLog.actor_user_id == int(actor_user_id))
        if from_date:
            q = q.filter(AuditLog.created_at >= from_date)
        if to_date:
            q = q.filter(AuditLog.created_at <= to_date)

        total = q.count()

        logs = (
            q.order_by(desc(AuditLog.created_at))
             .offset((page - 1) * page_size)
             .limit(page_size)
             .all()
        )

        return jsonify({
            "items": [
                {
                    "id": log.id,
                    "actor": {
                        "id": log.actor_user_id,
                        "username": log.actor_user.username if log.actor_user else None
                    },
                    "action": log.action,
                    "entity_type": log.entity_type,
                    "entity_id": log.entity_id,
                    "metadata": log.metadata,
                    "ip_address": log.ip_address,
                    "created_at": format_datetime(log.created_at)
                }
                for log in logs
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total
            }
        }), 200

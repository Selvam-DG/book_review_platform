import json
from flask import request
from db import SessionLocal
from models import AuditLog

def log_audit(
    actor_user_id: int | None,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    metadata: dict | None = None
):
    with SessionLocal() as s:
        log = AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            metadata=json.dumps(metadata) if metadata else None,
            ip_address=request.headers.get("X-Forwarded-For", request.remote_addr),
            user_agent=request.headers.get("User-Agent")
        )
        s.add(log)
        s.commit()

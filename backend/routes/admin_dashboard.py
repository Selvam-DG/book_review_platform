from flask import Blueprint
from sqlalchemy import func
from datetime import datetime, timedelta

from db import SessionLocal
from models import User, Book, Author, Genre, Review, BookSuggestion
from utils.auth_utils import admin_required

admin_dashboard_bp = Blueprint("admin_dashboard", __name__)

@admin_dashboard_bp.get("/admin/dashboard/metrics")
@admin_required
def dashboard_metrics():
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)

    with SessionLocal() as s:
        metrics = {
            "users": {
                "total": s.query(func.count(User.id)).scalar(),
                "pending": s.query(func.count(User.id)).filter(User.status == "PENDING").scalar(),
                "active": s.query(func.count(User.id)).filter(User.status == "ACTIVE").scalar(),
                "admins": s.query(func.count(User.id)).filter(User.is_admin == True).scalar(),
            },
            "books": {
                "total": s.query(func.count(Book.id)).scalar(),
                "authors": s.query(func.count(Author.id)).scalar(),
                "genres": s.query(func.count(Genre.id)).scalar(),
            },
            "reviews": {
                "total": s.query(func.count(Review.id)).scalar(),
                "last_7_days": s.query(func.count(Review.id)).filter(
                    Review.created_at >= seven_days_ago
                ).scalar(),
            },
            "suggestions": {
                "pending": s.query(func.count(BookSuggestion.id)).filter(
                    BookSuggestion.status == "PENDING"
                ).scalar()
            }
        }

        return metrics, 200

from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import BookSuggestion
from utils.auth_utils import token_required, format_datetime

book_suggestions_bp = Blueprint("book_suggestions", __name__)


@book_suggestions_bp.post("/suggestions")
@token_required
def create_suggestion():
    data = request.get_json(force=True)

    title = data.get("title")
    author_name = data.get("author_name")
    genre_name = data.get("genre_name")
    description = data.get("description")

    if not title:
        return {"error": "title required"}, 400

    with SessionLocal() as s:
        suggestion = BookSuggestion(
            suggested_by_user_id=request.user_id,
            title=title,
            author_name=author_name,
            genre_name=genre_name,
            description=description
        )
        s.add(suggestion)
        s.commit()
        s.refresh(suggestion)

        return {
            "message": "Book suggestion submitted for admin review",
            "suggestion_id": suggestion.id,
            "status": suggestion.status
        }, 202


@book_suggestions_bp.get("/suggestions/mine")
@token_required
def my_suggestions():
    with SessionLocal() as s:
        suggestions = s.query(BookSuggestion).filter(
            BookSuggestion.suggested_by_user_id == request.user_id
        ).all()

        return jsonify([
            {
                "id": sg.id,
                "title": sg.title,
                "author_name": sg.author_name,
                "genre_name": sg.genre_name,
                "status": sg.status,
                "created_at": format_datetime(sg.created_at)
            }
            for sg in suggestions
        ]), 200

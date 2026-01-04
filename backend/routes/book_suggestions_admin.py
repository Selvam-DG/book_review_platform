from flask import Blueprint, request, jsonify
from datetime import datetime
from db import SessionLocal
from models import BookSuggestion, Book, Author, Genre
from utils.auth_utils import admin_required, format_datetime

book_suggestions_admin_bp = Blueprint("admin_suggestions", __name__)


@book_suggestions_admin_bp.get("/admin/suggestions")
@admin_required
def list_suggestions():
    status = request.args.get("status", "PENDING")

    with SessionLocal() as s:
        suggestions = s.query(BookSuggestion).filter(
            BookSuggestion.status == status
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

@book_suggestions_admin_bp.post("/admin/suggestions/<int:suggestion_id>/approve")
@admin_required
def approve_suggestion(suggestion_id: int):
    with SessionLocal() as s:
        sg = s.query(BookSuggestion).filter(BookSuggestion.id == suggestion_id).first()
        if not sg or sg.status != "PENDING":
            return {"error": "suggestion not found or already processed"}, 404

        # Author
        author = None
        if sg.author_name:
            author = s.query(Author).filter(Author.name == sg.author_name).first()
            if not author:
                author = Author(name=sg.author_name)
                s.add(author)
                s.flush()

        # Genre
        genre = None
        if sg.genre_name:
            genre = s.query(Genre).filter(Genre.name == sg.genre_name).first()
            if not genre:
                genre = Genre(name=sg.genre_name)
                s.add(genre)
                s.flush()

        # Create Book
        book = Book(
            title=sg.title,
            author_id=author.id if author else None,
            genre_id=genre.id if genre else None,
            description=sg.description
        )
        s.add(book)

        sg.status = "APPROVED"
        sg.reviewed_at = datetime.utcnow()
        sg.reviewed_by = request.user_id

        s.commit()

        return {
            "message": "Suggestion approved and book created",
            "book_id": book.id
        }, 200


@book_suggestions_admin_bp.post("/admin/suggestions/<int:suggestion_id>/reject")
@admin_required
def reject_suggestion(suggestion_id: int):
    data = request.get_json(force=True)
    reason = data.get("reason")

    with SessionLocal() as s:
        sg = s.query(BookSuggestion).filter(BookSuggestion.id == suggestion_id).first()
        if not sg:
            return {"error": "suggestion not found"}, 404

        sg.status = "REJECTED"
        sg.admin_notes = reason
        sg.reviewed_at = datetime.utcnow()
        sg.reviewed_by = request.user_id

        s.commit()

        return {"message": "suggestion rejected"}, 200

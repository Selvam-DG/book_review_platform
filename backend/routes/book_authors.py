from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from db import SessionLocal

from models import Author
from utils.auth_utils import admin_required, format_date, format_datetime

book_authors_bp = Blueprint('authors', __name__)

# ============= AUTHOR ENDPOINTS (Admin only for create/delete) =============
@book_authors_bp.get("/authors")
def list_authors():
    with SessionLocal() as s:
        authors = s.query(Author).all()
        return jsonify([
            {
                "id": a.id,
                "name": a.name,
                "bio": a.bio,
                "birth_date": format_date(a.birth_date),
                "nationality": a.nationality,
                "created_at": format_datetime(a.created_at)
            }
            for a in authors
        ]), 200

@book_authors_bp.get("/authors/<int:author_id>")
def get_author(author_id: int):
    with SessionLocal() as s:
        author = s.query(Author).options(joinedload(Author.books)).filter(Author.id == author_id).first()
        if not author:
            return {"error": "author not found"}, 404
        return {
            "id": author.id,
            "name": author.name,
            "bio": author.bio,
            "birth_date": format_date(author.birth_date),
            "nationality": author.nationality,
            "created_at": format_datetime(author.created_at),
            "books": [{"id": b.id, "title": b.title, "isbn": b.isbn} for b in author.books]
        }, 200

@book_authors_bp.post("/authors")
@admin_required
def create_author():
    data = request.get_json(force=True)
    name = data.get("name")
    bio = data.get("bio")
    birth_date = data.get("birth_date")
    nationality = data.get("nationality")

    if not name:
        return {"error": "name required"}, 400

    try:
        birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date() if birth_date else None
    except ValueError:
        return {"error": "birth_date must be in YYYY-MM-DD format"}, 400

    with SessionLocal() as s:
        try:
            author = Author(name=name, bio=bio, birth_date=birth_date_obj, nationality=nationality)
            s.add(author)
            s.commit()
            s.refresh(author)
            return {
                "id": author.id,
                "name": author.name,
                "bio": author.bio,
                "birth_date": format_date(author.birth_date),
                "nationality": author.nationality,
                "created_at": format_datetime(author.created_at)
            }, 201
        except IntegrityError:
            s.rollback()
            return {"error": "author name already exists"}, 409

@book_authors_bp.delete("/authors/<int:author_id>")
@admin_required
def delete_author(author_id: int):
    with SessionLocal() as s:
        author = s.query(Author).filter(Author.id == author_id).first()
        if not author:
            return {"error": "author not found"}, 404
        s.delete(author)
        s.commit()
        return {"message": "author deleted"}, 200


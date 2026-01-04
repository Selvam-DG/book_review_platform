from flask import Blueprint, request, jsonify

from sqlalchemy.exc import IntegrityError

from db import SessionLocal
from models import Genre
from utils.auth_utils import admin_required, format_datetime

book_genres_bp = Blueprint('genres', __name__)

# ============= GENRE ENDPOINTS (Admin only for create/delete) =============
@book_genres_bp.get("/genres")
def list_genres():
    with SessionLocal() as s:
        genres = s.query(Genre).all()
        return jsonify([
            {
                "id": g.id,
                "name": g.name,
                "description": g.description,
                "created_at": format_datetime(g.created_at)
            }
            for g in genres
        ]), 200

@book_genres_bp.post("/genres")
@admin_required
def create_genre():
    data = request.get_json(force=True)
    name = data.get("name")
    description = data.get("description")

    if not name:
        return {"error": "name required"}, 400

    with SessionLocal() as s:
        try:
            genre = Genre(name=name, description=description)
            s.add(genre)
            s.commit()
            s.refresh(genre)
            return {
                "id": genre.id,
                "name": genre.name,
                "description": genre.description,
                "created_at": format_datetime(genre.created_at)
            }, 201
        except IntegrityError:
            s.rollback()
            return {"error": "genre name already exists"}, 409

@book_genres_bp.delete("/genres/<int:genre_id>")
@admin_required
def delete_genre(genre_id: int):
    with SessionLocal() as s:
        genre = s.query(Genre).filter(Genre.id == genre_id).first()
        if not genre:
            return {"error": "genre not found"}, 404
        s.delete(genre)
        s.commit()
        return {"message": "genre deleted"}, 200


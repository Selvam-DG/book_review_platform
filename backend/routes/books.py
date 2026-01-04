from flask import Blueprint,  jsonify, request
from db import SessionLocal
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from models import Book, Review, Author, Genre
from utils.auth_utils import admin_required, format_datetime, format_date
from datetime import datetime

books_bp = Blueprint("books", __name__)
# ============= BOOK ENDPOINTS (Admin only for create/delete) =============
@books_bp.get("/books")
def list_books():
    with SessionLocal() as s:
        books = s.query(Book).options(
            joinedload(Book.author),
            joinedload(Book.genre)
        ).all()
        return jsonify([
            {
                "id": b.id,
                "title": b.title,
                "author": {"id": b.author.id, "name": b.author.name},
                "genre": {"id": b.genre.id, "name": b.genre.name},
                "isbn": b.isbn,
                "publication_date": format_date(b.publication_date),
                "pages": b.pages,
                "language": b.language,
                "publisher": b.publisher,
                "description": b.description,
                "created_at": format_datetime(b.created_at)
            }
            for b in books
        ]), 200

@books_bp.get("/books/<int:book_id>")
def get_book(book_id: int):
    with SessionLocal() as s:
        book = s.query(Book).options(
            joinedload(Book.author),
            joinedload(Book.genre),
            joinedload(Book.reviews).joinedload(Review.user)
        ).filter(Book.id == book_id).first()

        if not book:
            return {"error": "book not found"}, 404

        return {
            "id": book.id,
            "title": book.title,
            "author": {"id": book.author.id, "name": book.author.name},
            "genre": {"id": book.genre.id, "name": book.genre.name},
            "isbn": book.isbn,
            "publication_date": format_date(book.publication_date),
            "pages": book.pages,
            "language": book.language,
            "publisher": book.publisher,
            "description": book.description,
            "created_at": format_datetime(book.created_at),
            "reviews": [
                {
                    "id": r.id,
                    "user": {"id": r.user.id, "username": r.user.username},
                    "rating": r.rating,
                    "review_text": r.review_text,
                    "helpful_count": r.helpful_count,
                    "created_at": format_datetime(r.created_at)
                }
                for r in book.reviews
            ]
        }, 200

@books_bp.post("/books")
@admin_required
def create_book():
    data = request.get_json(force=True)
    title = data.get("title")
    author_id = data.get("author_id")
    genre_id = data.get("genre_id")
    isbn = data.get("isbn")
    publication_date = data.get("publication_date")
    pages = data.get("pages")
    language = data.get("language")
    publisher = data.get("publisher")
    description = data.get("description")

    if not title or not author_id or not genre_id:
        return {"error": "title, author_id, and genre_id required"}, 400

    try:
        pub_date_obj = datetime.strptime(publication_date, '%Y-%m-%d').date() if publication_date else None
    except ValueError:
        return {"error": "publication_date must be in YYYY-MM-DD format"}, 400

    with SessionLocal() as s:
        author = s.query(Author).filter(Author.id == author_id).first()
        if not author:
            return {"error": "author not found"}, 404

        genre = s.query(Genre).filter(Genre.id == genre_id).first()
        if not genre:
            return {"error": "genre not found"}, 404

        try:
            book = Book(
                title=title,
                author_id=author_id,
                genre_id=genre_id,
                isbn=isbn,
                publication_date=pub_date_obj,
                pages=pages,
                language=language,
                publisher=publisher,
                description=description
            )
            s.add(book)
            s.commit()
            s.refresh(book)
            return {
                "id": book.id,
                "title": book.title,
                "author_id": book.author_id,
                "genre_id": book.genre_id,
                "isbn": book.isbn,
                "publication_date": format_date(book.publication_date),
                "pages": book.pages,
                "language": book.language,
                "publisher": book.publisher,
                "description": book.description,
                "created_at": format_datetime(book.created_at)
            }, 201
        except IntegrityError:
            s.rollback()
            return {"error": "isbn already exists"}, 409

@books_bp.delete("/books/<int:book_id>")
@admin_required
def delete_book(book_id: int):
    with SessionLocal() as s:
        book = s.query(Book).filter(Book.id == book_id).first()
        if not book:
            return {"error": "book not found"}, 404
        s.delete(book)
        s.commit()
        return {"message": "book deleted"}, 200


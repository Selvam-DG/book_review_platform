
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import joinedload
from models import Base, Book, Review
from db import engine, SessionLocal

app = Flask(__name__)
CORS(app)

# Health
@app.get("/health")
def health():
    return {"status": "ok"}

# GET /books
@app.get("/books")
def list_books():
    with SessionLocal() as s:
        books = s.query(Book).all()
        return jsonify([
            {"id": b.id, "title": b.title, "author": b.author, "description": b.description}
            for b in books
        ])

# GET /books/<id>
@app.get("/books/<int:book_id>")
def get_book(book_id: int):
    with SessionLocal() as s:
        b = s.query(Book).options(joinedload(Book.reviews)).filter(Book.id == book_id).first()
        if not b:
            return {"error": "not found"}, 404
        return {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "description": b.description,
            "reviews": [{"id": r.id, "rating": r.rating, "comment": r.comment} for r in b.reviews]
        }

# POST /reviews
@app.post("/reviews")
def add_review():
    data = request.get_json(force=True)
    book_id = data.get("book_id")
    rating  = data.get("rating")
    comment = data.get("comment", "")

    if not isinstance(book_id, int) or not isinstance(rating, int) or rating < 1 or rating > 5:
        return {"error": "book_id (int), rating (1..5) required"}, 400

    with SessionLocal() as s:
        b = s.query(Book).filter(Book.id == book_id).first()
        if not b:
            return {"error": "book not found"}, 404
        r = Review(book_id=book_id, rating=rating, comment=comment)
        s.add(r)
        s.commit()
        return {"id": r.id, "book_id": book_id, "rating": rating, "comment": comment}, 201

if __name__ == "__main__":
    # Auto-create tables if not present (safe in dev)
    Base.metadata.create_all(engine)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))

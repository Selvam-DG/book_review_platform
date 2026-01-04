from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from db import SessionLocal
from models import Review, User, Book
from utils.auth_utils import  format_datetime, token_required, require_active_user

book_reviews_bp = Blueprint('reviews', __name__)

# ============= REVIEW ENDPOINTS (User authenticated) =============
@book_reviews_bp.get("/reviews")
def list_reviews():
    with SessionLocal() as s:
        reviews = s.query(Review).options(
            joinedload(Review.book),
            joinedload(Review.user)
        ).all()
        return jsonify([
            {
                "id": r.id,
                "book": {"id": r.book.id, "title": r.book.title},
                "user": {"id": r.user.id, "username": r.user.username},
                "rating": r.rating,
                "review_text": r.review_text,
                "helpful_count": r.helpful_count,
                "created_at": format_datetime(r.created_at)
            }
            for r in reviews
        ]), 200

@book_reviews_bp.get("/reviews/<int:review_id>")
def get_review(review_id: int):
    with SessionLocal() as s:
        review = s.query(Review).options(
            joinedload(Review.book),
            joinedload(Review.user)
        ).filter(Review.id == review_id).first()

        if not review:
            return {"error": "review not found"}, 404

        return {
            "id": review.id,
            "book": {"id": review.book.id, "title": review.book.title},
            "user": {"id": review.user.id, "username": review.user.username},
            "rating": review.rating,
            "review_text": review.review_text,
            "helpful_count": review.helpful_count,
            "created_at": format_datetime(review.created_at)
        }, 200

@book_reviews_bp.post("/reviews")
@token_required
@require_active_user
def create_review():
    data = request.get_json(force=True)
    book_id = data.get("book_id")
    rating = data.get("rating")
    review_text = data.get("review_text", "")

    if not isinstance(book_id, int) or not isinstance(rating, int):
        return {"error": "book_id and rating (int) required"}, 400
    if rating < 1 or rating > 5:
        return {"error": "rating must be between 1 and 5"}, 400

    with SessionLocal() as s:
        book = s.query(Book).filter(Book.id == book_id).first()
        if not book:
            return {"error": "book not found"}, 404

        user = s.query(User).filter(User.id == request.user_id).first()
        if not user:
            return {"error": "user not found"}, 404

        try:
            review = Review(book_id=book_id, user_id=request.user_id, rating=rating, review_text=review_text)
            s.add(review)
            s.commit()
            s.refresh(review)
            return {
                "id": review.id,
                "book_id": review.book_id,
                "user_id": review.user_id,
                "rating": review.rating,
                "review_text": review.review_text,
                "helpful_count": review.helpful_count,
                "created_at": format_datetime(review.created_at)
            }, 201
        except IntegrityError:
            s.rollback()
            return {"error": "you already reviewed this book"}, 409

@book_reviews_bp.put("/reviews/<int:review_id>")
@token_required
@require_active_user
def update_review(review_id: int):
    data = request.get_json(force=True)

    with SessionLocal() as s:
        review = s.query(Review).filter(Review.id == review_id).first()
        if not review:
            return {"error": "review not found"}, 404

        if review.user_id != request.user_id and not request.is_admin:
            return {"error": "you can only edit your own reviews"}, 403

        if "rating" in data:
            if not isinstance(data["rating"], int) or data["rating"] < 1 or data["rating"] > 5:
                return {"error": "rating must be an integer between 1 and 5"}, 400
            review.rating = data["rating"]

        if "review_text" in data:
            review.review_text = data["review_text"]

        if "helpful_count" in data and request.is_admin:
            review.helpful_count = data["helpful_count"]

        s.commit()
        s.refresh(review)

        return {
            "id": review.id,
            "book_id": review.book_id,
            "user_id": review.user_id,
            "rating": review.rating,
            "review_text": review.review_text,
            "helpful_count": review.helpful_count,
            "created_at": format_datetime(review.created_at)
        }, 200

@book_reviews_bp.delete("/reviews/<int:review_id>")
@token_required
@require_active_user
def delete_review(review_id: int):
    with SessionLocal() as s:
        review = s.query(Review).filter(Review.id == review_id).first()
        if not review:
            return {"error": "review not found"}, 404

        if review.user_id != request.user_id and not request.is_admin:
            return {"error": "you can only delete your own reviews"}, 403

        s.delete(review)
        s.commit()
        return {"message": "review deleted"}, 200


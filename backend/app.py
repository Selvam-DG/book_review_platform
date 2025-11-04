import os
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from models import Base, Author, Genre, User, Book, Review
from db import engine, SessionLocal
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "")

# Helper function to format dates
def format_date(date_obj):
    return date_obj.strftime('%Y-%m-%d') if date_obj else None

def format_datetime(dt_obj):
    return dt_obj.strftime('%Y-%m-%d %H:%M:%S') if dt_obj else None

# ============= AUTH HELPERS =============
def generate_token(user_id, is_admin=False, expires_in_days=7):
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(days=expires_in_days)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_token_from_request():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    try:
        return auth_header.split(' ')[1]
    except IndexError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        if not token:
            return {"error": "missing authorization token"}, 401
        
        payload = verify_token(token)
        if not payload:
            return {"error": "invalid or expired token"}, 401
        
        request.user_id = payload['user_id']
        request.is_admin = payload.get('is_admin', False)
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        if not token:
            return {"error": "missing authorization token"}, 401
        
        payload = verify_token(token)
        if not payload:
            return {"error": "invalid or expired token"}, 401
        
        if not payload.get('is_admin', False):
            return {"error": "admin access required"}, 403
        
        request.user_id = payload['user_id']
        request.is_admin = payload['is_admin']
        return f(*args, **kwargs)
    return decorated

# ============= HEALTH =============
@app.get("/health")
def health():
    return {"status": "ok"}, 200

# ============= AUTH ENDPOINTS =============
@app.post("/auth/register-request")
def register_request():
    """User requests registration - sent to admin"""
    data = request.get_json(force=True)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "username, email, and password required"}, 400

    with SessionLocal() as s:
        existing = s.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing:
            return {"error": "username or email already exists"}, 409
        
        return {
            "message": "registration request submitted - awaiting admin approval",
            "requested_username": username,
            "requested_email": email
        }, 202

@app.post("/auth/login")
def login():
    """User login with username and password"""
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "username and password required"}, 400

    with SessionLocal() as s:
        user = s.query(User).filter(User.username == username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {"error": "invalid username or password"}, 401
        
        token = generate_token(user.id, is_admin=user.is_admin)
        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }
        }, 200

# ============= ADMIN USER MANAGEMENT =============
@app.post("/admin/users")
@admin_required
def admin_create_user():
    """Admin creates a new user"""
    data = request.get_json(force=True)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    is_admin = data.get("is_admin", False)

    if not username or not email or not password:
        return {"error": "username, email, and password required"}, 400

    with SessionLocal() as s:
        existing = s.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing:
            return {"error": "username or email already exists"}, 409
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=is_admin
        )
        s.add(user)
        s.commit()
        s.refresh(user)
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": format_datetime(user.created_at)
        }, 201

@app.get("/admin/users")
@admin_required
def admin_list_users():
    """Admin lists all users"""
    with SessionLocal() as s:
        users = s.query(User).all()
        return jsonify([
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "is_admin": u.is_admin,
                "created_at": format_datetime(u.created_at)
            }
            for u in users
        ]), 200

@app.delete("/admin/users/<int:user_id>")
@admin_required
def admin_delete_user(user_id: int):
    """Admin deletes a user"""
    with SessionLocal() as s:
        user = s.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "user not found"}, 404
        s.delete(user)
        s.commit()
        return {"message": "user deleted"}, 200

# ============= AUTHOR ENDPOINTS (Admin only for create/delete) =============
@app.get("/authors")
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

@app.get("/authors/<int:author_id>")
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

@app.post("/authors")
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

@app.delete("/authors/<int:author_id>")
@admin_required
def delete_author(author_id: int):
    with SessionLocal() as s:
        author = s.query(Author).filter(Author.id == author_id).first()
        if not author:
            return {"error": "author not found"}, 404
        s.delete(author)
        s.commit()
        return {"message": "author deleted"}, 200

# ============= GENRE ENDPOINTS (Admin only for create/delete) =============
@app.get("/genres")
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

@app.post("/genres")
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

@app.delete("/genres/<int:genre_id>")
@admin_required
def delete_genre(genre_id: int):
    with SessionLocal() as s:
        genre = s.query(Genre).filter(Genre.id == genre_id).first()
        if not genre:
            return {"error": "genre not found"}, 404
        s.delete(genre)
        s.commit()
        return {"message": "genre deleted"}, 200

# ============= BOOK ENDPOINTS (Admin only for create/delete) =============
@app.get("/books")
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

@app.get("/books/<int:book_id>")
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

@app.post("/books")
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

@app.delete("/books/<int:book_id>")
@admin_required
def delete_book(book_id: int):
    with SessionLocal() as s:
        book = s.query(Book).filter(Book.id == book_id).first()
        if not book:
            return {"error": "book not found"}, 404
        s.delete(book)
        s.commit()
        return {"message": "book deleted"}, 200

# ============= REVIEW ENDPOINTS (User authenticated) =============
@app.get("/reviews")
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

@app.get("/reviews/<int:review_id>")
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

@app.post("/reviews")
@token_required
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

@app.put("/reviews/<int:review_id>")
@token_required
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

@app.delete("/reviews/<int:review_id>")
@token_required
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

# ============= ERROR HANDLER =============
@app.errorhandler(404)
def not_found(e):
    return {"error": "endpoint not found"}, 404

@app.errorhandler(500)
def server_error(e):
    return {"error": "internal server error"}, 500

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
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
from routes.auth import auth_bp
from routes.admin_users import admin_users_bp
from routes.books import books_bp
from routes.book_authors import book_authors_bp
from routes.book_genres import book_genres_bp
from routes.book_reviews import book_reviews_bp
from routes.book_images import book_images_bp
from routes.book_suggestions import book_suggestions_bp
from routes.book_suggestions_admin import book_suggestions_admin_bp
from utils.auth_utils import admin_required
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "")


# ============= HEALTH =============
@app.get("/health")
def health():
    return {"status": "ok"}, 200

# ============= ERROR HANDLER =============
@app.errorhandler(404)
def not_found(e):
    return {"error": "endpoint not found"}, 404

@app.errorhandler(500)
def server_error(e):
    return {"error": "internal server error"}, 500

app.register_blueprint(auth_bp)
app.register_blueprint(admin_users_bp)
app.register_blueprint(books_bp)
app.register_blueprint(book_authors_bp)
app.register_blueprint(book_images_bp)
app.register_blueprint(book_genres_bp)
app.register_blueprint(book_reviews_bp)
app.register_blueprint(book_suggestions_bp)
app.register_blueprint(book_suggestions_admin_bp)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
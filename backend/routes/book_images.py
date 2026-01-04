from flask import Blueprint, request
from models import Book, BookImage
from db import SessionLocal
from services.oci_storage import upload_book_image
from utils.auth_utils import admin_required

book_images_bp = Blueprint("book_images", __name__)

@book_images_bp.post("/books/<int:book_id>/images")
@admin_required
def upload_book_images(book_id):
    files = request.files.getlist("images")

    if not files:
        return {"error": "no images provided"}, 400

    with SessionLocal() as s:
        book = s.query(Book).filter(Book.id == book_id).first()
        if not book:
            return {"error": "book not found"}, 404

        uploaded = []
        for file in files:
            object_name, object_url = upload_book_image(file, book_id)

            image = BookImage(
                book_id=book_id,
                object_name=object_name,
                object_url=object_url
            )
            s.add(image)
            uploaded.append(image)

        s.commit()

        return {
            "images": [
                {"id": img.id, "url": img.object_url}
                for img in uploaded
            ]
        }, 201

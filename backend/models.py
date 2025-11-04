from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Date, UniqueConstraint
from datetime import datetime
from typing import Optional

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    birth_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    books: Mapped[list["Book"]] = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    books: Mapped[list["Book"]] = relationship(
        "Book",
        back_populates="genre"
    )

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="CASCADE"), nullable=False)
    isbn: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)
    publication_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    pages: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    publisher: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="books"
    )

    genre: Mapped["Genre"] = relationship(
        "Genre",
        back_populates="books"
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="book",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (UniqueConstraint('book_id', 'user_id', name='unique_book_user_review'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    helpful_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    book: Mapped["Book"] = relationship(
        "Book",
        back_populates="reviews"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews"
    )

    def __repr__(self):
        return f"<Review(id={self.id}, book_id={self.book_id}, user_id={self.user_id}, rating={self.rating})>"
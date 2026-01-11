import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BooksAPI } from "../api/books";
import BooksHeaderStats from "../components/books/BooksHeaderStats";
import BooksFilters from "../components/books/BooksFilters";
import BooksGrid from "../components/books/BooksGrid";
import type {  BookCard, BookStats } from "../types";

export default function BooksPage() {
  const [books, setBooks] = useState<BookCard[]>([]);
  const [filtered, setFiltered] = useState<BookCard[]>([]);
  const [filters, setFilters] = useState({
    genre: "",
    author: "",
    sort: "popular"
  });
  const navigate = useNavigate();

  const [stats, setStats] = useState<BookStats>({
    total_books: 0,
    total_genres: 0,
    max_reviews: 0,
    user_reviews: 0,
  });


  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    const raw = await BooksAPI.list();

    const cards: BookCard[] = raw.map((b) => ({
      id: b.id,
      title: b.title,
      author: b.author,
      genre: b.genre,
      cover_url:
        b.images?.find((i) => i.is_cover)?.object_url ||
        b.images?.[0]?.object_url ||
        "/placeholder-book.png",
      avg_rating: b.avg_rating ?? 0,
      reviews_count: b.reviews_count ?? 0,
    }));

    setBooks(cards);
    setFiltered(cards);

    setStats({
      total_books: raw.length,
      total_genres: new Set(raw.map((b) => b.genre.name)).size,
      max_reviews: Math.max(...cards.map((c) => c.reviews_count), 0),
      user_reviews: 0
    });
  };

  const applyFilters = () => {
    let out = [...books];

    if (filters.genre) {
      out = out.filter((b) => b.genre.name === filters.genre);
    }
    if (filters.author) {
      out = out.filter((b) => b.author.name === filters.author);
    }
    if (filters.sort === "rating") {
      out = out.sort((a, b) => b.avg_rating - a.avg_rating);
    } else if (filters.sort === "new") {
      out = out.sort((a, b) => b.id - a.id);
    } else {
      out = out.sort((a, b) => b.reviews_count - a.reviews_count);
    }

    setFiltered(out);
  };

  useEffect(applyFilters, [filters, books]);

  return (
    <div className="max-w-7xl mx-auto p-6 relative">
      <BooksHeaderStats stats={{
        total_books: books.length,
        total_genres: new Set(books.map((b) => b.genre.name)).size,
        max_reviews: Math.max(...books.map((b) => b.reviews_count), 0),
        user_reviews: 0,
      }}/>

      <BooksFilters
        genres={[...new Set(books.map((b) => b.genre.name))]}
        authors={[...new Set(books.map((b) => b.author.name))]}
        onChange={(f) => setFilters((prev) => ({ ...prev, ...f }))}
      />

      <BooksGrid books={filtered} onSelect={(id) => navigate(`/books/${id}`)} />
    </div>
  );
}

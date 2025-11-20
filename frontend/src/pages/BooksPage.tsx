import { useState, useEffect } from "react";
import { Star, AlertCircle, Loader } from "lucide-react";
import { fetchJSON, postJSON } from "../api";
import type { Book, BookDetail, User } from "../types";

interface BooksPageProps {
  token?: string;
  user?: User;
}

export default function BooksPage({ token, user }: BooksPageProps) {
  const [books, setBooks] = useState<Book[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [detail, setDetail] = useState<BookDetail | null>(null);
  const [rating, setRating] = useState(5);
  const [reviewText, setReviewText] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadBooks();
  }, []);

  useEffect(() => {
    if (selected !== null) {
      loadBookDetail(selected);
    }
  }, [selected]);

  const loadBooks = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await fetchJSON<Book[]>("/books", token);
      setBooks(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const loadBookDetail = async (bookId: number) => {
    try {
      const data = await fetchJSON<BookDetail>(`/books/${bookId}`, token);
      setDetail(data);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleSubmitReview = async (e: React.MouseEvent) => {
    e.preventDefault();

    if (!token || !user || !selected) {
      setError("Please login to submit a review");
      return;
    }

    if (!reviewText.trim()) {
      setError("Please write a review");
      return;
    }

    try {
      setSubmitting(true);
      setError("");
      await postJSON(
        "/reviews",
        {
          book_id: selected,
          user_id: user.id,
          rating,
          review_text: reviewText,
        },
        token
      );
      setReviewText("");
      setRating(5);
      await loadBookDetail(selected);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader className="mx-auto mb-4 animate-spin text-indigo-600" size={40} />
          <p className="text-gray-600">Loading books...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">Browse Books</h1>

      {error && (
        <div className="mb-4 p-4 bg-red-100 text-red-800 rounded-lg flex gap-2">
          <AlertCircle size={20} className="flex-shrink-0" />
          <p>{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Books List */}
        <div className="md:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-4 sticky top-20">
            <h2 className="font-semibold mb-3 text-gray-900">Book List</h2>
            <ul className="divide-y max-h-96 overflow-y-auto">
              {books.length === 0 ? (
                <li className="p-3 text-gray-500 text-center">No books found</li>
              ) : (
                books.map((b) => (
                  <li
                    key={b.id}
                    className={`p-3 cursor-pointer hover:bg-gray-50 transition ${
                      selected === b.id ? "bg-blue-50 border-l-4 border-indigo-600" : ""
                    }`}
                    onClick={() => setSelected(b.id)}
                  >
                    <div className="font-medium text-sm text-gray-900 truncate">
                      {b.title}
                    </div>
                    <div className="text-xs text-gray-500 truncate">
                      {b.author.name}
                    </div>
                  </li>
                ))
              )}
            </ul>
          </div>
        </div>

        {/* Book Details and Reviews */}
        <div className="md:col-span-2">
          {detail ? (
            <div className="space-y-4">
              {/* Book Info */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-2xl font-semibold mb-2 text-gray-900">
                  {detail.title}
                </h2>
                <p className="text-gray-600 mb-2">by {detail.author.name}</p>
                {detail.author.bio && (
                  <p className="text-sm text-gray-500 mb-3">{detail.author.bio}</p>
                )}

                <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-4">
                  <span>📚 Genre: {detail.genre.name}</span>
                  {detail.pages && <span>📖 {detail.pages} pages</span>}
                  {detail.language && <span>🌐 {detail.language}</span>}
                </div>

                {detail.isbn && (
                  <p className="text-xs text-gray-500 mb-3">
                    ISBN: {detail.isbn}
                  </p>
                )}
                {detail.publisher && (
                  <p className="text-xs text-gray-500 mb-3">
                    Publisher: {detail.publisher}
                  </p>
                )}

                {detail.description && (
                  <p className="mt-4 text-gray-700 leading-relaxed">
                    {detail.description}
                  </p>
                )}
              </div>

              {/* Reviews */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="font-semibold mb-4 text-gray-900">
                  Reviews ({detail.reviews.length})
                </h3>

                {detail.reviews.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">
                    No reviews yet. Be the first to review!
                  </p>
                ) : (
                  <div className="space-y-3">
                    {detail.reviews.map((r) => (
                      <div
                        key={r.id}
                        className="p-4 border rounded-lg bg-gray-50 hover:bg-gray-100 transition"
                      >
                        <div className="flex justify-between items-start mb-2">
                          <div className="font-medium text-sm text-gray-900">
                            {r.user.username}
                          </div>
                          <div className="flex items-center gap-1">
                            {[...Array(5)].map((_, i) => (
                              <Star
                                key={i}
                                size={14}
                                className={`${
                                  i < r.rating
                                    ? "fill-yellow-400 text-yellow-400"
                                    : "text-gray-300"
                                }`}
                              />
                            ))}
                          </div>
                        </div>
                        {r.review_text && (
                          <p className="text-sm text-gray-700 mb-2">
                            {r.review_text}
                          </p>
                        )}
                        <div className="text-xs text-gray-400">
                          👍 {r.helpful_count} found this helpful
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Add Review */}
              {token && user ? (
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="font-semibold mb-4 text-gray-900">
                    Add Your Review
                  </h3>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm font-medium mb-1 text-gray-700">
                        Rating
                      </label>
                      <select
                        className="border rounded px-3 py-2 w-full text-gray-700"
                        value={rating}
                        onChange={(e) => setRating(parseInt(e.target.value))}
                      >
                        {[1, 2, 3, 4, 5].map((n) => (
                          <option key={n} value={n}>
                            {n} ⭐
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1 text-gray-700">
                        Review
                      </label>
                      <textarea
                        className="border rounded px-3 py-2 w-full text-gray-700"
                        rows={4}
                        placeholder="Share your thoughts about this book..."
                        value={reviewText}
                        onChange={(e) => setReviewText(e.target.value)}
                      />
                    </div>
                    <button
                      onClick={handleSubmitReview}
                      disabled={submitting}
                      className="w-full px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:opacity-50 transition font-medium"
                    >
                      {submitting ? "Submitting..." : "Submit Review"}
                    </button>
                  </div>
                </div>
              ) : (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                  <p className="text-blue-900">
                    Login to submit a review
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-gray-50 rounded-lg p-12 text-center">
              <p className="text-gray-500 text-lg">
                Select a book to view details
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
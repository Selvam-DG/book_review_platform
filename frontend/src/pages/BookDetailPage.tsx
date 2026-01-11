import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { BooksAPI } from "../api/books";
import { ReviewsAPI } from "../api/reviews";
import { useAuth } from "../auth/AuthContext";

import ReviewItem from "../components/reviews/ReviewItem";
import ReviewForm from "../components/reviews/ReviewForm";

import type { Book, Review } from "../types";
import { timeAgo } from "../utils/timeAgo";
const REVIEWS_PER_PAGE = 3;


export default function BookDetailPage() {
  const { id } = useParams();
  const { user, token } = useAuth();

  const [book, setBook] = useState<Book | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [page, setPage] = useState(1);

  const [editingReview, setEditingReview] = useState<Review | null>(null);

  useEffect(() => {
    loadBook();
  }, [id]);

  const loadBook = async () => {
    const data = await BooksAPI.detail(Number(id));

    setBook(data);
    setReviews(data.reviews?.slice(0, REVIEWS_PER_PAGE) ?? []);
    setPage(1);
  };

  const loadMoreReviews = () => {
    if (!book?.reviews) return;

    const start = page * REVIEWS_PER_PAGE;
    const end = start + REVIEWS_PER_PAGE;

    const nextChunk = book.reviews.slice(start, end);

    if (nextChunk.length > 0) {
      setReviews((prev) => [...prev, ...nextChunk]);
      setPage(page + 1);
    }
  };

  if (!book) return <div className="p-6">Loading...</div>;

  /** ADD REVIEW */
  const handleAdd = async (payload: { rating: number; review_text: string }) => {
    if (!user) return alert("Login required");

    await ReviewsAPI.create({
      book_id: Number(id),
      rating: payload.rating,
      review_text: payload.review_text,
    });

    await loadBook();
  };

  /** UPDATE REVIEW */
  const handleUpdate = async (payload: { rating: number; review_text: string }) => {
    if (!editingReview) return;

    await ReviewsAPI.update(editingReview.id, payload);

    setEditingReview(null);
    await loadBook();
  };

  /** DELETE REVIEW */
  const handleDelete = async (review_id: number) => {
    if (!confirm("Delete your review?")) return;

    await ReviewsAPI.delete(review_id);
    await loadBook();
  };

  if (!book) return <div className="p-6">Loading...</div>;

  const myReview = user
    ? book.reviews ?.find((r) => r.user.id === user.id)
    : null;

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Cover image */}
        <div className="col-span-1">
          <img
            src={
              book.images?.find((i) => i.is_cover)?.object_url ||
              book.images?.[0]?.object_url ||
              "/placeholder-book.png"
            }
            className="rounded shadow w-full"
          />
        </div>

        {/* Book Info */}
        <div className="col-span-2 space-y-4">
          <h1 className="text-3xl font-bold">{book.title}</h1>
          <p className="text-gray-700 text-lg">{book.author.name}</p>
          <p className="text-gray-500">{book.genre.name}</p>

          <div className="text-gray-600 space-y-1">
            <p><span className="font-semibold">ISBN:</span> {book.isbn || "N/A"}</p>
            <p><span className="font-semibold">Publisher:</span> {book.publisher || "N/A"}</p>
            <p><span className="font-semibold">Pages:</span> {book.pages || "N/A"}</p>
            <p><span className="font-semibold">Language:</span> {book.language || "N/A"}</p>
            <p><span className="font-semibold">Publication Date:</span> {book.publication_date || "N/A"}</p>
          </div>

          <p className="text-gray-800 mt-4">{book.description}</p>
        </div>
      </div>
      {/* --- MY REVIEW SECTION --- */}
      {user && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">My Review</h2>

          {/* If user has NOT reviewed */}
          {!myReview && !editingReview && (
            <ReviewForm onSubmit={handleAdd} />
          )}

          {/* If editing their review */}
          {editingReview && (
            <ReviewForm
              initial={editingReview}
              onSubmit={handleUpdate}
              onCancel={() => setEditingReview(null)}
            />
          )}

          {/* If user has a review already */}
          {myReview && !editingReview && (
            <ReviewItem
              review={myReview}
              owned={true}
              onEdit={() => setEditingReview(myReview)}
              onDelete={() => handleDelete(myReview.id)}
            />
          )}
        </div>
      )}

      {/* Reviews Section */}
      <div className="space-y-4">
        {book.reviews && (
            <h2 className="text-2xl font-semibold">
                Reviews ({book.reviews.length})
            </h2>
        )}

        {reviews.length === 0 && (
          <p className="text-gray-500">No reviews yet.</p>
        )}

        {reviews.map((r) => (
           <ReviewItem
            key={r.id}
            review={r}
            owned={user?.id === r.user.id}
            onEdit={() => setEditingReview(r)}
            onDelete={() => handleDelete(r.id)}
          />
        ))}

        {/* Show more button */}
        {book.reviews && reviews.length < book.reviews.length && (
          <button
            onClick={loadMoreReviews}
            className="px-4 py-2 bg-indigo-600 text-white rounded"
          >
            Show More Reviews
          </button>
        )}
      </div>
    </div>
  );
}

import type { Review } from "../../types";
import { timeAgo } from "../../utils/timeAgo"

export default function ReviewItem({
  review,
  owned,
  onEdit,
  onDelete,
}: {
  review: Review;
  owned: boolean;
  onEdit: () => void;
  onDelete: () => void;
}) {
  return (
    <div className="border rounded p-4 mb-3">
      <div className="flex justify-between items-center">
        <p className="font-semibold">{review.user.username}</p>
        <p className="text-gray-500 text-sm">{review.created_at && timeAgo(review.created_at)}</p>
      </div>

      <p className="text-yellow-600 font-medium">Rating: {review.rating}</p>
      <p className="mt-2">{review.review_text}</p>

      {owned && (
        <div className="flex gap-3 mt-3">
          <button onClick={onEdit} className="text-indigo-600 font-semibold">
            Edit
          </button>
          <button onClick={onDelete} className="text-red-600 font-semibold">
            Delete
          </button>
        </div>
      )}
    </div>
  );
}

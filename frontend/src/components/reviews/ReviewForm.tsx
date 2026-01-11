import { useState } from "react";
import type { Review } from "../../types";

export default function ReviewForm({
  initial,
  onSubmit,
  onCancel,
}: {
  initial?: Review | null;
  onSubmit: (payload: { rating: number; review_text: string }) => void;
  onCancel?: () => void;
}) {
  const [rating, setRating] = useState(initial?.rating ?? 5);
  const [text, setText] = useState(initial?.review_text ?? "");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ rating, review_text: text });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 border p-4 rounded">
      <div>
        <label className="font-semibold">Rating</label>
        <select
          value={rating}
          onChange={(e) => setRating(Number(e.target.value))}
          className="border rounded p-1 ml-2"
        >
          {[5, 4, 3, 2, 1].map((r) => (
            <option key={r}>{r}</option>
          ))}
        </select>
      </div>

      <textarea
        className="border rounded p-2 w-full"
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Write your review..."
      />

      <div className="flex gap-3">
        <button type="submit" className="px-3 py-2 bg-indigo-600 text-white rounded">
          {initial ? "Update Review" : "Submit Review"}
        </button>

        {initial && (
          <button
            type="button"
            onClick={onCancel}
            className="px-3 py-2 bg-gray-300 rounded"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

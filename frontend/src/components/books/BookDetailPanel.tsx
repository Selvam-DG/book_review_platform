import { X } from "lucide-react";
import type { Book } from "../../types";

export default function BookDetailPanel({
  book,
  open,
  onClose,
}: {
  book: Book | null;
  open: boolean;
  onClose: () => void;
}) {
  return (
    <div
      className={`fixed inset-0 bg-black/40 backdrop-blur-sm transition-opacity ${
        open ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
      }`}
      onClick={onClose}
    >
      <div
        className={`absolute right-0 top-0 h-full w-full sm:w-[450px] bg-white shadow-xl transform transition-transform ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-4 flex justify-between items-center border-b">
          <h2 className="text-xl font-semibold">{book?.title}</h2>
          <X className="cursor-pointer" onClick={onClose} />
        </div>

        {!book ? (
          <div className="p-6">Loading...</div>
        ) : (
          <div className="p-6 overflow-y-auto h-full space-y-6">
            <img
              src={
                book.images?.find((i) => i.is_cover)?.object_url ||
                book.images?.[0]?.object_url ||
                "/placeholder-book.png"
              }
              className="rounded shadow w-full"
            />

            <div>
              <p className="text-gray-600">{book.author.name}</p>
              <p className="text-gray-500 text-sm">{book.genre.name}</p>
              <p className="mt-4">{book.description}</p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Reviews</h3>

              {book.reviews?.length === 0 && (
                <p className="text-gray-500">No reviews yet.</p>
              )}

              {book.reviews?.map((r) => (
                <div key={r.id} className="border p-3 rounded mb-3">
                  <p className="font-semibold">{r.user.username}</p>
                  <p className="text-yellow-600 font-medium">Rating: {r.rating}</p>
                  <p>{r.review_text}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

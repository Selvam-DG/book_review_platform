import { Star } from "lucide-react";
import type { BookCard } from "../../types";

export default function BookCard({
  book,
  onSelect,
}: {
  book: BookCard;
  onSelect: () => void;
}) {
  return (
    <div
      onClick={onSelect}
      className="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer overflow-hidden"
    >
      <img
        src={book.cover_url}
        className="h-48 w-full object-cover"
        alt={book.title}
      />

      <div className="p-4">
        <h3 className="font-semibold text-lg truncate">{book.title}</h3>
        <p className="text-sm text-gray-500">{book.author.name}</p>
        <p className="text-xs text-gray-400">{book.genre.name}</p>

        <div className="flex items-center gap-2 mt-2">
          <Star className="text-yellow-400" size={16} />
          <span className="text-sm">
            {book.avg_rating.toFixed(1)}
          </span>
          <span className="text-xs text-gray-400">
            ({book.reviews_count})
          </span>
        </div>
      </div>
    </div>
  );
}

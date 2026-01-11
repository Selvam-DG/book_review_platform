import BookCard from "./BookCard";
import type { BookCard as Card } from "../../types";

export default function BooksGrid({
  books,
  onSelect,
}: {
  books: Card[];
  onSelect: (id: number) => void;
}) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {books.map((b) => (
        <BookCard key={b.id} book={b} onSelect={() => onSelect(b.id)} />
      ))}
    </div>
  );
}

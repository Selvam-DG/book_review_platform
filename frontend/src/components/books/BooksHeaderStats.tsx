import { BookOpen, Layers, Star, User } from "lucide-react";
import type { BookStats } from "../../types";

export default function BooksHeaderStats({ stats }: { stats: BookStats }) {
  const items = [
    { label: "Books", value: stats.total_books, icon: BookOpen },
    { label: "Genres", value: stats.total_genres, icon: Layers },
    { label: "Max Reviews", value: stats.max_reviews, icon: Star },
    { label: "Your Reviews", value: stats.user_reviews, icon: User },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {items.map(({ label, value, icon: Icon }) => (
        <div key={label} className="bg-white rounded-lg shadow p-4 flex items-center gap-3">
          <Icon className="text-indigo-600" />
          <div>
            <div className="text-xl font-bold">{value}</div>
            <div className="text-sm text-gray-500">{label}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

interface Props {
  genres: string[];
  authors: string[];
  onChange: (filters: {
    genre?: string;
    author?: string;
    sort?: string;
  }) => void;
}

export default function BooksFilters({ genres, authors, onChange }: Props) {
  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      <select onChange={(e) => onChange({ genre: e.target.value })}>
        <option value="">All Genres</option>
        {genres.map((g) => (
          <option key={g}>{g}</option>
        ))}
      </select>

      <select onChange={(e) => onChange({ author: e.target.value })}>
        <option value="">All Authors</option>
        {authors.map((a) => (
          <option key={a}>{a}</option>
        ))}
      </select>

      <select onChange={(e) => onChange({ sort: e.target.value })}>
        <option value="popular">Most Reviewed</option>
        <option value="rating">Highest Rated</option>
        <option value="new">Newest</option>
      </select>
    </div>
  );
}

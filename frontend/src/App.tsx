import { useEffect, useState } from "react";
import { fetchJSON, postJSON, apiUrl } from "./api";

type Book = { id: number; title: string; author: string; description?: string };
type Review = { id: number; rating: number; comment?: string };
type BookDetail = Book & { reviews: Review[] };

export default function App() {
  const [books, setBooks] = useState<Book[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [detail, setDetail] = useState<BookDetail | null>(null);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");

  useEffect(() => { fetchJSON<Book[]>("/books").then(setBooks).catch(console.error); }, []);
  useEffect(() => {
    if (selected !== null) fetchJSON<BookDetail>(`/books/${selected}`).then(setDetail).catch(console.error);
  }, [selected]);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Book Review Platform</h1>
        <p className="text-sm text-gray-500 mb-6">API: {apiUrl()}</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1">
            <h2 className="font-semibold mb-2">Books</h2>
            <ul className="divide-y rounded border bg-white">
              {books.map(b => (
                <li key={b.id}
                    className={`p-3 cursor-pointer ${selected===b.id?"bg-blue-50":""}`}
                    onClick={() => setSelected(b.id)}>
                  <div className="font-medium">{b.title}</div>
                  <div className="text-sm text-gray-500">{b.author}</div>
                </li>
              ))}
            </ul>
          </div>

          <div className="md:col-span-2">
            {detail ? (
              <div className="space-y-4">
                <div className="p-4 bg-white border rounded">
                  <h2 className="text-xl font-semibold">{detail.title}</h2>
                  <p className="text-gray-600">by {detail.author}</p>
                  {detail.description && <p className="mt-2">{detail.description}</p>}
                </div>

                <div className="p-4 bg-white border rounded">
                  <h3 className="font-semibold mb-2">Reviews</h3>
                  <ul className="space-y-2">
                    {detail.reviews.length === 0 && <li className="text-gray-500">No reviews yet.</li>}
                    {detail.reviews.map(r => (
                      <li key={r.id} className="p-2 border rounded">
                        <div className="font-medium">Rating: {r.rating}/5</div>
                        {r.comment && <div className="text-sm">{r.comment}</div>}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 bg-white border rounded">
                  <h3 className="font-semibold mb-2">Add Review</h3>
                  <form onSubmit={async e => {
                    e.preventDefault();
                    if (selected === null) return;
                    try {
                      await postJSON("/reviews", { book_id: selected, rating, comment });
                      setComment("");
                      const fresh = await fetchJSON<BookDetail>(`/books/${selected}`);
                      setDetail(fresh);
                    } catch (err) { console.error(err); }
                  }} className="space-y-3">
                    <div>
                      <label className="block text-sm font-medium">Rating</label>
                      <select className="border rounded p-2" value={rating}
                              onChange={e => setRating(parseInt(e.target.value))}>
                        {[1,2,3,4,5].map(n => <option key={n} value={n}>{n}</option>)}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium">Comment</label>
                      <textarea className="border rounded p-2 w-full" rows={3}
                                value={comment} onChange={e => setComment(e.target.value)} />
                    </div>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded" type="submit">Submit</button>
                  </form>
                </div>
              </div>
            ) : (
              <div className="p-4 text-gray-500 border rounded bg-white">Select a book to view details</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}


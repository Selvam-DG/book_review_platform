import { useState } from "react";
import { BooksAPI } from "../../api/books";

export default function SuggestionForm({ onSubmit }: { onSubmit: (payload: any) => Promise<void> }) {
  const [form, setForm] = useState({
    title: "",
    author_name: "",
    genre_name: "",
    isbn: "",
    pages: "",
    publication_date: "",
    publisher: "",
    language: "",
    description: "",
    review_seed_text: "",
    review_seed_rating: 5,
  });

  const [images, setImages] = useState<File[]>([]);
  const [duplicate, setDuplicate] = useState<string | null>(null);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const checkDuplicate = async (title: string) => {
    const books = await BooksAPI.list();
    const exists = books.some((b) => b.title.toLowerCase() === title.toLowerCase());
    setDuplicate(exists ? "A book with this title already exists." : null);
  };

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (name === "title") checkDuplicate(value);
  };

  const submit = async (e: any) => {
    e.preventDefault();
    if (duplicate) return;

    try {
      setSubmitting(true);
      await onSubmit({ ...form, images });
      setMessage({ type: "success", text: "Your suggestion was sent to the admin!" });
      setTimeout(() => setMessage(null), 3000);

      // Reset
      setForm({
        title: "",
        author_name: "",
        genre_name: "",
        isbn: "",
        pages: "",
        publication_date: "",
        publisher: "",
        language: "",
        description: "",
        review_seed_text: "",
        review_seed_rating: 5,
      });
      setImages([]);
    } catch (err: any) {
      setMessage({ type: "error", text: err.message || "Failed to submit suggestion" });
      setTimeout(() => setMessage(null), 3000);
    }

    setSubmitting(false);
  };

  return (
    <form className="space-y-4 border p-4 rounded bg-white" onSubmit={submit}>
      {message && (
        <p className={`text-sm ${message.type === "success" ? "text-green-600" : "text-red-600"}`}>
          {message.text}
        </p>
      )}


      <fieldset className="grid grid-cols-1 gap-4">

        <div className="grid grid-cols-2">    
          <label className="label px-4">Title</label>
          <input required name="title" placeholder="Book Title" className="input border p-1 rounded w-full" onChange={handleChange} value={form.title} />
        </div>

      {duplicate && <p className="text-red-500 text-sm">{duplicate}</p>}

      <div className="grid grid-cols-1 gap-4">
        <input name="author_name" placeholder="Author" className="input" onChange={handleChange} value={form.author_name} />
        <input name="genre_name" placeholder="Genre" className="input" onChange={handleChange} value={form.genre_name} />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <input name="isbn" placeholder="ISBN" className="input" onChange={handleChange} value={form.isbn} />
        <input name="publisher" placeholder="Publisher" className="input" onChange={handleChange} value={form.publisher} />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <input name="pages" type="number" placeholder="Pages" className="input" onChange={handleChange} value={form.pages} />
        <input name="language" placeholder="Language" className="input" onChange={handleChange} value={form.language} />
      </div>

      <input name="publication_date" type="date" className="input" onChange={handleChange} value={form.publication_date} />

      <textarea name="description" placeholder="Description" className="input" rows={3} onChange={handleChange} value={form.description} />

      <h3 className="font-semibold">Upload Images</h3>
      <input type="file" multiple accept="image/*" onChange={(e) => setImages([...e.target.files!])} />

      <h3 className="font-semibold">Optional Review</h3>
      <textarea name="review_seed_text" className="input" placeholder="Your review" onChange={handleChange} value={form.review_seed_text} />
      <select name="review_seed_rating" className="input" onChange={handleChange} value={form.review_seed_rating}>
        {[5,4,3,2,1].map((x) => <option key={x}>{x}</option>)}
      </select>
      </fieldset>

      <button disabled={submitting} type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded">
        {submitting ? "Submitting..." : "Submit Suggestion"}
      </button>
    </form>
  );
}

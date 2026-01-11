import { useEffect, useState } from "react";
import { SuggestionsAPI } from "../../api/suggestions";
import SuggestionItem from "../../components/book_suggestions/SuggestionItem";
import type { BookSuggestion } from "../../types";

export default function MySuggestionsPage() {
  const [items, setItems] = useState<BookSuggestion[]>([]);

  useEffect(() => {
    SuggestionsAPI.mine().then(setItems);
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">My Suggestions</h1>

      {items.map((sg) => (
        <SuggestionItem key={sg.id} sg={sg} />
      ))}
    </div>
  );
}

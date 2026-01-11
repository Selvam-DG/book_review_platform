import SuggestionForm from "../../components/book_suggestions/SuggestionForm";
import { SuggestionsAPI } from "../../api/suggestions";

export default function SuggestBookPage() {
  const handleSubmit = async (payload: any) => {
    await SuggestionsAPI.create(payload);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Suggest a New Book</h1>
      <SuggestionForm onSubmit={handleSubmit} />
    </div>
  );
}

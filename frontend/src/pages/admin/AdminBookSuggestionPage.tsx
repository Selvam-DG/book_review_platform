import { useEffect, useState } from "react";
import SuggestionItem from "../../components/book_suggestions/SuggestionItem";
import { SuggestionsAPI } from "../../api/suggestions";
import type { BookSuggestion } from "../../types";

export default function AdminSuggestionsPage() {
  const [items, setItems] = useState<BookSuggestion[]>([]);
  const [status, setStatus] = useState("PENDING");

  const load = async () => {
    const res = await SuggestionsAPI.adminList(status);
    setItems(res);
  };

  useEffect(() => { load(); }, [status]);

  const handleApprove = async (id: number) => {
    await SuggestionsAPI.approve(id);
    load();
  };

  const handleReject = async (id: number) => {
    const reason = prompt("Enter rejection reason:");
    if (!reason) return;
    await SuggestionsAPI.reject(id, reason);
    load();
  };

  return (
    <div className="max-w-5xl mx-auto p-6">

      <div className="flex gap-3 mb-4">
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="border p-2"
        >
          <option value="PENDING">Pending</option>
          <option value="APPROVED">Approved</option>
          <option value="REJECTED">Rejected</option>
        </select>
      </div>

      {items.map((sg) => (
        <SuggestionItem
          key={sg.id}
          sg={sg}
          admin={true}
          onApprove={() => handleApprove(sg.id)}
          onReject={() => handleReject(sg.id)}
        />
      ))}
    </div>
  );
}

import type { BookSuggestion } from "../../types";

export default function SuggestionItem({
  sg,
  admin,
  onApprove,
  onReject
}: {
  sg: BookSuggestion;
  admin?: boolean;
  onApprove?: () => void;
  onReject?: () => void;
}) {
  return (
    <div className="border rounded p-4 mb-4">
      <h3 className="text-xl font-semibold">{sg.title}</h3>
      <p className="text-gray-600">{sg.author_name}</p>
      <p className="text-gray-600">{sg.genre_name}</p>
      <p className="text-gray-500 text-sm">{sg.created_at}</p>
      <p className="mt-2">{sg.description}</p>

      <p className="mt-3 font-bold">Status: {sg.status}</p>

      {admin && sg.status === "PENDING" && (
        <div className="flex gap-3 mt-3">
          <button className="bg-green-600 text-white px-3 py-2 rounded"
            onClick={onApprove}>Approve</button>

          <button className="bg-red-600 text-white px-3 py-2 rounded"
            onClick={onReject}>Reject</button>
        </div>
      )}
    </div>
  );
}

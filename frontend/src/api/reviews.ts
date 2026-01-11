import { getJSON, postJSON, putJSON, deleteJSON } from "./index";
import type { Review } from "../types";

export const ReviewsAPI = {
  create: (payload: {
    book_id: number;
    rating: number;
    review_text: string;
  }) => postJSON("/reviews", payload),

  update: (id: number, payload: Partial<Review>) =>
    putJSON(`/reviews/${id}`, payload),

  delete: (id: number) => deleteJSON(`/reviews/${id}`),
};

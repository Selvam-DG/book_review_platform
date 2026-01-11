import { getJSON, postJSON } from "./index";
import type { BookSuggestion } from "../types";

export const SuggestionsAPI = {
  create: (payload: {
    title: string;
    author_name?: string;
    genre_name?: string;
    description?: string;
  }) => postJSON(`/suggestions`, payload),

  mine: () => getJSON<BookSuggestion[]>(`/suggestions/mine`),

  adminList: (status = "PENDING") =>
    getJSON<BookSuggestion[]>(`/admin/suggestions?status=${status}`),

  approve: (id: number) =>
    postJSON(`/admin/suggestions/${id}/approve`, {}),

  reject: (id: number, reason: string) =>
    postJSON(`/admin/suggestions/${id}/reject`, { reason }),
};

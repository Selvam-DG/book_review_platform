import { getJSON } from "./index";
import type { Book, BookDetail } from "../types";

export const BooksAPI = {
  list: () => getJSON<Book[]>("/books"),
  detail: (id: number) => getJSON<BookDetail>(`/books/${id}`),
};

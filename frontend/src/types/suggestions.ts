export interface BookSuggestion {
  id: number;
  title: string;
  author_name?: string;
  genre_name?: string;
  isbn?: string;
  publication_date?: string;
  pages?: number;
  language?: string;
  publisher?: string;
  description?: string;

  image_urls?: string[]; 

  review_seed_text?: string;
  review_seed_rating?: number;

  status: "PENDING" | "APPROVED" | "REJECTED";
  created_at: string;
  admin_notes?: string;
}

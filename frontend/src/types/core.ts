export type Author = {
  id: number;
  name: string;
  bio?: string;
  birth_date?: string;
  nationality?: string;
  created_at?: string;
};

export type Genre = {
  id: number;
  name: string;
  description?: string;
  created_at?: string;
};

export type BookImage = {
  id: number;
  object_url: string;
  is_cover: boolean;
  created_at?: string;
};


export type Book = {
  id: number;
  title: string;
  author: Author;
  genre: Genre;
  isbn?: string;
  publication_date?: string;
  pages?: number;
  language?: string;
  publisher?: string;
  description?: string;
  created_at?: string;

  images?: BookImage[];
  reviews?: Review[];

  avg_rating?: number;
  reviews_count?: number;
};

export type User = {
  id: number;
  username: string;
  email: string;
  is_admin: number;
  created_at?: string;
};

export type Review = {
  id: number;
  rating: number;
  review_text?: string;
  helpful_count: number;
  created_at?: string;
  user: User;
};

export type BookDetail = Book & {
  reviews: Review[];
};

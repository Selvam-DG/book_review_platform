// Type definitions for the frontend

export type Author = {
  id: number;
  name: string;
  bio?: string;
  birth_date?: string;
  nationality?: string;
};

export type Genre = {
  id: number;
  name: string;
  description?: string;
};

export type Book = {
  id: number;
  title: string;
  author: Author;
  genre: Genre;
  isbn?: string;
  description?: string;
  pages?: number;
  language?: string;
  publisher?: string;
  created_at?: string;
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
  user: User;
  helpful_count: number;
  created_at?: string;
};

export type BookDetail = Book & {
  reviews: Review[];
};

export type AuthResponse = {
  access_token: string;
  user: User;
};

export type LoginRequest = {
  username: string;
  password: string;
};

export type RegisterRequest = {
  username: string;
  email: string;
  password: string;
};

export type ReviewRequest = {
  book_id: number;
  user_id: number;
  rating: number;
  review_text?: string;
};
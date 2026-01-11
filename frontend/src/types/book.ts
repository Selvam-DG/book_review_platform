import type { Author, Genre, BookImage } from "./core";

export type BookAPI = {
  id: number;
  title: string;
  author: Author;
  genre: Genre;
  images?: BookImage[];
  reviews_count?: number;
  avg_rating?: number;
};


export type BookCard = {
  id: number;
  title: string;
  author: Author;
  genre: Genre;
  cover_url: string;
  avg_rating: number;
  reviews_count: number;
};

export type BookStats = {
  total_books: number;
  total_genres: number;
  max_reviews: number;
  user_reviews: number;
};

import type { User } from "./core";

export type AdminUser = User & {
  status: "PENDING" | "ACTIVE" | "REJECTED";
  approved_at?: string | null;
};

export type AdminMetrics = {
  users: {
    total: number;
    active: number;
    pending: number;
    rejected: number;
  };
  books: {
    total: number;
    genres: number;
    max_reviews: number;
  };
  reviews: {
    total: number;
  };
};

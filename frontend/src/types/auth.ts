import type { User } from "./core";


export type AuthResponse = {
  access_token: string;
  refresh_token: string;
  user: User;
};

export type LoginRequest = {
  username?: string;
  email?: string;
  password: string;
};

export type RegisterRequest = {
  username: string;
  email: string;
  password: string;
};

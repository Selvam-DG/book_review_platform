import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from "react";
import type { User } from "../types";
import { apiUrl } from "../api/index";

interface AuthContextType {
  token: string | null;
  user: User | null;
  login: (access: string, refresh: string, user: User) => void;
  logout: () => void;
  refresh: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("access_token")
  );
  

  const [user, setUser] = useState<User | null>(() => {
    const raw = localStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  });

  /** LOGIN */
  const login = (access: string, refresh: string, u: User) => {
    setToken(access);
    setUser(u);

    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    localStorage.setItem("user", JSON.stringify(u));
  };

  /** LOGOUT */
  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    window.location.href = "/";
  }, []);

  /** REFRESH ACCESS TOKEN */
  const refresh = useCallback(async (): Promise<string | null> => {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
      logout();
      return null;
    }

    try {
      const res = await fetch(`${await apiUrl()}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (!res.ok) {
        logout();
        return null;
      }

      const data = await res.json();

      setToken(data.access_token);
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);

      return data.access_token;
    } catch {
      logout();
      return null;
    }
  }, [logout]);

  /** Sync token changes across tabs */
  useEffect(() => {
    const handler = () => {
      setToken(localStorage.getItem("access_token"));
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, []);

  return (
    <AuthContext.Provider
      value={{ token, user, login, logout, refresh }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return ctx;
};

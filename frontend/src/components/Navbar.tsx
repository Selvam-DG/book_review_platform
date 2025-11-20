import { BookOpen, LogOut, LogIn, UserPlus } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import type { User } from "../types";

interface NavbarProps {
  token: string | null;
  user: User | null;
  onLogout: () => void;
}

export default function Navbar({
  token,
  user,
  onLogout,
}: NavbarProps) {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
        <div
          className="flex items-center gap-2 cursor-pointer hover:opacity-80 transition"
          onClick={() => navigate("/")}
        >
          <BookOpen className="text-indigo-600" size={28} />
          <span className="font-bold text-lg text-gray-900">BookReview</span>
        </div>

        <div className="flex gap-4 items-center">
          <button
            onClick={() => navigate("/books")}
            className={`transition ${
              location.pathname === "/books"
                ? "text-indigo-600 font-semibold"
                : "text-gray-700 hover:text-indigo-600"
            }`}
          >
            Books
          </button>

          {token && user ? (
            <>
              <span className="text-sm text-gray-600">
                Welcome, <span className="font-semibold">{user.username}</span>
              </span>
              {user.is_admin === 1 && (
                <span className="px-2 py-1 bg-amber-100 text-amber-800 text-xs rounded font-semibold">
                  Admin
                </span>
              )}
              <button
                onClick={onLogout}
                className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition text-sm"
              >
                <LogOut size={16} /> Logout
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => navigate("/login")}
                className="flex items-center gap-2 px-4 py-2 border border-indigo-600 text-indigo-600 rounded hover:bg-indigo-50 transition text-sm"
              >
                <LogIn size={16} /> Login
              </button>
              <button
                onClick={() => navigate("/signup")}
                className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition text-sm"
              >
                <UserPlus size={16} /> Sign Up
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
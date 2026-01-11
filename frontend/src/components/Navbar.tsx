import { BookOpen, ChevronDown } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { useState, useRef, useEffect } from "react";


export default function Navbar() {
  const { token, user, logout } = useAuth();
  const navigate = useNavigate();

  const [openUserMenu, setOpenUserMenu] = useState(false);
  const userMenuRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(e.target as Node)) {
        setOpenUserMenu(false);
      }
    };
    document.addEventListener("click", handleClick);
    return () => document.removeEventListener("click", handleClick);
  }, []);

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

        <div className="flex gap-6 items-center">
          <button
            onClick={() => navigate("/books")}
            className="text-gray-700 hover:text-indigo-600"
          >
            Books
          </button>

          {!token && (
            <div className="flex gap-4">
              <button onClick={() => navigate("/login")} className="hover:text-indigo-600">
                Login
              </button>
              <button onClick={() => navigate("/signup")} className="hover:text-indigo-600">
                Sign Up
              </button>
            </div>
          )}

          {token && user && (
            <div className="relative" ref={userMenuRef}>
              <button
                onClick={() => setOpenUserMenu(!openUserMenu)}
                className="flex items-center gap-1 text-gray-800 hover:text-indigo-600"
              >
                {user.username}
                <ChevronDown size={18} />
              </button>

              {openUserMenu && (
                <div className="absolute right-0 mt-2 bg-white shadow-lg rounded w-48 p-2 z-50">
                  {!user.is_admin && (
                    <>
                      <MenuItem label="My Profile" onClick={() => navigate("/profile")} />
                      <MenuItem label="My Reviews" onClick={() => navigate("/my-reviews")} />
                      <MenuItem label="Suggest Book" onClick={() => navigate("/suggest-book")} />
                      <MenuItem label="My Suggestions" onClick={() => navigate("/my-suggestions")} />
                      <Divider />
                    </>
                  )}

                  {user.is_admin && (
                    <>
                      <MenuItem label="Admin Dashboard" onClick={() => navigate("/admin")} />
                      <MenuItem label="Book Suggestions" onClick={() => navigate("/admin/suggestions")} />
                      <MenuItem label="User Approvals" onClick={() => navigate("/admin/users")} />
                      <MenuItem label="Stats" onClick={() => navigate("/admin/stats")} />
                      <Divider />
                    </>
                  )}

                  <MenuItem label="Logout" onClick={logout} className="text-red-600" />
                </div>
              )}
            </div>
          )}

          
        </div>
      </div>
    </nav>
  );
}

function MenuItem({ label, onClick, className = "" }: any) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left px-3 py-2 text-gray-700 hover:bg-gray-100 rounded ${className}`}
    >
      {label}
    </button>
  );
}

function Divider() {
  return <div className="border-t my-2"></div>;
}
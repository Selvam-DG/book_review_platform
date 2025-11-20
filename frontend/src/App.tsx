import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import type { User } from "./types";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import HomePage from "./pages/HomePage";
import BooksPage from "./pages/BooksPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";

function AppContent() {
  const navigate = useNavigate();
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );
  const [user, setUser] = useState<User | null>(() => {
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  const handleAuthSuccess = (newToken: string, newUser: User) => {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem("token", newToken);
    localStorage.setItem("user", JSON.stringify(newUser));
    navigate("/books");
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <Navbar
        token={token}
        user={user}
        onLogout={handleLogout}
      />

      <main className="flex-1">
        <Routes>
          <Route
            path="/"
            element={<HomePage onBooksClick={() => navigate("/books")} />}
          />
          <Route
            path="/books"
            element={<BooksPage token={token || undefined} user={user || undefined} />}
          />
          <Route
            path="/login"
            element={<LoginPage onSuccess={handleAuthSuccess} />}
          />
          <Route
            path="/signup"
            element={<SignupPage onSuccess={handleAuthSuccess} />}
          />
          {/* Redirect unknown routes to home */}
          <Route path="*" element={<HomePage onBooksClick={() => navigate("/books")} />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}
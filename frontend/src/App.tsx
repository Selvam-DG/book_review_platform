import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import HomePage from "./pages/HomePage";
import BooksPage from "./pages/BooksPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminUsersPage from "./pages/admin/AdminUserPage";
import BookDetailPage from "./pages/BookDetailPage";

import SuggestBookPage from "./pages/book_suggestions/SuggestBookPage";
import MySuggestionsPage from "./pages/book_suggestions/MySuggestionsPage";
import AdminSuggestionsPage from "./pages/admin/AdminBookSuggestionPage";


export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-1 bg-gray-50">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/books" element={<BooksPage />} />
              <Route path="/books/:id" element={<BookDetailPage />} />

              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              
              {/* User Pages */}
              <Route path="/suggest-book" element={
                <ProtectedRoute>
                  <SuggestBookPage />
                </ProtectedRoute>
              } />

              <Route path="/my-suggestions" element={
                <ProtectedRoute>
                  <MySuggestionsPage />
                </ProtectedRoute>
              } />
              {/*
              <Route path="/my-reviews" element={
                <ProtectedRoute>
                  <MyReviewsPage />
                </ProtectedRoute>
              } />
              */}

              {/* Admin Pages  */}
              
              <Route path="/admin" element={
                <ProtectedRoute adminOnly>
                  <AdminDashboard />
                </ProtectedRoute>
              } />
              
              <Route path="/admin/suggestions" element={
                <ProtectedRoute adminOnly>
                  <AdminSuggestionsPage />
                </ProtectedRoute>
              } />
              
              <Route path="/admin/users" element={
                <ProtectedRoute adminOnly>
                  <AdminUsersPage />
                </ProtectedRoute>
              } />
              {/* 
              <Route path="/admin/stats" element={
                <ProtectedRoute adminOnly>
                  <AdminStatsPage />
                </ProtectedRoute>
              } />

              */}


            </Routes>
          </main>
          <Footer />
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}

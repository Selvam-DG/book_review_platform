import { useState } from "react";
import { AlertCircle, Loader, Info } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { postJSON } from "../api/index";
import { useAuth } from "../auth/AuthContext";
import type { AuthResponse } from "../types";



export default function LoginPage() {
    const navigate = useNavigate();
    const { login } = useAuth();

  const [identifier, setIdentifier] = useState(""); 
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [info, setInfo] = useState("");

  const handleSubmit = async () => {
    setError("");
    setInfo("");

    if (!identifier.trim() || !password.trim()) {
      setError("Username/email and password are required");
      return;
    }
    const payload: any = {
      password,
    };
    if (identifier.includes("@")) {
      payload.email = identifier.trim();
    } else {
      payload.username = identifier.trim();
    }

    try {
      setLoading(true);

      const response = await postJSON<AuthResponse>("/auth/login", payload);

      login(response.access_token, response.refresh_token, response.user);
      navigate("/books");
    } catch (err) {
      const msg = (err as Error).message;

      // Backend-aligned messages
      if (msg.includes("pending approval")) {
        setInfo(
          "Your account is pending approval. You will be notified once activated."
        );
      } else if (msg.includes("invalid")) {
        setError("Invalid username/email or password");
      } else {
        setError(msg || "Login failed");
      }
    } finally {
      setLoading(false);
    }
  };


  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !loading) {
      handleSubmit();
    }
  };

  return (
    <div className="min-h-[calc(100vh-200px)] flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Login</h2>
          <p className="text-gray-600 mt-2">
            Sign in using your username or email
          </p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 text-red-800 rounded-lg flex gap-2">
            <AlertCircle size={20} className="flex-shrink-0" />
            <p className="text-sm">{error}</p>
          </div>
        )}
         {info && (
          <div className="mb-4 p-4 bg-blue-100 text-blue-800 rounded-lg flex gap-2">
            <Info size={20} />
            <p className="text-sm">{info}</p>
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Username or Email
            </label>
            <input
              type="text"
              className="w-full border border-gray-300 rounded px-4 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Enter  username or email"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              className="w-full border border-gray-300 rounded px-4 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50 transition flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader size={18} className="animate-spin" />
                Logging in...
              </>
            ) : (
              "Login"
            )}
          </button>

          <p className="text-center text-gray-600 text-sm">
            Don't have an account?{" "}
            <Link to="/signup" className="text-indigo-600 hover:text-indigo-700 font-semibold">
                Sign up
            </Link>
          </p>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center">
             You can log in using either your username or email address
          </p>
        </div>
      </div>
    </div>
  );
}
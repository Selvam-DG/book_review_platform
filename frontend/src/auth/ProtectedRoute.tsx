import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import React from "react";

type ProtectedRouteProps = {
  adminOnly?: boolean;
  children: React.ReactNode;
};

export default function ProtectedRoute({
  adminOnly,
  children,
}: ProtectedRouteProps) {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" />;
  if (adminOnly && !user.is_admin) return <Navigate to="/" />;

  return <>{children}</>;
}

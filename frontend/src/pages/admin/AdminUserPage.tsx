import { useEffect, useState } from "react";
import { Check, X, Trash2, Loader } from "lucide-react";
import { useAuth } from "../../auth/AuthContext";
import { AdminAPI } from "../../api/admin";
import type { AdminUser } from "../../api/admin";




export default function AdminUsersPage() {
  const { token } = useAuth();
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const [error, setError] = useState("");

  const loadUsers = async () => {
    try {
      setLoading(true);
      const data = await AdminAPI.usersList(token!);
      setUsers(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleApprove = async (id: number) => {
    setActionLoading(id);
    await AdminAPI.userApprove(id, token!);
    await loadUsers();
    setActionLoading(null);
  };

  const handleReject = async (id: number) => {
    setActionLoading(id);
    await AdminAPI.userReject(id, token!);
    await loadUsers();
    setActionLoading(null);
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this user?")) return;
    setActionLoading(id);
    await AdminAPI.userDelete(id, token!);
    await loadUsers();
    setActionLoading(null);
  };

  if (loading) {
    return (
      <div className="p-6 text-center">
        <Loader className="animate-spin mx-auto mb-2" />
        Loading users…
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">User Management</h1>

      {error && (
        <div className="mb-4 text-red-600">{error}</div>
      )}

      <div className="overflow-x-auto bg-white shadow rounded-lg">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-100 text-gray-700">
            <tr>
              <th className="px-4 py-3 text-left">Username</th>
              <th className="px-4 py-3 text-left">Email</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Role</th>
              <th className="px-4 py-3">Created</th>
              <th className="px-4 py-3">Approved</th>
              <th className="px-4 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {users.map((u) => (
              <tr key={u.id}>
                <td className="px-4 py-3">{u.username}</td>
                <td className="px-4 py-3">{u.email}</td>

                <td className="px-4 py-3">
                  <span
                    className={`px-2 py-1 rounded text-xs font-semibold ${
                      u.status === "ACTIVE"
                        ? "bg-green-100 text-green-700"
                        : u.status === "PENDING"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-red-100 text-red-700"
                    }`}
                  >
                    {u.status}
                  </span>
                </td>

                <td className="px-4 py-3">
                  {u.is_admin ? "Admin" : "User"}
                </td>

                <td className="px-4 py-3">{u.created_at}</td>
                <td className="px-4 py-3">
                  {u.approved_at || "-"}
                </td>

                <td className="px-4 py-3 text-right space-x-2">
                  {u.status === "PENDING" && (
                    <>
                      <button
                        onClick={() => handleApprove(u.id)}
                        disabled={actionLoading === u.id}
                        className="text-gray-100 p-2 bg-green-600 rounded-md hover:bg-green-700 hover:shadow-md hover:scale-105 transition duration-200 ease-in-out active:scale-95"
                        title="Approve"
                      >
                        Approve
                      </button>
                      <button
                        onClick={() => handleReject(u.id)}
                        disabled={actionLoading === u.id}
                        className="bg-yellow-600 p-2 rounded-md hover:bg-yellow-700 hover:shadow-md hover:scale-105 transition duration-200 ease-in-out active:scale-95"
                        title="Reject"
                      >
                        Reject
                      </button>
                    </>
                  )}

                  <button
                    onClick={() => handleDelete(u.id)}
                    disabled={actionLoading === u.id}
                    className="bg-red-600 p-2 rounded-md text-gray-100 hover:bg-red-700 hover:shadow-md hover:scale-105 transition duration-200 ease-in-out active:scale-95"
                    title="Delete"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {users.length === 0 && (
          <div className="p-6 text-center text-gray-500">
            No users found
          </div>
        )}
      </div>
    </div>
  );
}

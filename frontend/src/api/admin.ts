import { getJSON, postJSON, deleteJSON } from "./index";
import { API } from "./api_endpoints";

export interface AdminUser {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
  status: "PENDING" | "ACTIVE" | "REJECTED";
  created_at: string;
  approved_at?: string | null;
}

export const AdminAPI = {

  usersList: () =>
    getJSON<AdminUser[]>(API.ADMIN_USERS),
  userApprove: (userId: number) =>
    postJSON(`/admin/users/${userId}/approve`, {}),

  userReject: (userId: number) =>
    postJSON(`/admin/users/${userId}/reject`, {}),

  userDelete: (userId: number) =>
    deleteJSON(`/admin/users/${userId}`),

  metrics: () => getJSON(API.ADMIN_METRICS,),
  auditLogs: (q = "") =>
    getJSON(`${API.ADMIN_AUDIT_LOGS}${q}`),
};

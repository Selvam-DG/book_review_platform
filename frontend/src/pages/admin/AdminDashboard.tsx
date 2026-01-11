import { useEffect, useState } from "react";
import { useAuth } from "../../auth/AuthContext";
import { AdminAPI } from "../../api/admin";
import MetricCard from "../../components/admin/MetricCard";

export default function AdminDashboard() {
  const { token } = useAuth();
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    AdminAPI.metrics(token!).then(setMetrics);
  }, []);

  if (!metrics) return <p className="p-6">Loading dashboard...</p>;

  return (
    <div className="p-6 grid grid-cols-1 md:grid-cols-4 gap-4">
      <MetricCard title="Users" value={metrics.users.total} />
      <MetricCard title="Pending Users" value={metrics.users.pending} />
      <MetricCard title="Books" value={metrics.books.total} />
      <MetricCard title="Reviews" value={metrics.reviews.total} />
    </div>
  );
}

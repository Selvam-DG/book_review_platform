// export function apiUrl(): string {
//   // Prefer runtime config from ConfigMap; fallback to Vite env; then default
//   const w = window as any;
//   return (w._CONFIG_ && w._CONFIG_.API_URL)
//       || import.meta.env.VITE_API_URL
//       || "http://10.0.0.7:30089";
// }
export function apiUrl(): string {
  // Prefer runtime config from ConfigMap; fallback to Vite env; then default
  return "http://10.0.0.7:30089";
}
export async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${apiUrl()}${path}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function postJSON<T>(path: string, body: any): Promise<T> {
  const res = await fetch(`${apiUrl()}${path}`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

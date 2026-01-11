// API configuration and helper functions

// export function apiUrl(): string {
//   // Fallback to environment variable or default
//   return import.meta.env.VITE_API_URL || "http://10.0.0.7:8000";
// }

let runtimeConfig: { api_url?: string } | null = null;

/**
 * Load runtime config.json (Docker / Nginx)
 * Called only if .env variable is not present
 */
async function loadRuntimeConfig(): Promise<void> {
  if (runtimeConfig !== null) return;

  try {
    const res = await fetch("/config.json");
    if (!res.ok) throw new Error("No config.json");
    runtimeConfig = await res.json();
  } catch {
    runtimeConfig = {};
  }
}

/**
 * Resolve API base URL
 */
export async function apiUrl(): Promise<string> {
  //  Local dev (.env)
  const envUrl = import.meta.env.VITE_API_URL;
  if (envUrl) return envUrl;

  //  Runtime config (Docker / prod)
  await loadRuntimeConfig();
  if (runtimeConfig?.api_url) return runtimeConfig.api_url;

  //  Fallback
  return "http://localhost:8000";
}

async function request<T>(
  method: string,
  path: string,
  body?: any,
): Promise<T> {
  const base = await apiUrl();
  const access = localStorage.getItem("access_token");
  const refresh = localStorage.getItem("refresh_token");
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (access) {
    headers.Authorization = `Bearer ${access}`;
  }

  let res = await fetch(`${base}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (res.status === 401 && refresh) {
    const refreshRes = await fetch(`${base}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refresh }),
    });

    if (refreshRes.ok) {
      const data = await refreshRes.json();

      // saved new tokens
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);

      // retry request
      headers["Authorization"] = `Bearer ${data.access_token}`;

      res = await fetch(`${base}${path}`, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
      });
    }
  }

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Request failed");
  }


   return (await res.json()) as T;
}

export const getJSON = <T>(path: string, ) =>
  request<T>("GET", path);

export const postJSON = <T>(path: string, body: any) =>
  request<T>("POST", path, body);

export const putJSON = <T>(path: string, body: any) =>
  request<T>("PUT", path, body);

export const deleteJSON = <T>(path: string) =>
  request<T>("DELETE", path, undefined);

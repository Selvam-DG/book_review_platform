// API configuration and helper functions

// export function apiUrl(): string {
//   // Fallback to environment variable or default
//   return import.meta.env.VITE_API_URL || "http://10.0.0.7:8000";
// }
let runtimeConfig: any = null;

// Load config.json ONCE at runtime
async function loadConfig(): Promise<void> {
  if (runtimeConfig) return;
  const res = await fetch("/config.json");
  runtimeConfig = await res.json();
}

export async function apiUrl(): Promise<string> {
  await loadConfig();
  return runtimeConfig.api_url;
}

export async function fetchJSON<T>(path: string, token?: string): Promise<T> {
  const base = await apiUrl();
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${base}${path}`, {
    method: "GET",
    headers,
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || `HTTP Error: ${res.status}`);
  }

  return res.json();
}

export async function postJSON<T>(
  path: string,
  body: any,
  token?: string
): Promise<T> {
  const base = await apiUrl();
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${base}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || `HTTP Error: ${res.status}`);
  }

  return res.json();
}

export async function putJSON<T>(
  path: string,
  body: any,
  token?: string
): Promise<T> {
  const base = await apiUrl();
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${base}${path}`, {
    method: "PUT",
    headers,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || `HTTP Error: ${res.status}`);
  }

  return res.json();
}

export async function deleteJSON<T>(path: string, token?: string): Promise<T> {
  const base = await apiUrl();
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${base}${path}`, {
    method: "DELETE",
    headers,
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || `HTTP Error: ${res.status}`);
  }

  return res.json();
}
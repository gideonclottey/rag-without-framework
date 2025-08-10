// Prefer Vite proxy in dev: fetch("/api/...") -> to 127.0.0.1:8000
// Fallback to env var if set:
const base = import.meta.env.VITE_API_BASE || "/api";

async function jsonFetch(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) {
    let msg = await res.text().catch(() => "");
    throw new Error(msg || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function uploadFiles(files) {
  const form = new FormData();
  [...files].forEach(f => form.append("files", f));
  return jsonFetch(`${base}/upload`, { method: "POST", body: form });
}

export async function ingest({ folder = "data", chunk_size = 500, overlap = 50 } = {}) {
  return jsonFetch(`${base}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ folder, chunk_size, overlap }),
  });
}

export async function ask({ query, top_k = 5 }) {
  return jsonFetch(`${base}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, top_k }),
  });
}

import { $, escapeHtml } from "../utils/dom.js";

const API_BASE = import.meta.env.VITE_API_BASE || "/api";

async function safeJson(res) {
  // turn non-2xx into readable errors
  if (!res.ok) {
    const txt = await res.text().catch(() => "");
    throw new Error(txt || `HTTP ${res.status}`);
  }
  return res.json();
}

async function pollIngestStatus(onDone, { interval = 1000, timeoutMs = 120000 } = {}) {
  const url = `${API_BASE}/ingest/status`;
  const startedAt = Date.now();
  const timer = setInterval(async () => {
    try {
      const res = await fetch(url, { cache: "no-store" });
      const s = await safeJson(res);

      // guard against undefined values
      const running = Boolean(s?.running);
      if (!running) {
        clearInterval(timer);
        onDone?.(s);
      } else if (Date.now() - startedAt > timeoutMs) {
        clearInterval(timer);
        onDone?.({ running: false, last_error: "Ingest timed out", docs: s?.docs ?? 0, chunks: s?.chunks ?? 0 });
      }
    } catch (e) {
      clearInterval(timer);
      onDone?.({ running: false, last_error: e.message, docs: 0, chunks: 0 });
    }
  }, interval);
}

export function mountUpload() {
  const $btn = $("#btnUpload");
  const $input = $("#fileInput");
  const $status = $("#uploadStatus");

  $btn.addEventListener("click", async () => {
    const files = $input.files;
    if (!files || !files.length) {
      $status.textContent = "Pick at least one file.";
      return;
    }

    // UX: disable while uploading
    $btn.disabled = true;
    $status.textContent = "Uploading…";

    try {
      const form = new FormData();
      [...files].forEach((f) => form.append("files", f));

      const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form });
      const out = await safeJson(res);

      const savedList = Array.isArray(out?.saved) ? out.saved : [];
      $status.textContent = `Saved: ${escapeHtml(savedList.join(", ") || "none")} | Reindex started…`;

      // poll until ingest finishes
      await pollIngestStatus((s) => {
        const docs = s?.docs ?? 0;
        const chunks = s?.chunks ?? 0;
        const err = s?.last_error ? ` (error: ${s.last_error})` : "";
        $status.textContent = `Reindex done. Docs: ${docs}, Chunks: ${chunks}${err}`;
      });
    } catch (e) {
      $status.textContent = `Upload failed: ${e.message}`;
    } finally {
      $btn.disabled = false;
    }
  });
}

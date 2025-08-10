import { $ } from "../utils/dom.js";
import { ingest } from "../api/client.js";

export function mountIngest() {
  $("#btnIngest").addEventListener("click", async () => {
    const chunk_size = Number($("#chunkSize").value || 500);
    const overlap = Number($("#overlap").value || 50);
    $("#ingestStatus").textContent = "Indexing...";
    try {
      const out = await ingest({ folder: "data", chunk_size, overlap });
      $("#ingestStatus").textContent = `Docs: ${out.documents} | Chunks: ${out.chunks}`;
    } catch (e) {
      $("#ingestStatus").textContent = `Error: ${e.message}`;
    }
  });
}

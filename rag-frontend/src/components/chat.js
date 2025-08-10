import { $, escapeHtml } from "../utils/dom.js";
import { ask } from "../api/client.js";

export function mountChat() {
  $("#btnAsk").addEventListener("click", async () => {
    const query = $("#query").value.trim();
    const top_k = Number($("#topK").value || 5);
    if (!query) return;
    $("#answer").textContent = "Thinking...";
    $("#context").innerHTML = "";
    try {
      const out = await ask({ query, top_k });
      $("#answer").textContent = out.answer || "(no answer)";
      const previews = out.context_preview || []; // if you added this in /query
      $("#context").innerHTML = previews
        .map(p => `<li><pre>${escapeHtml(p)}</pre></li>`)
        .join("");
    } catch (e) {
      $("#answer").textContent = `Error: ${e.message}`;
    }
  });
}

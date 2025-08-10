import { $, escapeHtml } from "../utils/dom.js";
import { uploadFiles } from "../api/client.js";

export function mountUpload() {
  $("#btnUpload").addEventListener("click", async () => {
    const files = $("#fileInput").files;
    if (!files || !files.length) {
      $("#uploadStatus").textContent = "Pick at least one file.";
      return;
    }
    $("#uploadStatus").textContent = "Uploading...";
    try {
      const out = await uploadFiles(files);
      $("#uploadStatus").textContent = `Uploaded: ${escapeHtml(out.saved?.join(", ") || "OK")}`;
    } catch (e) {
      $("#uploadStatus").textContent = `Error: ${e.message}`;
    }
  });
}

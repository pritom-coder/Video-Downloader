async function downloadVideo() {
  const videoURL = document.getElementById("videoURL").value.trim();
  const statusEl = document.getElementById("status");
  const btn = document.getElementById("downloadBtn");

  if (!videoURL) {
    statusEl.textContent = "⚠️ Please enter a valid video URL.";
    statusEl.className = "error";
    return;
  }

  statusEl.textContent = "⏳ Downloading...";
  statusEl.className = "loading";
  btn.disabled = true;

  try {
    const response = await fetch("http://127.0.0.1:8000/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: videoURL }),
    });

    if (!response.ok) throw new Error("Server Error");

    const data = await response.json();

    if (data.filename) {
      statusEl.textContent = "✅ Successfully downloaded!";
      statusEl.className = "success";
    } else {
      throw new Error("Download failed. Try again.");
    }
  } catch (error) {
    statusEl.textContent = "❌ " + error.message;
    statusEl.className = "error";
  } finally {
    btn.disabled = false;
  }
}

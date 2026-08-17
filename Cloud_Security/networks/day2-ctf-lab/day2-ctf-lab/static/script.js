document.addEventListener("DOMContentLoaded", () => {
  // Boot sequence -> reveal app
  const boot = document.getElementById("boot-screen");
  const app = document.getElementById("app");
  const bootDuration = window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 1900;
  setTimeout(() => {
    boot.classList.add("hidden");
    app.classList.remove("hidden");
  }, bootDuration);

  // Sidebar navigation
  const items = document.querySelectorAll(".challenge-item");
  const panels = document.querySelectorAll(".challenge-panel");

  items.forEach((item) => {
    item.addEventListener("click", () => {
      const id = item.dataset.id;
      items.forEach((i) => i.classList.toggle("active", i === item));
      panels.forEach((p) => p.classList.toggle("active", p.dataset.id === id));
    });
    item.setAttribute("tabindex", "0");
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); item.click(); }
    });
  });

  // Copy command buttons
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const cmd = btn.dataset.cmd;
      try {
        await navigator.clipboard.writeText(cmd);
        btn.classList.add("copied");
        btn.textContent = "✓";
        setTimeout(() => { btn.classList.remove("copied"); btn.textContent = "⧉"; }, 1200);
      } catch (err) {
        showToast("Couldn't copy — select and copy manually.");
      }
    });
  });

  // Save answer buttons
  document.querySelectorAll(".btn-save").forEach((btn) => {
    btn.addEventListener("click", () => saveAnswer(btn.dataset.id));
  });

  // Export
  document.getElementById("export-btn").addEventListener("click", () => {
    window.location.href = "/api/export";
  });

  // Complete day
  const completeBtn = document.getElementById("complete-btn");
  completeBtn.addEventListener("click", async () => {
    if (completeBtn.disabled) return;
    const answered = document.querySelectorAll(".challenge-item.logged").length;
    const total = items.length;
    if (answered < total) {
      const proceed = confirm(
        `You've logged ${answered}/${total} challenges. Mark the day complete anyway?`
      );
      if (!proceed) return;
    }
    const res = await fetch("/api/complete_day", { method: "POST" });
    if (res.ok) {
      completeBtn.disabled = true;
      completeBtn.textContent = "✓ Day Complete";
      showToast("Day marked complete. Export your answers and hand them over for review.");
    }
  });

  async function saveAnswer(id) {
    const textarea = document.querySelector(`.answer-box[data-id="${id}"]`);
    const statusEl = document.querySelector(`.save-status[data-id="${id}"]`);
    const answer = textarea.value.trim();
    if (!answer) {
      statusEl.textContent = "Write something first";
      statusEl.classList.add("show");
      setTimeout(() => statusEl.classList.remove("show"), 1800);
      return;
    }

    try {
      const res = await fetch("/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ challenge_id: id, answer }),
      });
      const data = await res.json();
      if (data.ok) {
        statusEl.textContent = "Saved ✓";
        statusEl.classList.add("show");
        setTimeout(() => statusEl.classList.remove("show"), 1800);

        // Update sidebar dot + progress bar
        const item = document.querySelector(`.challenge-item[data-id="${id}"]`);
        item.classList.add("logged");
        item.querySelector(".ch-status").textContent = "●";

        document.getElementById("progress-count").textContent = data.answered_count;
        const pct = (data.answered_count / data.total_count) * 100;
        document.getElementById("progress-fill").style.width = pct + "%";
      } else {
        statusEl.textContent = data.error || "Error saving";
        statusEl.classList.add("show");
      }
    } catch (err) {
      statusEl.textContent = "Network error";
      statusEl.classList.add("show");
    }
  }

  function showToast(msg) {
    const toast = document.getElementById("toast");
    toast.textContent = msg;
    toast.classList.remove("hidden");
    setTimeout(() => toast.classList.add("hidden"), 3500);
  }
});

const music = document.getElementById("site-music");
const toggle = document.getElementById("music-toggle");

if (music && toggle) {
  toggle.addEventListener("click", async () => {
    if (music.paused) {
      try {
        await music.play();
        toggle.textContent = "Ⅱ";
        toggle.setAttribute("aria-label", "Zatrzymaj muzykę");
      } catch (error) {
        console.error("Nie udało się uruchomić muzyki:", error);
      }
    } else {
      music.pause();
      toggle.textContent = "♫";
      toggle.setAttribute("aria-label", "Włącz muzykę");
    }
  });

  music.addEventListener("pause", () => {
    toggle.textContent = "♫";
    toggle.setAttribute("aria-label", "Włącz muzykę");
  });

  music.addEventListener("play", () => {
    toggle.textContent = "Ⅱ";
    toggle.setAttribute("aria-label", "Zatrzymaj muzykę");
  });
}

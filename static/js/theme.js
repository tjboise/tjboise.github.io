(function () {
  function toggleTheme() {
    var dark = !document.documentElement.classList.contains("dark");
    document.documentElement.classList.toggle("dark", dark);
    try {
      localStorage.setItem("theme", dark ? "dark" : "light");
    } catch (e) {}
  }

  document.querySelectorAll(".toggle-theme-button").forEach(function (el) {
    el.addEventListener("click", toggleTheme);
  });
})();

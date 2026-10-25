/* Vedant Konde - portfolio interactions
   Theme toggle, scroll reveal, stat count-up.
   Vanilla JS, no dependencies. */

(function () {
  "use strict";

  /* ---------- theme ---------- */
  var root = document.documentElement;
  var btn = document.getElementById("themeToggle");

  function applyTheme(theme, label) {
    if (theme === "dark") {
      root.setAttribute("data-theme", "dark");
    } else {
      root.removeAttribute("data-theme");
    }
    if (btn) { btn.textContent = label; }
  }

  var stored = null;
  try { stored = window.localStorage.getItem("theme"); } catch (e) {}
  if (stored === "dark") {
    applyTheme("dark", "Light");
  } else {
    applyTheme("light", "Dark");
  }

  if (btn) {
    btn.addEventListener("click", function () {
      var dark = root.hasAttribute("data-theme");
      if (dark) {
        applyTheme("light", "Dark");
      } else {
        applyTheme("dark", "Light");
      }
      try { window.localStorage.setItem("theme", dark ? "light" : "dark"); } catch (e) {}
    });
  }

  /* ---------- scroll reveal ---------- */
  var items = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------- stat count-up ---------- */
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

  function countUp(el, target, duration) {
    var start = performance.now();
    function tick(now) {
      var p = Math.min(1, (now - start) / duration);
      el.textContent = Math.round(easeOut(p) * target);
      if (p < 1) { requestAnimationFrame(tick); }
    }
    requestAnimationFrame(tick);
  }

  var nums = document.querySelectorAll(".stat-num[data-count]");
  if (nums.length && "IntersectionObserver" in window) {
    var nio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          countUp(el, parseInt(el.getAttribute("data-count"), 10) || 0, 900);
          nio.unobserve(el);
        }
      });
    }, { threshold: 0.4 });
    nums.forEach(function (el) { nio.observe(el); });
  }
})();

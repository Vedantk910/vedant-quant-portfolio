/* Vedant Konde - portfolio interactions
   Theme toggle, scroll reveal, stat count-up.
   Vanilla JS, no dependencies. */

(function () {
  "use strict";

  /* ---------- scroll progress ---------- */
  var bar = document.createElement("div");
  bar.className = "scroll-progress";
  bar.setAttribute("aria-hidden", "true");
  document.body.appendChild(bar);
  var ticking = false;
  function updateProgress() {
    ticking = false;
    var h = document.documentElement;
    var max = h.scrollHeight - window.innerHeight;
    var pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
    bar.style.width = pct + "%";
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(updateProgress); }
  }, { passive: true });
  updateProgress();

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
  var prefersDark = false;
  try { prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches; } catch (e) {}
  if (stored === "dark" || (stored === null && prefersDark)) {
    applyTheme("dark", "Light");
  } else {
    applyTheme("light", "Dark");
  }

  var metaTheme = document.getElementById("themeColor");
  var syncMetaTheme = function () {
    if (!metaTheme) return;
    metaTheme.setAttribute("content", root.hasAttribute("data-theme") ? "#000000" : "#f5f5f7");
  };
  syncMetaTheme();

  if (btn) {
    btn.addEventListener("click", function () {
      var dark = root.hasAttribute("data-theme");
      if (dark) {
        applyTheme("light", "Dark");
      } else {
        applyTheme("dark", "Light");
      }
      syncMetaTheme();
      try { window.localStorage.setItem("theme", dark ? "light" : "dark"); } catch (e) {}
    });
  }

  /* ---------- nav scrollspy + back-to-top + copy email ---------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".site-nav a"));
  var sections = navLinks.map(function (a) {
    var el = document.querySelector(a.getAttribute("href"));
    return el ? { link: a, el: el } : null;
  }).filter(Boolean);
  if (sections.length && "IntersectionObserver" in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        sections.forEach(function (s) { s.link.classList.remove("active"); });
        var hit = sections.filter(function (s) { return s.el === entry.target; })[0];
        if (hit) hit.link.classList.add("active");
      });
    }, { rootMargin: "-40% 0px -55% 0px", threshold: 0 });
    sections.forEach(function (s) { spy.observe(s.el); });
  }

  var back = document.getElementById("backToTop");
  if (back) {
    back.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    var showBack = function () {
      back.classList.toggle("show", window.scrollY > 700);
    };
    window.addEventListener("scroll", showBack, { passive: true });
    showBack();
  }

  document.querySelectorAll(".copy-email").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var done = function () {
        var prev = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = prev; }, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, done);
      } else {
        var ta = document.createElement("textarea");
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  });

  /* ---------- collapsible breakdowns ---------- */
  document.querySelectorAll(".fold-toggle").forEach(function (toggle) {
    toggle.addEventListener("click", function () {
      var panel = document.getElementById(toggle.getAttribute("aria-controls"));
      var open = toggle.getAttribute("aria-expanded") === "true";
      if (panel) panel.classList.toggle("open", !open);
      toggle.setAttribute("aria-expanded", String(!open));
      toggle.firstChild.nodeValue = open ? "Breakdown" : "Close breakdown";
    });
  });

  /* ---------- 3D tilt + magnetic (Apple-grade, pointer-fine only, respects reduced motion) ---------- */
  var finePointer = false, reducedMotion = false;
  try {
    finePointer = window.matchMedia("(pointer: fine)").matches;
    reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) {}

  if (finePointer && !reducedMotion) {
    /* 3D tilt: cards rotate toward the cursor; a light glare follows */
    document.querySelectorAll("[data-tilt]").forEach(function (el) {
      var maxTilt = parseFloat(el.getAttribute("data-tilt-max")) || 6;
      var raf = null, rx = 0, ry = 0, active = false;
      function apply() {
        raf = null;
        if (!active) return;
        el.style.transform = "perspective(1200px) rotateX(" + rx.toFixed(2) + "deg) rotateY(" + ry.toFixed(2) + "deg)";
      }
      el.addEventListener("mousemove", function (ev) {
        var r = el.getBoundingClientRect();
        var px = (ev.clientX - r.left) / r.width - 0.5;
        var py = (ev.clientY - r.top) / r.height - 0.5;
        ry = px * maxTilt;
        rx = -py * maxTilt;
        el.style.setProperty("--gx", ((px + 0.5) * 100).toFixed(1) + "%");
        el.style.setProperty("--gy", ((py + 0.5) * 100).toFixed(1) + "%");
        active = true;
        if (!raf) raf = requestAnimationFrame(apply);
      });
      el.addEventListener("mouseleave", function () {
        active = false;
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        el.style.transform = "perspective(1200px) rotateX(0deg) rotateY(0deg)";
      });
    });

    /* magnetic: the element is pulled toward the cursor, then springs back */
    document.querySelectorAll("[data-magnetic]").forEach(function (el) {
      var strength = parseFloat(el.getAttribute("data-magnetic")) || 0.3;
      var raf = null;
      el.addEventListener("mousemove", function (ev) {
        var r = el.getBoundingClientRect();
        var dx = ev.clientX - (r.left + r.width / 2);
        var dy = ev.clientY - (r.top + r.height / 2);
        if (!raf) raf = requestAnimationFrame(function () {
          raf = null;
          el.style.transform = "translate(" + (dx * strength).toFixed(1) + "px," + (dy * strength).toFixed(1) + "px)";
        });
      });
      el.addEventListener("mouseleave", function () {
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        el.style.transform = "translate(0,0)";
      });
    });

    /* hero parallax: the index panel drifts slower than scroll, for depth */
    var heroIndex = document.querySelector(".hero-index");
    var heroTitle = document.querySelector(".hero-main");
    if (heroIndex && heroTitle) {
      var pRaf = null;
      function parallax() {
        pRaf = null;
        var y = window.scrollY;
        if (y > 600) return;
        heroIndex.style.transform = "translateY(" + (y * 0.12).toFixed(1) + "px)";
        heroTitle.style.transform = "translateY(" + (y * 0.05).toFixed(1) + "px)";
      }
      window.addEventListener("scroll", function () {
        if (!pRaf) pRaf = requestAnimationFrame(parallax);
      }, { passive: true });
    }
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

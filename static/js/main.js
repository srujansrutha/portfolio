/* THE KUMAR CUT — interactive controller (vanilla, FastAPI build) */
(function () {
  "use strict";

  var projects = {
    "agentic-rag": { badge: "FEATURED · GitHub", title: "Agentic ChatBot", tagline: "LangGraph agent · ClickHouse + MongoDB tools · document & image RAG", desc: "A LangGraph agent on FastAPI that queries ClickHouse and MongoDB tools to give business-friendly answers, with RAG over PDF/DOCX and multimodal image RAG using CLIP.", features: ["LangGraph agent on FastAPI querying ClickHouse and MongoDB tools for business-friendly answers.", "RAG over PDF/DOCX with sentence-transformer embeddings, plus multimodal image RAG using CLIP.", "Short- and long-term memory via Redis conversation history and LangGraph SQLite checkpointing.", "Guardrails, token-based security, automated tests, an evaluation script and Docker Compose deployment."], stack: ["FastAPI", "LangGraph", "LangChain", "Ollama", "Redis", "MongoDB", "ClickHouse", "CLIP", "Docker"], github: "https://github.com/srujansrutha/Agentic-Bot" },
    "wheat-detection": { badge: "COMPUTER VISION · Intel AI for Youth", title: "Global Wheat Detection", tagline: "YOLO11 detection, held-out-farm evaluation + LoRA-tuned Qwen2.5 advisor", desc: "YOLO11s fine-tuned on 148K annotations (3.4K images, 7 farms) and evaluated on held-out farms, paired with a LoRA fine-tuned Qwen2.5-3B-Instruct that gives crop-quality and fertilizer advice.", features: ["0.945 mAP@50 in-domain and 0.890 on held-out farms.", "Source-disjoint train/val/OOD split; traced a 0.15 mAP@50-95 domain-shift gap to object scale and density.", "LoRA fine-tuned Qwen2.5-3B-Instruct for crop-quality and fertilizer advice.", "Served through a FastAPI inference endpoint."], stack: ["YOLO11", "PyTorch", "Ultralytics", "Qwen2.5", "LoRA/PEFT", "FastAPI"], github: "https://github.com/srujansrutha/GWD-workflow" },
    "mcp-fashion-analytics": { badge: "PRODUCTION AI · TrendGully", title: "MCP Fashion Analytics", tagline: "Natural-language querying over ClickHouse", desc: "An MCP-powered LLM analytics agent that integrates the fashion-analytics data layer through an MCP server, so business stakeholders can query datasets in natural language.", features: ["MCP server over the fashion-analytics data layer, with tool bindings for LLM context.", "ClickHouse backend — analytical queries cut from ~6–7 s to ~1–2 s after the MongoDB migration.", "Companion work: Qwen3-VL fine-tuned with QLoRA for attribute labeling, 98% accuracy on a held-out set."], stack: ["MCP", "ClickHouse", "MongoDB", "Python", "Qwen3-VL"] },
    "cloud-cost-agent": { badge: "ENTERPRISE · Ellucian", title: "AWS Cloud Cost Optimization Agent", tagline: "SageMaker predictive analytics + multi-agent recommender · −20% spend", desc: "An AI-driven cloud cost optimization dashboard on AWS SageMaker with predictive analytics, plus a multi-agent recommendation system integrating multiple AWS services for resource optimization.", features: ["Cut cloud costs 20% and improved utilization 15% with predictive analytics.", "Multi-agent recommendation system integrating multiple AWS services.", "Fine-tuned an LLM code-generation system that converts natural-language prompts into executable code."], stack: ["SageMaker", "AWS", "Multi-Agent", "Python", "Predictive Analytics"] }
  };

  var busy = false;
  var cutA, cutB;

  document.addEventListener("DOMContentLoaded", function () {
    initHeroVideo();
    initReveals();
    initMagnetic();
    initTilt();
    initNav();
    initChat();
    initModal();
    initPalette();
    initContact();
    initPageCuts();
  });

  /* ---------- hero video: seamless background loop + elapsed timer ---------- */
  function initHeroVideo() {
    var v = document.getElementById("hero-video");
    if (v) {
      v.muted = true; v.loop = true;
      var userPaused = false;
      var play = function () { var p = v.play && v.play(); if (p && p.catch) p.catch(function () {}); };
      play();
      // the HUD's "PLAY" label is a real pause/play control for the background loop
      var tog = document.querySelector("[data-hero-toggle]");
      if (tog) {
        var label = function () {
          tog.textContent = v.paused ? "▮▮ PAUSED ▶" : "▶ PLAY ▮▮";
          tog.setAttribute("aria-label", v.paused ? "Play background video" : "Pause background video");
        };
        tog.addEventListener("click", function () { if (v.paused) { userPaused = false; play(); } else { userPaused = true; v.pause(); } });
        v.addEventListener("play", label); v.addEventListener("pause", label); label();
      }
      // autoplay can be blocked (battery saver, strict browser settings): start on the first interaction instead
      var kick = function () { if (v.paused && !userPaused) play(); };
      ["pointerdown", "keydown", "touchstart", "scroll"].forEach(function (ev) { window.addEventListener(ev, kick, { once: true, passive: true }); });
    }
    var tc = document.querySelector("[data-timecode]");
    if (tc) {
      var t0 = performance.now();
      var tick = function () {
        var s = (performance.now() - t0) / 1000;
        var hh = String(Math.floor(s / 3600)).padStart(2, "0");
        var mm = String(Math.floor(s / 60) % 60).padStart(2, "0");
        var ss = String(Math.floor(s) % 60).padStart(2, "0");
        var ff = String(Math.floor((s % 1) * 24)).padStart(2, "0");
        tc.textContent = hh + ":" + mm + ":" + ss + ":" + ff;
      };
      setInterval(tick, 42); tick();
    }
  }

  /* ---------- scroll reveals + counters + VU bars ---------- */
  function initReveals() {
    var els = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]"));
    els.forEach(function (el) {
      el.style.opacity = "0";
      el.style.transform = "translateY(30px) scale(0.99)";
      el.style.filter = "blur(6px)";
      el.style.transition = "opacity 0.45s ease, transform 0.5s cubic-bezier(0.2,0.85,0.25,1), filter 0.45s ease";
    });
    var reveal = function (el) {
      el.style.opacity = "1"; el.style.transform = "none"; el.style.filter = "none";
      animateCounters(el); animateBars(el);
    };
    if (!("IntersectionObserver" in window)) { els.forEach(reveal); return; }
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { reveal(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
    setTimeout(function () { els.forEach(function (el) { if (el.style.opacity === "0") reveal(el); }); }, 3500);
  }
  function animateCounters(scope) {
    scope.querySelectorAll("[data-count]").forEach(function (el) {
      if (el.dataset.done) return; el.dataset.done = "1";
      var target = parseFloat(el.dataset.target), dec = parseInt(el.dataset.decimals || "0"), dur = 1400, t0 = performance.now();
      var step = function (t) {
        var p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3), val = target * e;
        el.textContent = dec ? val.toFixed(dec) : Math.round(val).toString();
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
  }
  function animateBars(scope) {
    scope.querySelectorAll("[data-bar]").forEach(function (el) { el.style.width = el.dataset.pct + "%"; });
  }

  /* ---------- magnetic buttons ---------- */
  function initMagnetic() {
    document.querySelectorAll("[data-magnetic]").forEach(function (el) {
      el.style.transition = "transform 0.25s cubic-bezier(0.22,1,0.36,1)";
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        el.style.transform = "translate(" + ((e.clientX - (r.left + r.width / 2)) * 0.28) + "px," + ((e.clientY - (r.top + r.height / 2)) * 0.4) + "px)";
      });
      el.addEventListener("mouseleave", function () { el.style.transform = "translate(0,0)"; });
    });
  }

  /* ---------- 3D tilt case-file cards ---------- */
  function initTilt() {
    document.querySelectorAll("[data-tilt]").forEach(function (el) {
      el.style.transition = "transform 0.2s ease, border-color 0.3s";
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = "perspective(900px) rotateY(" + (px * 8) + "deg) rotateX(" + (-py * 8) + "deg) translateZ(6px)";
        el.style.borderColor = "rgba(255,46,58,0.6)";
      });
      el.addEventListener("mouseleave", function () {
        el.style.transform = "perspective(900px) rotateY(0) rotateX(0)";
        el.style.borderColor = "rgba(255,46,58,0.22)";
      });
      el.addEventListener("click", function () { openModal(el.dataset.project); });
    });
  }

  /* ---------- nav: scrubber + scrollspy + cinematic cut ---------- */
  function initNav() {
    var nav = document.querySelector("[data-nav]"), scrub = document.querySelector("[data-scrub]");
    var onScroll = function () {
      if (scrub) { var h = document.documentElement.scrollHeight - window.innerHeight; scrub.style.width = (h > 0 ? (window.scrollY / h * 100) : 0) + "%"; }
      if (window.scrollY > 40) { nav.style.background = "rgba(5,5,6,0.85)"; nav.style.backdropFilter = "blur(16px)"; nav.style.borderBottomColor = "rgba(255,46,58,0.25)"; }
      else { nav.style.background = "transparent"; nav.style.backdropFilter = "none"; nav.style.borderBottomColor = "transparent"; }
      var cur = "";
      document.querySelectorAll("section[id]").forEach(function (s) { if (window.scrollY >= s.offsetTop - 200) cur = s.id; });
      document.querySelectorAll("[data-navlink]").forEach(function (a) { a.style.color = a.dataset.navlink === cur ? "#FF6B5E" : "#8A93A3"; });
    };
    window.addEventListener("scroll", onScroll); onScroll();
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      var id = a.getAttribute("href").slice(1); if (!id) return;
      a.addEventListener("click", function (e) { e.preventDefault(); scrollToId(id); });
    });
  }
  function cutTo(id, label) {
    var el = document.getElementById(id); if (!el) return;
    var cut = document.querySelector("[data-cut]"), lab = document.querySelector("[data-cut-label]"), bar = document.querySelector("[data-cut-bar]");
    var go = function () { window.scrollTo({ top: Math.max(0, el.offsetTop - 70), behavior: "auto" }); };
    if (!cut) { go(); return; }
    if (lab) lab.textContent = label || "CUT";
    cut.style.pointerEvents = "all"; cut.style.opacity = "1";
    if (bar) { bar.style.transition = "none"; bar.style.width = "0"; requestAnimationFrame(function () { bar.style.transition = "width 0.5s linear"; bar.style.width = "100%"; }); }
    clearTimeout(cutA); clearTimeout(cutB);
    cutA = setTimeout(go, 210);
    cutB = setTimeout(function () { cut.style.opacity = "0"; cut.style.pointerEvents = "none"; }, 560);
  }
  function scrollToId(id) {
    // off the home page (e.g. /mlops) the section lives on "/", so go there instead
    if (!document.getElementById(id)) { window.location.href = "/#" + id; return; }
    var m = { hero: "The Kumar Cut", work: "The Work", experience: "The Record", skills: "The Toolkit", achievements: "Roll Credits", contact: "Final Scene", top: "MLOps", projects: "The Pipeline", stack: "The Stack", hire: "Final Scene" };
    cutTo(id, m[id] || id);
  }

  /* ---------- cinematic cut between pages (e.g. home -> /mlops) ---------- */
  function goPage(href, label) {
    var cut = document.querySelector("[data-cut]"), lab = document.querySelector("[data-cut-label]"), bar = document.querySelector("[data-cut-bar]");
    if (!cut) { window.location.href = href; return; }
    if (lab) lab.textContent = label || "CUT";
    cut.style.pointerEvents = "all"; cut.style.opacity = "1";
    if (bar) { bar.style.transition = "none"; bar.style.width = "0"; requestAnimationFrame(function () { bar.style.transition = "width 0.5s linear"; bar.style.width = "100%"; }); }
    setTimeout(function () { window.location.href = href; }, 420);
  }
  function initPageCuts() {
    document.querySelectorAll("a[data-cut-page]").forEach(function (a) {
      a.addEventListener("click", function (e) {
        if (e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        e.preventDefault(); goPage(a.getAttribute("href"), a.dataset.cutPage);
      });
    });
    // returning with the browser's back button can restore the page with the cut overlay still showing
    window.addEventListener("pageshow", function (e) {
      var cut = document.querySelector("[data-cut]");
      if (e.persisted && cut) { cut.style.opacity = "0"; cut.style.pointerEvents = "none"; }
    });
  }

  /* ---------- COMMS chat (server /api/chat) ---------- */
  function addBubble(text, who) {
    var wrap = document.querySelector("[data-chat-messages]"), b = document.createElement("div");
    b.style.cssText = "max-width:88%;padding:13px 16px;font-size:14px;line-height:1.55;white-space:pre-wrap;" + (who === "user" ? "background:#FF2E3A;color:#fff;font-weight:500;align-self:flex-end;" : "background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#D7DEE8;align-self:flex-start;");
    b.textContent = text; wrap.appendChild(b); wrap.scrollTop = wrap.scrollHeight; return b;
  }
  function sendChat(text) {
    if (!text || busy) return; busy = true;
    addBubble(text, "user");
    var typing = addBubble("•••", "bot"); typing.style.fontFamily = "'JetBrains Mono',monospace";
    var d = 0, iv = setInterval(function () { d = (d + 1) % 4; typing.textContent = new Array((d || 1) + 1).join("•"); }, 350);
    fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: text }) })
      .then(function (r) { return r.json(); })
      .then(function (data) { clearInterval(iv); typing.textContent = data.response || "…"; typing.style.fontFamily = ""; })
      .catch(function () { clearInterval(iv); typing.textContent = "Signal lost — reach Srujan directly at srujansrutha01@gmail.com."; typing.style.fontFamily = ""; })
      .then(function () { var w = document.querySelector("[data-chat-messages]"); if (w) w.scrollTop = 1e9; busy = false; });
  }
  function openChat() {
    var dw = document.querySelector("[data-chat-drawer]");
    dw.style.opacity = "1"; dw.style.pointerEvents = "all"; dw.style.transform = "translateY(0) scale(1)";
    var i = document.querySelector("[data-chat-input]"); if (i) i.focus();
  }
  function closeChat() {
    var dw = document.querySelector("[data-chat-drawer]");
    dw.style.opacity = "0"; dw.style.pointerEvents = "none"; dw.style.transform = "translateY(16px) scale(0.98)";
  }
  function initChat() {
    document.querySelectorAll("[data-open-chat]").forEach(function (b) { b.addEventListener("click", openChat); });
    var close = document.querySelector("[data-close-chat]"); if (close) close.addEventListener("click", closeChat);
    var input = document.querySelector("[data-chat-input]");
    var send = document.querySelector("[data-chat-send]");
    if (send) send.addEventListener("click", function () { var v = input.value.trim(); input.value = ""; sendChat(v); });
    if (input) input.addEventListener("keypress", function (e) { if (e.key === "Enter") { var v = input.value.trim(); input.value = ""; sendChat(v); } });
    document.querySelectorAll("[data-suggest]").forEach(function (b) { b.addEventListener("click", function () { sendChat(b.dataset.suggest); }); });
  }

  /* ---------- CASE FILE modal ---------- */
  function openModal(id) {
    var p = projects[id]; if (!p) return;
    document.querySelector("[data-modal-body]").innerHTML =
      '<div style="font-family:\'JetBrains Mono\',monospace;font-size:11px;letter-spacing:1px;color:#FF6B5E;background:rgba(255,46,58,0.12);border:1px solid rgba(255,46,58,0.3);display:inline-block;padding:5px 12px;margin-bottom:16px;">CASE FILE · ' + p.badge + '</div>' +
      '<h2 style="font-family:\'Space Grotesk\',sans-serif;font-size:28px;font-weight:700;text-transform:uppercase;margin:0 0 8px;color:#F3F6FB;">' + p.title + '</h2>' +
      '<div style="color:#FF2E3A;font-weight:600;font-size:14px;margin-bottom:20px;font-family:\'JetBrains Mono\',monospace;">' + p.tagline + '</div>' +
      '<p style="color:#9AA4B4;font-size:15px;line-height:1.7;margin:0 0 26px;">' + p.desc + '</p>' +
      '<div style="font-family:\'JetBrains Mono\',monospace;font-size:11px;letter-spacing:1.5px;color:#FF6B5E;margin-bottom:12px;">KEY DELIVERABLES</div>' +
      '<ul style="list-style:none;margin:0 0 26px;padding:0;display:flex;flex-direction:column;gap:10px;">' + p.features.map(function (f) { return '<li style="position:relative;padding-left:24px;color:#B9C4D4;font-size:14.5px;line-height:1.6;"><span style="position:absolute;left:0;color:#FF2E3A;">✓</span>' + f + '</li>'; }).join("") + '</ul>' +
      '<div style="font-family:\'JetBrains Mono\',monospace;font-size:11px;letter-spacing:1.5px;color:#FF6B5E;margin-bottom:12px;">TECH STACK</div>' +
      '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:28px;">' + p.stack.map(function (t) { return '<span style="font-family:\'JetBrains Mono\',monospace;font-size:12px;color:#FF6B5E;background:rgba(255,46,58,0.1);border:1px solid rgba(255,46,58,0.25);padding:5px 12px;">' + t + '</span>'; }).join("") + '</div>' +
      (p.github
        ? '<a href="' + p.github + '" target="_blank" style="display:inline-flex;align-items:center;gap:8px;background:#FF2E3A;color:#fff;font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:13px;letter-spacing:1px;padding:12px 22px;">VIEW GITHUB REPO →</a>'
        : '<div style="font-family:\'JetBrains Mono\',monospace;font-size:12px;letter-spacing:1px;color:#6a7280;border:1px solid rgba(255,255,255,0.1);display:inline-block;padding:10px 16px;">SOURCE NOT PUBLIC · EMPLOYER WORK</div>');
    var ov = document.querySelector("[data-modal-overlay]"); ov.style.opacity = "1"; ov.style.pointerEvents = "all";
  }
  function closeModal() { var ov = document.querySelector("[data-modal-overlay]"); ov.style.opacity = "0"; ov.style.pointerEvents = "none"; }
  function initModal() {
    var close = document.querySelector("[data-close-modal]"); if (close) close.addEventListener("click", closeModal);
    var ov = document.querySelector("[data-modal-overlay]"); if (ov) ov.addEventListener("click", function (e) { if (e.target === ov) closeModal(); });
  }

  /* ---------- SCENE SELECT command palette ---------- */
  function initPalette() {
    var onMlops = window.location.pathname.indexOf("/mlops") === 0;
    var cmds = [
      onMlops ? { label: "Back to Portfolio", hint: "page", act: function () { goPage("/", "PORTFOLIO"); } }
              : { label: "MLOps Projects", hint: "page", act: function () { goPage("/mlops", "MLOPS"); } },
      { label: "Scene 01 · The Work", hint: "jump", act: function () { scrollToId("work"); } },
      { label: "Scene 02 · The Record", hint: "jump", act: function () { scrollToId("experience"); } },
      { label: "Scene 03 · The Toolkit", hint: "jump", act: function () { scrollToId("skills"); } },
      { label: "Roll Credits", hint: "jump", act: function () { scrollToId("achievements"); } },
      { label: "Final Scene · Contact", hint: "jump", act: function () { scrollToId("contact"); } },
      { label: "Open COMMS", hint: "action", act: function () { openChat(); } },
      { label: "Email Srujan", hint: "contact", act: function () { window.location.href = "mailto:srujansrutha01@gmail.com"; } },
      { label: "GitHub", hint: "link", act: function () { window.open("https://github.com/srujansrutha", "_blank"); } },
      { label: "LinkedIn", hint: "link", act: function () { window.open("https://linkedin.com/in/srujan-vishwakarma", "_blank"); } }
    ];
    var ov = document.querySelector("[data-palette-overlay]"), list = document.querySelector("[data-palette-list]"), input = document.querySelector("[data-palette-input]");
    if (!ov) return;
    var sel = 0, filtered = cmds.slice();
    var render = function () {
      list.innerHTML = "";
      filtered.forEach(function (c, i) {
        var row = document.createElement("div");
        row.style.cssText = "display:flex;justify-content:space-between;align-items:center;padding:12px 14px;cursor:pointer;" + (i === sel ? "background:rgba(255,46,58,0.15);" : "");
        row.innerHTML = '<span style="color:' + (i === sel ? "#F3F6FB" : "#C7D0DC") + ';font-size:14px;font-family:\'JetBrains Mono\',monospace;">' + c.label + '</span><span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:#5b6576;">' + c.hint + '</span>';
        row.addEventListener("mouseenter", function () { sel = i; render(); });
        row.addEventListener("click", function () { close(); c.act(); });
        list.appendChild(row);
      });
    };
    var open = function () { ov.style.opacity = "1"; ov.style.pointerEvents = "all"; input.value = ""; filtered = cmds.slice(); sel = 0; render(); setTimeout(function () { input.focus(); }, 40); };
    var close = function () { ov.style.opacity = "0"; ov.style.pointerEvents = "none"; };
    input.addEventListener("input", function () { var q = input.value.toLowerCase(); filtered = cmds.filter(function (c) { return c.label.toLowerCase().indexOf(q) !== -1; }); sel = 0; render(); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); sel = Math.min(sel + 1, filtered.length - 1); render(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); sel = Math.max(sel - 1, 0); render(); }
      else if (e.key === "Enter") { e.preventDefault(); if (filtered[sel]) { close(); filtered[sel].act(); } }
    });
    document.querySelectorAll("[data-open-palette]").forEach(function (b) { b.addEventListener("click", open); });
    ov.addEventListener("click", function (e) { if (e.target === ov) close(); });
    window.addEventListener("keydown", function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); ov.style.opacity === "1" ? close() : open(); }
      if (e.key === "Escape") { close(); closeModal(); closeChat(); }
    });
  }

  /* ---------- contact form (server /api/contact) ---------- */
  function initContact() {
    var form = document.querySelector("[data-contact-form]"); if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = form.querySelector("[data-cf=name]").value;
      var email = form.querySelector("[data-cf=email]").value;
      var message = form.querySelector("[data-cf=message]").value;
      var status = document.querySelector("[data-cf-status]");
      status.style.display = "block"; status.textContent = "● TRANSMITTING…";
      fetch("/api/contact", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: name, email: email, message: message }) })
        .then(function (r) { return r.json(); })
        .then(function (data) { status.textContent = "● " + (data.message || "Message sent."); form.reset(); })
        .catch(function () { status.textContent = "● Failed — email srujansrutha01@gmail.com directly."; });
    });
  }
})();

/* /mlops page — pipeline-stage filter for the project cards */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var chips = document.querySelectorAll("[data-stage-filter]");
    var cells = document.querySelectorAll("[data-stages]");
    var count = document.querySelector("[data-ml-count]");
    if (!chips.length || !cells.length) return;

    function apply(stage) {
      var shown = 0;
      cells.forEach(function (c) {
        var on = stage === "all" || c.dataset.stages.split(" ").indexOf(stage) !== -1;
        c.hidden = !on;
        if (on) shown++;
      });
      chips.forEach(function (b) {
        var active = b.dataset.stageFilter === stage;
        b.classList.toggle("is-active", active);
        b.setAttribute("aria-pressed", active ? "true" : "false");
      });
      if (count) count.textContent = "SHOWING " + shown + " OF " + cells.length;
    }

    chips.forEach(function (b) {
      b.addEventListener("click", function () { apply(b.dataset.stageFilter); });
    });

    // deep link: /mlops#deploy opens with that stage selected
    var h = decodeURIComponent(location.hash.slice(1));
    if (h && document.querySelector('[data-stage-filter="' + h + '"]')) apply(h);
  });
})();

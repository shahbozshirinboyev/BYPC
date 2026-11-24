(function () {
  "use strict";

  function init() {
    var chipset = document.getElementById("id_chipset");
    var target = document.querySelector(".aio-socket");
    if (!chipset || !target) return;

    var map = {};
    try {
      map = JSON.parse(target.dataset.map || "{}");
    } catch (err) {
      map = {};
    }

    function update() {
      target.textContent = map[chipset.value] || "—";
    }

    chipset.addEventListener("change", update);
    update();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

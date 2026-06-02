(function () {
  var container = document.getElementById("pano");
  var fsBtn = document.getElementById("btn-fullscreen");
  if (!container || typeof pannellum === "undefined") {
    return;
  }

  var viewer = pannellum.viewer("pano", {
    type: "equirectangular",
    panorama: "panorama/office.jpg",
    autoLoad: true,
    showControls: true,
    compass: false,
    haov: 360,
    vaov: 90,
    vOffset: 0,
    hfov: 95,
    minHfov: 50,
    maxHfov: 120,
    pitch: -4,
    yaw: 0,
    friction: 0.12,
    mouseZoom: true,
    keyboardZoom: true,
  });

  if (fsBtn) {
    fsBtn.addEventListener("click", function () {
      var root = document.querySelector(".tour--pano");
      if (!root) return;
      if (!document.fullscreenElement) {
        root.requestFullscreen().catch(function () {});
      } else {
        document.exitFullscreen();
      }
    });
  }

  window.officeTourViewer = viewer;
})();

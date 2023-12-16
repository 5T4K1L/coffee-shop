document.addEventListener("DOMContentLoaded", () => {
  var trackOrder = new WebSocket(`ws://${window.location.host}/track-order/`);

  trackOrder.onmessage = function (e) {
    var data = JSON.parse(e.data);

    if (data.status == "track_order") {
      location.reload();
    }
  };
});

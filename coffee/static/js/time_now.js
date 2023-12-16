document.addEventListener("DOMContentLoaded", function () {
  var socket = new WebSocket(`ws://${window.location.host}/time/`);

  socket.onmessage = (e) => {
    var timeData = JSON.parse(e.data);
    document.getElementById("time").innerText = timeData.time;
  };
});

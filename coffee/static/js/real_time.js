document.addEventListener("DOMContentLoaded", function () {
  var socket = new WebSocket(`ws://${window.location.host}/orders/`);

  socket.onmessage = function (e) {
    var data = JSON.parse(e.data);

    if (data.status == "notification") {
      var notificationData = data.value.users;
      console.log(notificationData);
      if (notificationData) {
        // Store the current scroll position
        var scrollPos =
          window.scrollY ||
          window.scrollTop ||
          document.getElementsByTagName("html")[0].scrollTop;

        // Reload the page
        location.reload();

        // Set the scroll position back after the reload
        window.scrollTo(0, scrollPos);
      }
    }
  };
});

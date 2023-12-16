document.addEventListener("DOMContentLoaded", () => {
  let name = document.getElementById("name");
  let contact = document.getElementById("contact");
  let address = document.getElementById("address");
  let checkout = document.getElementById("checkout");

  let errorMessage = document.getElementById("errorMessage");

  checkout.addEventListener("click", (e) => {
    if (name.value == "" || contact.value == "" || address.value == "") {
      errorMessage.innerText = `First Name,
      Contact Number and
      Full Address can't be blank`;
      e.preventDefault();
    }
  });
});

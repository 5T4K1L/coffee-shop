document.addEventListener("DOMContentLoaded", () => {
  const quantity = document.getElementById("quantity");
  const sizeSelect = document.getElementById("size");

  function getTotal() {
    const sizeSelectValue = document.getElementById("size").value;

    if (sizeSelectValue === "small") {
      console.log("{{product.smallprice}}" * quantity);
    }
  }

  quantity.addEventListener("change", getTotal());
  sizeSelect.addEventListener("change", getTotal());
});

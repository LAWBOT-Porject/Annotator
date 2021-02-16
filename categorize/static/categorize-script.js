// Get the modal
// let modal = document.querySelectorAll('dev[id^="myModal"]');

// // When the user clicks anywhere outside of the modal, close it
// window.onclick = function (event) {
//   console.log("Mohamed");
//   modal.forEach((item) => {
//     if (event.target == item) {
//       item.style.display = "none";
//     }
//   });
// };

document.querySelectorAll('span[class^="categorie-info-"]').forEach((item) => {
  let index = item.className.split("-")[2];
  item.addEventListener("click", () => {
    document.getElementById("myModal-" + index).style.display = "block";
  });
});

document.querySelectorAll('span[class^="close-"]').forEach((item) => {
  let index2 = item.className.split("-")[1];
  item.addEventListener("click", () => {
    document.getElementById("myModal-" + index2).style.display = "none";
  });
});

document.querySelectorAll('span[class^="norme-info-"]').forEach((item) => {
  let index = item.className.split("-")[2];
  item.addEventListener("click", () => {
    document.getElementById("myModalNorme-" + index).style.display = "block";
  });
});

document.querySelectorAll('span[class^="closenorme-"]').forEach((item) => {
  let index2 = item.className.split("-")[1];
  item.addEventListener("click", () => {
    document.getElementById("myModalNorme-" + index2).style.display = "none";
  });
});

const displayNormeForm = () => {
  let newNormContainer = document.querySelector(".create-norme-container");
  newNormContainer.style.display = "block";
  newNormContainer.style["height"] = "100%";
  newNormContainer.style["width"] = "100%";
  newNormContainer.style["margin"] = "0 auto";
  document.getElementById("normes-ul").style.display = "none";
  document.querySelector(".normes-title").style.display = "none";
  let normForm = document.querySelector("form.new-norm-form");
  normForm.style.display = "flex";
  normForm.style["height"] = "100%";
  normForm.style["width"] = "100%";
  normForm.style["margin"] = "0 auto";
  normForm.style["flex-direction"] = "column";
  normForm.style["justify-content"] = "right";
  normForm.style["align-items"] = "center";
};

const displayCategoryForm = () => {
  let newCategoryContainer = document.querySelector(
    ".create-category-container"
  );
  newCategoryContainer.style.display = "block";
  newCategoryContainer.style["height"] = "100%";
  newCategoryContainer.style["width"] = "100%";
  newCategoryContainer.style["margin"] = "0 auto";
  document.getElementById("categories-ul").style.display = "none";
  document.querySelector(".categories-title").style.display = "none";
  let normForm = document.querySelector("form.new-category-form");
  normForm.style.display = "flex";
  normForm.style["height"] = "100%";
  normForm.style["width"] = "100%";
  normForm.style["margin"] = "0 auto";
  normForm.style["flex-direction"] = "column";
  normForm.style["justify-content"] = "right";
  normForm.style["align-items"] = "center";
};

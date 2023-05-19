var el = document.getElementById("wrapper");
var toggleButton = document.getElementById("menu-toggle");
var sidebar = document.getElementById("sidebar-wrapper");
toggleButton.onclick = function () {
    el.classList.toggle("toggled");
};

// Esto Causa problemas
// sidebar.addEventListener("mouseover", function () {
//     if (el.classList.contains("toggled")) {
//         el.classList.toggle("toggler");
//         el.classList.toggle("toggled");
//     }
// });

// sidebar.addEventListener("mouseout", function () {
//     if (el.classList.contains("toggler")) {
//         el.classList.toggle("toggler");
//         el.classList.toggle("toggled");
//     }
// });
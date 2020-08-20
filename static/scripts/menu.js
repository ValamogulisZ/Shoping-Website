var nav = document.querySelector(".nav-bar");
var nav_swich = false;

function scrollCheck(y) {
  if (y > 30 && !nav_swich) {
    nav_swich = true;
    nav.classList.add("not-top");
  } else if (y <= 30 && nav_swich) {
    nav_swich = false;
    nav.classList.remove("not-top");
  }
}

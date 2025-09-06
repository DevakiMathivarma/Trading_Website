// Fade animation on scroll
document.addEventListener("scroll", function () {
  document.querySelectorAll(".fade-left, .fade-right, .fade-up").forEach(el => {
    let position = el.getBoundingClientRect().top;
    let screenHeight = window.innerHeight;
    if (position < screenHeight - 100) {
      el.classList.add("fade-in");
    }
  });
});

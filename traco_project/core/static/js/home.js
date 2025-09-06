// static/js/home.js
document.addEventListener("DOMContentLoaded", function () {
  function getCookie(name) {
    let v = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
    return v ? v.pop() : "";
  }

  const form = document.getElementById("traco-news-form");
  if (!form) return;
  const emailInput = document.getElementById("traco-news-email");
  const btn = form.querySelector(".traco-news-btn");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const email = (emailInput.value || "").trim();

    if (!email) {
      animateError("Please enter your email");
      return;
    }
    if (!/@/.test(email) || !/\.com$/i.test(email)) {
      animateError("Please enter a valid email (must include @ and .com)");
      return;
    }

    btn.disabled = true;
    btn.classList.add("traco-btn--loading");

    const data = new FormData();
    data.append("email", email);

    fetch(form.action, {
      method: "POST",
      body: data,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "X-Requested-With": "XMLHttpRequest",
      },
      credentials: "same-origin",
    })
      .then((resp) =>
        resp
          .json()
          .catch(() => ({ ok: false, error: "Invalid server response" }))
      )
      .then((json) => {
        btn.disabled = false;
        btn.classList.remove("traco-btn--loading");
        if (json.ok) {
          showSuccessAnimation(json.message || "Subscribed");
          alert("You are subscribed — Thank you for subscribing to TRACO!");
          emailInput.value = "";
        } else {
          animateError(json.error || "Subscription failed");
        }
      })
      .catch((err) => {
        btn.disabled = false;
        btn.classList.remove("traco-btn--loading");
        animateError("Network error. Try again.");
      });
  });

  function animateError(msg) {
    const p = document.createElement("div");
    p.className = "traco-news-error";
    p.innerText = msg;
    form.appendChild(p);
    setTimeout(() => p.classList.add("visible"), 16);
    setTimeout(() => p.classList.remove("visible"), 4000);
    setTimeout(() => p.remove(), 4400);
  }

  function showSuccessAnimation(msg) {
    const card = document.createElement("div");
    card.className = "traco-news-success";
    card.innerHTML =
      "<strong>Subscribed</strong><div>" + (msg || "Thank you") + "</div>";
    document.body.appendChild(card);
    setTimeout(() => card.classList.add("show"), 10);
    setTimeout(() => card.classList.remove("show"), 3500);
    setTimeout(() => card.remove(), 4200);
  }


});
  document.addEventListener("DOMContentLoaded", function () {
    document
      .querySelectorAll(".how-step, .reveal-in, .reveal-up, .reveal-fade")
      .forEach((el) => {
        el.classList.add("show");
        // also ensure any parent wrappers visible
        let p = el.parentElement;
        while (p) {
          p.style.opacity = 1;
          p.style.visibility = "visible";
          p = p.parentElement;
        }
      });
  });

  document.addEventListener("DOMContentLoaded", function () {
  // simple fade-in for hero
  const hero = document.querySelector(".hero-banner .hero-inner");
  if (hero) {
    hero.style.opacity = 0;
    hero.style.transform = "translateY(8px)";
    setTimeout(() => {
      hero.style.transition = "all 600ms cubic-bezier(.2,.9,.2,1)";
      hero.style.opacity = 1;
      hero.style.transform = "translateY(0)";
    }, 60);
  }

  // avatars tiny float on interval
  document.querySelectorAll(".avatars .avatar").forEach((av, i) => {
    av.style.transition = "transform .28s ease, box-shadow .28s ease";
    av.addEventListener("mouseenter", () => av.style.transform = "translateY(-8px) scale(1.06)");
    av.addEventListener("mouseleave", () => av.style.transform = "none");
  });
});


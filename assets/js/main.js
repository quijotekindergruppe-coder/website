// Quijote website – small enhancements. Everything works without JavaScript;
// this adds the phone menu and the contact-form routing.
document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", function () {
  // ---- Phone menu ----
  var header = document.querySelector(".header");
  var btn = document.querySelector(".menu-btn");
  if (header && btn) {
    btn.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.classList.contains("is-open")) {
        header.classList.remove("is-open");
        btn.setAttribute("aria-expanded", "false");
        btn.focus();
      }
    });
  }

  // ---- Contact form: send each topic to the right inbox ----
  // Routing lives in content/site.json ("form" → "route"); the build writes it
  // onto each <option> as data-route.
  var form = document.getElementById("contact-form");
  if (!form) return;
  var topic = form.querySelector("#topic");
  var recipient = document.getElementById("recipient");
  var subject = form.querySelector('input[name="_subject"]');
  var next = form.querySelector('input[name="_next"]');
  var endpoint = form.getAttribute("data-endpoint");

  // After sending, come back to our own thank-you page (works on the preview
  // address and on www.quijote.at alike).
  next.value = new URL(form.getAttribute("data-thanks"), location.href).href;

  function update() {
    var opt = topic.options[topic.selectedIndex];
    var key = opt.getAttribute("data-key");
    var route = opt.getAttribute("data-route");
    form.action = endpoint + route;
    recipient.textContent = route;
    subject.value = "Quijote Website: " + opt.textContent.trim();
    form.querySelectorAll("[data-show-for]").forEach(function (field) {
      var show = field.getAttribute("data-show-for").split(" ").indexOf(key) !== -1;
      field.hidden = !show;
      field.querySelectorAll("input, select, textarea").forEach(function (el) { el.disabled = !show; });
    });
  }
  topic.addEventListener("change", update);
  update();
});

document.addEventListener("DOMContentLoaded", function () {
  const faqQuestions = document.querySelectorAll(".faq-question");

  faqQuestions.forEach(function (question) {
    question.addEventListener("click", function () {
      const answer = this.nextElementSibling;
      answer.style.display =
        answer.style.display === "block" ? "none" : "block";
    });
  });

  const form = document.getElementById("query-form");
  const formMessage = document.getElementById("form-message");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    formMessage.style.display = "none";

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();

    if (name === "" || email === "" || message === "") {
      formMessage.textContent = "Please fill out all fields.";
      formMessage.style.display = "block";
      return;
    }

    if (!validateEmail(email)) {
      formMessage.textContent = "Please enter a valid email address.";
      formMessage.style.display = "block";
      return;
    }

    formMessage.textContent = "Thank you for your message!";
    formMessage.style.color = "#28a745";
    formMessage.style.display = "block";

    form.reset();
  });

  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }
});

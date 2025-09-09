// JavaScript function to show the spinner when the form is submitted
function showLoading() {
    // Show the spinner
    document.getElementById('spinner-container').style.display = 'flex';
    // Optionally, hide the form so the user can't submit multiple times
    document.getElementById('user-form').style.display = 'none';
    document.getElementById('form-container').style.display = 'none';
}

document.addEventListener("DOMContentLoaded", function () {
  let currentSlide = 1;
  const totalSlides = 4;

  const backBtn = document.getElementById("back");
  const nextBtn = document.getElementById("next");
  const submitBtn = document.getElementById("submit");
  const personalizeBtn = document.getElementById("personalize");

  function showSlide(slideNumber) {
    // Hide all slides
    for (let i = 1; i <= totalSlides; i++) {
      document.getElementById(`slide${i}`).style.display = "none";
    }

    // Show current slide
    document.getElementById(`slide${slideNumber}`).style.display = "block";

    // Handle button visibility
    if (slideNumber === 1) {
      personalizeBtn.style.display = "inline-block";
      document.getElementById("random").style.display = "inline-block";
      backBtn.style.display = "none";
      nextBtn.style.display = "none";
      submitBtn.style.display = "none";
    } else if (slideNumber > 1 && slideNumber < totalSlides) {
      personalizeBtn.style.display = "none";
      document.getElementById("random").style.display = "none";
      backBtn.style.display = "inline-block";
      nextBtn.style.display = "inline-block";
      submitBtn.style.display = "none";
    } else if (slideNumber === totalSlides) {
      personalizeBtn.style.display = "none";
      document.getElementById("random").style.display = "none";
      backBtn.style.display = "inline-block";
      nextBtn.style.display = "none";
      submitBtn.style.display = "inline-block";
    }
  }

  // Button event listeners
  personalizeBtn.addEventListener("click", function () {
    currentSlide = 2;
    showSlide(currentSlide);
  });

  nextBtn.addEventListener("click", function () {
    if (currentSlide === 2) {
      const gender = document.getElementById("gender").value.trim();
      const age = document.getElementById("age").value.trim();
      const diet_type = document.getElementById("diet_type").value.trim();
      const genderError = document.getElementById("genderError");
      const ageError = document.getElementById("ageError");
      const dietTypeError = document.getElementById("dietTypeError");

      if (gender === "None") {
        genderError.textContent = "Gender is required.";
      }
      else {
        genderError.textContent = "";
      }

      if (age === "") {
        ageError.textContent = "Age is required.";
      }
      else {
        ageError.textContent = "";
      }

      if (diet_type == "None") {
        dietTypeError.textContent = "Diet Type is required.";
      }
      else {
        dietTypeError.textContent = "";
      }
      
      if (gender === "None" || age === "" || diet_type === "") {
        return;
      }
    }
    if (currentSlide < totalSlides) {
      currentSlide++;
      showSlide(currentSlide);
    }
  });

  backBtn.addEventListener("click", function () {
    if (currentSlide > 1) {
      currentSlide--;
      showSlide(currentSlide);
    }
  });

  // Initial display
  showSlide(currentSlide);
});

nextBtn.addEventListener("click", function () {
  if (currentSlide === 2) {
    const gender = document.getElementById("gender").value.trim();
    const age = document.getElementById("age").value.trim();
    const diet_type = document.getElementById("diet_type").value.trim();

    if (gender === "" || age === "" || diet_type === "") {
      alert("Please fill out all required fields.");
      return; // Stop progression to next slide
    }
  }

  if (currentSlide < totalSlides) {
    currentSlide++;
    showSlide(currentSlide);
  }
});

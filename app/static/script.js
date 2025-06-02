// JavaScript function to show the spinner when the form is submitted
function showLoading() {
    // Show the spinner
    document.getElementById('spinner-container').style.display = 'flex';
    // Optionally, hide the form so the user can't submit multiple times
    document.getElementById('user-form').style.display = 'none';
    document.getElementById('form-container').style.display = 'none';
}

/* The commented block is blocking loading screen. Might remove later.*/
/*
const goals = {{ healthGoals | tojson }}
const foodAllergies = {{ healthGoals | tojson }}
const foodIntolerancies = {{ healthGoals | tojson }}

// Function to render checkboxes for each container
function renderCheckboxes(containerId, options, filters = []) {
    const container = document.getElementById(containerId);
    container.innerHTML = ""; // Clear previous checkboxes
    let visibleCount = 0;

    options.forEach(option => {
        const matchesAllFilters = filters.every(filter => 
            option.toLowerCase().includes(filter.toLowerCase())
        );
        
        if (matchesAllFilters) {
            const label = document.createElement('label');
            label.innerHTML = `<input type="checkbox" value="${option}"> ${option}`;
            container.appendChild(label);
            container.appendChild(document.createElement('br'));
            visibleCount++;
        }
    });

    // Adjust height of the container based on number of visible checkboxes
    container.style.maxHeight = visibleCount > 0 ? '150px' : '50px';
}

// Function to gather values from active search boxes and filter checkboxes
function filterCheckboxes() {
    // Get all search boxes
    const searchInputs = document.querySelectorAll('.search-box');
    
    searchInputs.forEach(input => {
        const containerId = `checkboxContainer${input.id.charAt(input.id.length - 1)}`; // Get the container id based on search box ID
        const value = input.value.trim();
        const filters = value ? [value] : [];
        
        // Choose the correct options list based on search box ID
        const options = input.id === 'search1' ? options1 : options2;
        
        renderCheckboxes(containerId, options, filters); // Render checkboxes for the correct container
    });
}

// Attach event listeners to all search boxes
document.addEventListener("DOMContentLoaded", () => {
    const searchInputs = document.querySelectorAll('.search-box');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', filterCheckboxes);
    });

    // Initial render of checkboxes
    renderCheckboxes('searchGoals', goals);
    renderCheckboxes('searchAllergies', foodAllergies);
    renderCheckboxes('searchIntolerancies', foodIntolerancies);
});
*/
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

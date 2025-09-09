  document.addEventListener('DOMContentLoaded', function () {
    // Get all like buttons (heart emoji buttons)
    const likeButtons = document.querySelectorAll('.like-form');

    likeButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();  // Prevent the form submission from reloading the page

        const mealId = button.getAttribute('data-meal-id');  // Get the mealId from the button's data attribute

        // Send AJAX request to Flask route
        fetch('/like_meal', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            'mealId': mealId  // Send the mealId in the body of the request
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Find the div using the mealId and remove it from the page
            console.log(mealId);
            const mealDiv = document.getElementById(mealId);
            if (mealDiv) {
              mealDiv.remove();  // Remove the entire div with the mealId
              console.log(`Removed meal with ID: ${mealId}`);
            } else {
              console.log('Meal div not found');
            }
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
      });
    });
  });

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.like-meal-plan-form').forEach(form => {
      form.addEventListener('submit', function(e) {
          e.preventDefault(); // Prevent the form from submitting normally
          const mealPlanId = this.getAttribute('data-meal-plan-id');
          const heartButton = this.querySelector('.like-meal-plan-btn'); // Get the button containing the heart emoji

          fetch('/like_meal_plan', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/x-www-form-urlencoded',
              },
              body: 'mealPlanId=' + encodeURIComponent(mealPlanId)
          })
          .then(response => response.json())
          .then(data => {
              if (data.redirect) {
                  window.location.href = data.redirect;
              } else if (data.success) {
                  heartButton.textContent = data.isLiked ? '❤️' : '🤍';
              } else {
                  alert('Error: ' + (data.message || 'Something went wrong'));
              }
          })
          .catch(error => {
              console.error('Error liking meal plan:', error);
          });
      });
  });
});

  document.addEventListener('DOMContentLoaded', function() {
    // Get buttons and content sections
    const showMealsBtn = document.getElementById('show-meals-btn');
    const showMealPlansBtn = document.getElementById('show-meal-plans-btn');
    const mealsContent = document.getElementById('meals-content');
    const mealPlansContent = document.getElementById('meal-plans-content');

    // Event listener for "Meals" button
    showMealsBtn.addEventListener('click', function() {
      mealsContent.style.display = 'block';  // Show meals
      mealPlansContent.style.display = 'none';  // Hide meal plans
    });

    // Event listener for "Meal Plans" button
    showMealPlansBtn.addEventListener('click', function() {
      mealsContent.style.display = 'none';  // Hide meals
      mealPlansContent.style.display = 'block';  // Show meal plans
    });
  });


document.addEventListener('DOMContentLoaded', function () {

    const dietFilter = document.getElementById('dietFilter');
    const showMealsBtn = document.getElementById('show-meals-btn');
    const showMealPlansBtn = document.getElementById('show-meal-plans-btn');
    const mealsContent = document.getElementById('meals-content');
    const mealPlansContent = document.getElementById('meal-plans-content');

    // Function to get all diet elements from the visible section
    function getVisibleDietElements() {
      const visibleSection = mealsContent.style.display !== 'none' ? mealsContent : mealPlansContent;
      return visibleSection.querySelectorAll('[data-diet]');
    }

    // Populate diet filter options dynamically
    function populateDietFilter() {
      const elements = getVisibleDietElements();
      const dietSet = new Set();

      elements.forEach(el => {
        const diet = el.dataset.diet?.trim();
        if (diet) dietSet.add(diet);
      });

      // Clear previous options and add "All"
      dietFilter.innerHTML = '<option value="all">All</option>';
      dietSet.forEach(diet => {
        const option = document.createElement('option');
        option.value = diet;
        option.textContent = diet;
        dietFilter.appendChild(option);
      });
    }

    // Filter visible elements based on selected diet
    dietFilter.addEventListener('change', function () {
      const selectedDiet = this.value.toLowerCase();
      const elements = getVisibleDietElements();

      elements.forEach(el => {
        const diet = (el.dataset.diet || '').toLowerCase();
        el.style.display = selectedDiet === 'all' || diet === selectedDiet ? '' : 'none';
      });
    });

    // Show meals and update filter
    showMealsBtn.addEventListener('click', () => {
      mealsContent.style.display = 'block';
      mealPlansContent.style.display = 'none';
      populateDietFilter();
      dietFilter.value = 'all';
    });

    // Show meal plans and update filter
    showMealPlansBtn.addEventListener('click', () => {
      mealsContent.style.display = 'none';
      mealPlansContent.style.display = 'block';
      populateDietFilter();
      dietFilter.value = 'all';
    });

    // Initialize view: show meals by default
    mealsContent.style.display = 'block';
    mealPlansContent.style.display = 'none';
    populateDietFilter();
  });

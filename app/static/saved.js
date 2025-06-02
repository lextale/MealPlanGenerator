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


function filterData(type) {
    // Update the URL with the chosen type
    const url = new URL(window.location.href);
    url.searchParams.set('type', type);  // Set type to either 'meals' or 'mealPlans'
    
    // Reload the page with the updated filter
    window.location.href = url.toString();
}

document.addEventListener('DOMContentLoaded', function () {
    const mealPlans = document.querySelectorAll('.meal-plans-content');
    const dietSet = new Set();

    mealPlans.forEach(plan => {
      const diet = plan.dataset.diet?.trim();
      if (diet) {
        dietSet.add(diet);
      }
    });

    const dietFilter = document.getElementById('dietFilter');
    Array.from(dietSet).sort().forEach(diet => {
      const option = document.createElement('option');
      option.value = diet;
      option.textContent = diet;
      dietFilter.appendChild(option);
    });
  });

    document.getElementById('dietFilter').addEventListener('change', function () {
    const selectedDiet = this.value.toLowerCase();
    const mealPlans = document.querySelectorAll('.meal-plans-content');

    mealPlans.forEach(plan => {
      const planDiet = (plan.dataset.diet || '').toLowerCase();
      plan.style.display = (selectedDiet === 'all' || planDiet === selectedDiet) ? 'block' : 'none';
    });
  });
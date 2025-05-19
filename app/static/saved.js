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

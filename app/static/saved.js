document.querySelectorAll('.like-form').forEach(form => {
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const mealId = this.dataset.mealId;

    fetch('/like_meal', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `mealId=${encodeURIComponent(mealId)}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        if (!data.isLiked) {
          // Remove the meal card from the DOM
          const mealCard = form.closest('.meal-card');
          if (mealCard) {
            mealCard.remove();
          }
        } else {
          // Optionally toggle heart icon if still liked
          const btn = form.querySelector('.like-meal-btn');
          if (btn) btn.textContent = '❤️'; // or 🤍 if unliked
        }
      } else if (data.redirect) {
        window.location.href = data.redirect;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
});

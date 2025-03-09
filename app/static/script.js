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
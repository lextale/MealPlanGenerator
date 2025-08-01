
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Input Form</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <script src="{{ url_for('static', filename='script.js') }}"></script>

    <!-- Select2 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />

    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

    <!-- Select2 JS -->
    <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    <script>
        $(document).ready(function() {
          $('#allergies').select2({
            tags: true,
            tokenSeparators: [',', ' '],
            placeholder: 'Select or type allergies to add',
            allowClear: true,
          });
        });

        $(document).ready(function() {
            $('#intolerances').select2({
                tags: true,
                tokenSeparators: [',', ' '],
                placeholder: "Select or type intolerances to add...",
                allowClear: true,
            });
        });

        $(document).ready(function() {
            $('#goals').select2({
                placeholder: "Type to search goals...",
                allowClear: true,
                minimumResultsForSearch: 0
            });
        });

        $(document).ready(function() {
            $('#food_to_avoid').select2({
              tags: true,            // Allow tagging (custom entries)
              tokenSeparators: [',', ' '],
              data: [],              // No predefined options
              placeholder: 'Type food to avoid',
              minimumInputLength: 1  // Optional: only start when user types
            });
          });
    </script>

</head>

<nav class="navbar">
  <div class="nav-left">
    <a href="/" id="logo"><span class="logo">Meal Plan Generator</span></a>
  </div>
  <div class="nav-right">
    <a href="/" id="home">Home</a>
    {% if 'user' not in session %}
    <a href="{{ url_for('login') }}" id="login">Login</a>
    <a href="{{ url_for('signup') }}" id="signup">Sign up</a>
    {% endif %}
    {% if 'user' in session %}
    <a href="{{ url_for('profile') }}" id="profile">Profile</a>
    <a href="{{ url_for('saved') }}" id="saved">Saved</a>
    <a href="{{ url_for('logout') }}" id="logout">Log out</a>
    {% endif %}
  </div>
</nav>

<body>

    <h1>Nutrition Generator</h1>

    <!-- Περιέχει την φόρμα που με τις πληφορίες που θα τροφοδοτήσει ο χρήστης το prompt του μοντέλου -->
    <div class="form-container" id="form-container">
        <form id="user-form" action="/submit" method="POST" onsubmit="showLoading()">
            <div class="form-section-1" id="slide2">
                <div class="form-section-column">
                    <div>
                      <p style="text-align: center;"><b>Tell us a bit about yourself to get a personalized diet plan.</b></p>
                      <p style="text-align: left;">Fill in your age, gender, and choose your preferred diet type (e.g., vegetarian, keto, Mediterranean, etc.). This helps us tailor your plan to better suit your needs and goals.</p>
                    </div>
                    <!-- Φύλο (Picklist) -->
                    <label for="gender">Gender:</label>
                    <select id="gender" name="gender">
                        {% for gender in genders %}
                            <option value="{{ gender }}">{{ gender }}</option>
                        {% endfor %}
                    </select><br><br>
                    <div id="genderError" class="error-message"></div>
                </div>
                <div class="form-section-column">
                    <!-- Ηλικία (Integer) -->
                    <label for="age">Age:</label>
                    <input type="number" id="age" name="age" min="1"><br><br>
                    <div id="ageError" class="error-message"></div>
                </div>
                <div class="form-section-column">
                    <!-- Τύπος Διατροφής (Picklist) -->                    
                    <label for="diet_type">Diet Type:</label>
                    <select id="diet_type" name="diet_type">
                        {% for diet in dietaryTypes %}
                            <option value="{{ diet }}">{{ diet }}</option>
                        {% endfor %}
                    </select><br><br>
                    <div id="dietTypeError" class="error-message"></div>
                </div>
            </div>
            <div class="form-section-2" id="section2">
                <div class="form-section-column-checkboxes" id="slide1">
                    <div>
                        <h2>🥗 Welcome to Nutrition App! 🚀</h2>
                        <p>Your personal AI-powered nutrition sidekick! Whether you're bulking up, slimming down, or just want to eat smarter, we've got you covered. 💪🍏</p>
                        
                        <h3>How it works? 🤔</h3>
                        <p>📊 Click on "Personalize" button to fill the nutrition form!<br>
                        🍽️ Get personalized meal suggestions tailored to your goals!<br>
                        🔥 Or click on "Random" button to skip into exploring random food suggetions!</p>
                
                        <p>Let's take the first step towards a healthier you! 🚀💚</p>
                    </div>
                </div>
                
                <div class="form-section-column-checkboxes" id="slide3">
                  <div>
                    <p style="text-align: center;"><b>Dietary Restrictions</b></p>
                    <p style="text-align: left;">
                    Let us know about any food intolerances or allergies and food you would like us not to include in meal plan generation so we can avoid ingredients that may cause discomfort or reactions. This helps us create meals that are safe and suitable for your dietary needs.
                    </p>
                  </div>
                    <!-- Αλλεργίες (Checkboxes) -->
                    <!-- deprecated
                        <label for="allergies"><b>Food Allergies</b><br><span style="font-size: 11.5px;">(Select all that apply)</span></label><br>
                        <div class="form-checkboxes-section">
                            {% for allergy in foodAllergies %}
                                <input type="checkbox" id="allergy_{{ allergy }}" name="allergies" value="{{ allergy }}">
                                <label for="allergy_{{ allergy }}">{{ allergy }}</label><br>
                            {% endfor %}<br>
                        </div>
                    -->
                    <div class="checkboxes-content">
                        <div class="select2-container">
                          <label for="allergies"><b>Food Allergies</b><br>
                            <span style="font-size: 11.5px;">(Select all that apply or add your own)</span>
                          </label><br>

                          <select id="allergies" name="allergies" multiple="multiple" style="width: 100%;">
                            {% for allergy in foodAllergies %}
                              <option value="{{ allergy }}">{{ allergy }}</option>
                            {% endfor %}
                          </select>
                        </div>
                      </div>

                      <!-- Δυσανεξίες (Checkboxes) -->
                    <div class="checkboxes-content">
                      <div class="select2-container">
                          <label for="intolerances"><b>Food Intolerances</b><br>
                          <span style="font-size: 11.5px;">(Select all that apply)</span></label><br>

                          <select id="intolerances" name="intolerances" multiple="multiple" style="width: 100%;">
                              {% for intolerance in foodIntolerancies %}
                                  <option value="{{ intolerance }}">{{ intolerance }}</option>
                              {% endfor %}
                          </select>
                      </div>
                    </div>

                    <!-- Προσωπικές Προτιμήσεις - Φαγητά προς αποφυγή -->
                    <div class="checkboxes-content">
                      <div class="select2-container">
                        <label for="food_to_avoid"><b>Foods to Avoid</b><br>
                          <span style="font-size: 11.5px;">(Type any foods you want to exclude)</span>
                        </label><br>

                        <select id="food_to_avoid" name="food_to_avoid" multiple="multiple" style="width: 100%;"></select>

                        <small style="color: #555;">
                          Please type any foods you want to avoid due to allergies, intolerances, or personal preferences. This helps us prepare meals that suit your needs.
                        </small>
                      </div>
                    </div>

                </div>
                <!-- move slide 
                <div class="form-section-column-checkboxes" id="slide4">
                    <label for="goals"><b>Health Goals</b><br><span style="font-size: 11.5px;">(Select all that apply)</span></label><br>
                    <div class="form-checkboxes-section">
                        {% for goal in healthGoals %}
                            <input type="checkbox" id="goal_{{ goal }}" name="goals" value="{{ goal }}">
                            <label for="goal_{{ goal }}">{{ goal }}</label><br>
                        {% endfor %}<br>
                    </div>
                </div>
                -->
                <div class="form-section-column-checkboxes" id="slide4">
                    <!-- Στόχοι (Checkboxes) -->
                    <!-- deprecated
                    <div class="form-checkboxes-section">
                        {% for goal in healthGoals %}
                            <input type="checkbox" id="goal_{{ goal }}" name="goals" value="{{ goal }}">
                            <label for="goal_{{ goal }}">{{ goal }}</label><br>
                        {% endfor %}<br>
                    </div>
                    -->
                    <div>
                      <p style="text-align: center;"><b>Share your health goals to personalize your meal plan.</b></p>
                      <p style="text-align: left;">Select or type the goals that matter most to you—whether it’s improving energy, managing weight, building strength, or boosting overall wellness. This helps us create meal options aligned with your objectives.</p>
                    </div>

                    <div class="checkboxes-content">
                        <div class="select2-container">
                            <label for="goals"><b>Health Goals</b><br>
                            <span style="font-size: 11.5px;">(Select all that apply)</span></label><br>

                            <select id="goals" name="goals" multiple="multiple" style="width: 100%;">
                                {% for goal in healthGoals %}
                                    <option value="{{ goal }}">{{ goal }}</option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                    <!--
                    <label for="intolerances"><b>Food Intolerances</b><br><span style="font-size: 10px;">(Select all that apply)</span></label><br>
                    <div class="search-container">
                        <div class="form-checkboxes-section">
                            <input type="text" id="search" onkeyup="filterCheckboxes()" placeholder="Search..." class="search-box">
                            <br>

                            <div class="checkbox-list" id="checkboxContainer">
                                {% for intolerance in foodIntolerancies %}
                                    <input type="checkbox" id="intolerance_{{ intolerance }}" name="intolerances" value="{{ intolerance }}">
                                    <label for="intolerance_{{ intolerance }}">{{ intolerance }}</label><br>
                                {% endfor %}<br>
                            </div>
                        </div>
                    </div>
                    -->
                </div>
            </div>
            <!-- Submit Button -->
            <div id="button-div">
              <input type="submit" value="Random" id="random">
              <input type="button" value="Personalize" id="personalize">
              <input type="button" value="Back" id="back">
              <input type="button" value="Next" id="next">
              <input type="submit" value="Submit" id="submit">
            </div>

        </form>
    </div>
    <!-- Spinner (hidden by default) -->
    <div class="spinner-container" id="spinner-container" style="display:none;">
      <div id="loading-spinner" class="loading-spinner backdrop" style="display:block;""></div>
    </div>
    
</body>
</html>

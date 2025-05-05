from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer
from huggingface_hub import login
from pyngrok import ngrok
from datetime import datetime
import os
from Constants import Constants
import json
import re
from jsonformer import Jsonformer
import time
import pyrebase
from werkzeug.utils import secure_filename
import requests
import traceback

app = Flask(__name__)
#tokenizer = None
#model = None

app.secret_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
firebase_config = {}


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

def init_auth():
    # Authorize ngrok
    ngrok_auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    
    # Run the ngrok command to set the authtoken
    os.system(f'ngrok authtoken {ngrok_auth_token}')

    # HuggingFace Authentication
    #login('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

'''
def loadLLM():
    save_path = '/content/drive/MyDrive/Πτυχιακή Backup/Saved Models/Llama-2-7b-chat-hf'
    if os.path.exists(save_path):
        # Load the model and tokenizer from local
        model = LlamaForCausalLM.from_pretrained(save_path)
        tokenizer = LlamaTokenizer.from_pretrained(save_path)
    else:
        # Load model from hugging face
        model_id = "meta-llama/Llama-2-7b-chat-hf"
        tokenizer = LlamaTokenizer.from_pretrained(model_id, use_fast=True)
        model = LlamaForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.float16,
            load_in_8bit=True
        )
    os.makedirs(save_path, exist_ok=True)
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
'''

def initialize():
    auth()
    #loadLLM()

@app.before_request
def before_request():
    app.jinja_env.cache = None
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

# Home page
@app.route("/", methods=["GET"])
def index():
     return render_template("index.html", 
                            genders=Constants.GENDERS, 
                            activityLevels=Constants.ACTIVITY_LEVELS, 
                            healthGoals=Constants.HEALTH_GOALS, 
                            dietaryTypes=Constants.DIETARY_TYPES, 
                            foodAllergies=Constants.FOOD_ALLERGIES, 
                            foodIntolerancies=Constants.FOOD_INTOLERANCHES, 
                            micronutrientFocus=Constants.MICRONUTRIENT_FOCUS,
                            cookingDifficulty=Constants.COOKING_DIFFICULTY)

# Receive user response from form submission
@app.route('/submit', methods=['POST'])
def getSubmitForm():
    try:
        # Get form data
        gender = request.form.get("gender")
        age = request.form.get("age")
        diet_type = request.form.get("diet_type")
        goals = request.form.getlist("goals")  # Get list of selected goals
        allergies = request.form.getlist("allergies")  # Get list of selected allergies
        intolerances = request.form.getlist("intolerances")  # Get list of selected intolerances
        medications = None

        # Pass form data to index2.html
        # *** NEED TO FIX ***
        '''
        if not name:
            return jsonify({"error": "No message provided."}), 400
        if not gender:
            return jsonify({"error": "No message provided."}), 400
        '''
        json_schema = {
            "title": "MealPlan",
            "type": "object",
            "properties": {
                "breakfast": {
                    "type": "object",
                    "properties": {
                        "mealName": {"type": "string"},
                        "ingredients": {"type": "array", "items": {"type": "string"}},
                        "instructions": {"type": "string",
                                         "maxLength": 300
                                         },
                        "cookingTime": {"type": "number"},
                        "calories": {"type": "number"},
                        "macros": {
                            "type": "object",
                            "properties": {
                                "protein": {"type": "number"},
                                "carbs": {"type": "number"},
                                "fat": {"type": "number"},
                            },
                        },
                    },
                },
                "lunch": {
                    "type": "object",
                    "properties": {
                        "mealName": {"type": "string"},
                        "ingredients": {"type": "array", "items": {"type": "string"}},
                        "instructions": {"type": "string",
                                         "maxLength": 300
                                         },
                        "cookingTime": {"type": "number"},
                        "calories": {"type": "number"},
                        "macros": {
                            "type": "object",
                            "properties": {
                                "protein": {"type": "number"},
                                "carbs": {"type": "number"},
                                "fat": {"type": "number"},
                            },
                        },
                    },
                },
                "dinner": {
                    "type": "object",
                    "properties": {
                        "mealName": {"type": "string"},
                        "ingredients": {"type": "array", "items": {"type": "string"}},
                        "instructions": {"type": "string",
                                         "maxLength": 300
                                         },
                        "cookingTime": {"type": "number"},
                        "calories": {"type": "number"},
                        "macros": {
                            "type": "object",
                            "properties": {
                                "protein": {"type": "number"},
                                "carbs": {"type": "number"},
                                "fat": {"type": "number"},
                            },
                        },
                    },
                },
            },
        }

        prompt = f"""
            You are a meal planner that provides to users a day meal plan in the form of json.
            The user's gender is {gender} and is {age} years old.
            The user follows {'a '+diet_type if diet_type else 'any'} diet and has the following goals: {goals if goals else 'None'}.
            The user is allergic to {allergies if allergies else 'nothing'}.
            The user is food intolerant to {intolerances if intolerances else 'nothing'}.
            {'The user is taking the following medication: '+medications+'.' if medications else any}

            Please generate a JSON object following this structure:
            - "breakfast": Contains details of the breakfast meal.
              - "mealName": A descriptive name of the meal.
              - "ingredients": A list of ingredients required.
              - "instructions": Step-by-step instructions for preparation using minimum 150 characters
              - "cookingTime": Time required to prepare the meal in minutes.
              - "calories": Total calorie count for the meal.
              - "macros": A breakdown of macronutrients.
                - "protein": Amount of protein in grams.
                - "carbs": Amount of carbohydrates in grams.
                - "fat": Amount of fat in grams.

            - "lunch": Similar structure to breakfast.
            - "dinner": Similar structure to breakfast.

            The meal names should be realistic, ingredients should be commonly available, and macros should be reasonable. Ensure the JSON output follows the expected structure exactly without extra text."""

        # START TEST (to be deleted)
        print(f'Response generation starts at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        # Replaced to set strict json response format
        '''
        # Tokenize input and generate response
        input_ids = tokenizer(prompt, return_tensors="pt").to("cuda") #.input_ids.to(model.device)
        output_ids = model.generate(
            input_ids.input_ids,
            max_length=1024,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)[len(prompt):]
        '''

        # Generate response
        #jsonformer = Jsonformer(model, tokenizer, json_schema, prompt)
        #response = jsonformer()
        response = {
            "breakfast": {
                "mealName": "Oatmeal with Banana and Almonds",
                "ingredients": [
                    "1/2 cup rolled oats",
                    "1 cup almond milk",
                    "1 banana, sliced",
                    "1 tbsp almonds, chopped",
                    "1 tsp honey",
                    "1/2 tsp cinnamon"
                ],
                "instructions": "Cook oats in almond milk over medium heat for 5 minutes, stirring occasionally. Add banana, almonds, honey, and cinnamon before serving.",
                "cookingTime": 10,
                "calories": 320.0,
                "macros": {
                    "protein": 8,
                    "carbs": 55,
                    "fat": 7
                }
            },
            "lunch": {
                "mealName": "Grilled Chicken Salad",
                "ingredients": [
                    "1 grilled chicken breast",
                    "2 cups mixed greens",
                    "1/4 cup cherry tomatoes, halved",
                    "1/4 cucumber, sliced",
                    "1 tbsp olive oil",
                    "1 tbsp balsamic vinegar",
                    "Salt and pepper to taste"
                ],
                "instructions": "Slice grilled chicken and toss with mixed greens, tomatoes, and cucumber. Drizzle with olive oil and balsamic vinegar. Season with salt and pepper.",
                "cookingTime": 15,
                "calories": 350,
                "macros": {
                    "protein": 40,
                    "carbs": 12,
                    "fat": 18
                }
            },
            "dinner": {
                "mealName": "Salmon with Quinoa and Steamed Vegetables",
                "ingredients": [
                    "1 salmon fillet",
                    "1/2 cup quinoa",
                    "1 cup broccoli, steamed",
                    "1/2 cup carrots, steamed",
                    "1 tbsp olive oil",
                    "1 tsp lemon juice",
                    "Salt and pepper to taste"
                ],
                "instructions": "Cook quinoa according to package instructions. Season salmon with salt, pepper, and lemon juice, then grill for 6-8 minutes per side. Serve with steamed vegetables.",
                "cookingTime": 25.0,
                "calories": 450.643,
                "macros": {
                    "protein": 42.345632,
                    "carbs": 35.0,
                    "fat": 20.66
                }
            }
        }


        # END TEST (to be deleted)
        print(f'Response generation ended at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        print(response)

        
        submissionForm = {"gender": gender,
                          "age": age,
                          "diet_type": diet_type,
                          "goals": goals,
                          "allergies": allergies,
                          "intolerances": intolerances}

        print('session => '+str(session))
        if 'user' in session:
          mealPlanId, response = storeGeneratedMealPlan(session['user']['uid'], response, submissionForm)

          print(mealPlanId)
          print(response)

        #time.sleep(30)
        if 'user' in session:
          return render_template("results.html", results=response, mealPlanId=mealPlanId)
        else:
          return render_template("results.html", results=response) #return render_template("results.html", response=jsonify({"response": response}))

    except Exception as e:
        print(e)
        print(str(response))
        traceback.print_exc()
        return render_template("error.html", error={"error": str(e)}) #return render_template("results.html", response=jsonify({"response": response}))
        #return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email, password)

            # Check if email is verified
            user_info = auth.get_account_info(user['idToken'])
            email_verified = user_info['users'][0]['emailVerified']

            if not email_verified:
                flash("Please verify your email before logging in.", "warning")
                return redirect(url_for('login'))

            session['user'] = {
                "email": email,
                "uid": user['localId'],
                "username": db.child("users").child(user['localId']).child("username").get(user['idToken']).val()
            }
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))

        except Exception as e:
            error_msg = str(e)
            if "INVALID_LOGIN_CREDENTIALS" in str(e):
                flash("Wrong email or password!", "danger")
                return render_template('login.html', email=email)
            
            flash(error_msg, "danger")
            return render_template('login.html', email=email)


    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        try:
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])

            # Save additional info to the database
            data = {
                "username": username,
                "email": email
            }
            uid = user['localId']
            db.child("users").child(uid).set(data)

            flash("Account created! Check your email to verify.", "success")
            return redirect(url_for('login'))

        except Exception as e:
          if "WEAK_PASSWORD" in str(e):
              flash("Password must be at least 6 characters.", "danger")
              return render_template('signup.html', username=username, email=email)
          
          flash(str(e), "danger")

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.clear()
    flash("You’ve been logged out", "info")
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('login'))

    user = session['user']
    return render_template("profile.html", user=user)

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user' not in session:
        flash("Please log in to change your password.", "danger")
        return redirect(url_for('login'))

    email = session['user']['email']
    current_password = request.form['current_password']
    new_password = request.form['new_password']

    try:
        # Re-authenticate to get a fresh token
        user = auth.sign_in_with_email_and_password(email, current_password)

        # Update password
        #auth.update_user_password(user['idToken'], new_password)
        auth.send_password_reset_email(email)
        #flash("Password updated successfully!", "success")
        flash("Check your email!", "success")
    except Exception as e:
        error_msg = str(e)
        print(error_msg)
        flash(f"Password change failed: {error_msg}", "danger")
    
    return redirect(url_for('profile'))

@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'user' not in session:
        flash("Please log in to upload an avatar.", "warning")
        return redirect(url_for('login'))

    avatar = request.files.get('avatar')
    if avatar:
        uid = session['user']['uid']
        filename = secure_filename(avatar.filename)
        filepath = os.path.join('/content/thesisRepo/app/static/uploads/', uid+'.'+filename.split('.')[1])
        avatar.save(filepath)

        # Save the avatar path to user's data
        db.child("users").child(uid).update({"avatar_url": f"{filepath}"})
        
        # Optional: update session data too
        session['user']['avatar_url'] = f"{filepath}"

        flash("Avatar uploaded successfully!", "success")

    return redirect(url_for('profile'))

def storeGeneratedMealPlan(userId, response, submissionForm):
    # Εκτελείται μόνο για συνδεδεμένους χρήστες

    timestamp_created = int(time.time())

    # Αποθήκευση ημερήσιου πλάνου στη Βάση Δεδομένων
    generatedMealPlan = db.child("mealPlans").push(
      {
          "user": userId,
          "timestamptCreated": timestamp_created, 
          "timestamptLiked": "", 
          "timestamptUnliked": "", 
          "isLiked": False, 
          "submissionFormId": submissionForm 
      }
    )
    mealPlanId = generatedMealPlan['name']
    mealIds = []
    # Αποθήκευση γεύματος στη Βάση Δεδομένων
    for mealType, mealInfo in response.items():
      generatedMeal = db.child("meals").push(
        {
          "user": userId,
          "mealPlanId": mealPlanId,
          "timestamptCreated": timestamp_created, 
          "timestamptLiked": "", 
          "timestamptUnliked": "", 
          "isLiked": False, 
          "mealType": mealType, 
          "mealName": mealInfo['mealName'], 
          "ingredients": mealInfo['ingredients'], 
          "preparation": mealInfo['instructions'], 
          "cookingTime": mealInfo['cookingTime'], 
          "calories": mealInfo['calories'], 
          "macros": mealInfo['macros']
        }
      )
      mealIds.append(generatedMeal['name'])

      for mealType, mealId in zip(response, mealIds):
        response[mealType]['mealId'] = mealId;

    return mealPlanId, response

@app.route('/like_meal_plan', methods=['POST'])
def like_meal_plan():
    if 'user' not in session:
        flash("Please log in to like meal plans.", "error")
        return jsonify({"success": False, "redirect": url_for('login'), "message": "Please log in."})

    userId = session['user']['uid']
    mealPlanId = request.form['mealPlanId']

    current_like = db.child("mealPlans").child(mealPlanId).child("isLiked").get().val()

    if current_like:
        # If already liked, toggle to unlike
        db.child("mealPlans").child(mealPlanId).child("isLiked").set(False)
    else:
        # If not liked, toggle to like
        db.child("mealPlans").child(mealPlanId).child("isLiked").set(True)

    flash("Meal saved!", "success")

    current_like = db.child("mealPlans").child(mealPlanId).child("isLiked").get().val()

    return jsonify({"success": True, "isLiked": current_like, "message": "Meal saved!"})


@app.route('/like_meal', methods=['POST'])
def like_meal():
    if 'user' not in session:
        flash("Please log in to like meals.", "error")
        return jsonify({"success": False, "redirect": url_for('login'), "message": "Please log in."})

    userId = session['user']['uid']
    mealId = request.form['mealId']

    current_like = db.child("meals").child(mealId).child("isLiked").get().val()

    if current_like:
        # If already liked, toggle to unlike
        db.child("meals").child(mealId).child("isLiked").set(False)
    else:
        # If not liked, toggle to like
        db.child("meals").child(mealId).child("isLiked").set(True)

    flash("Meal saved!", "success")

    current_like = db.child("meals").child(mealId).child("isLiked").get().val()

    return jsonify({"success": True, "isLiked": current_like, "message": "Meal saved!"})

@app.route('/saved', methods=['GET'])
def saved():
    if 'user' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('login'))

    user = session['user']
    savedMeals = db.child("meals").order_by_child("user").equal_to(user['uid']).get().val()
    savedMealPlans = db.child("mealPlans").order_by_child("user").equal_to(user['uid']).get().val()

    print(savedMeals)

    return render_template("saved.html", user=user, savedMeals=savedMeals, savedMealPlans=savedMealPlans)

if __name__ == '__main__':
    init_auth()
    #loadLLM()
    '''
    save_path = '/content/drive/MyDrive/Πτυχιακή Backup/Saved Models/Llama-2-7b-chat-hf'
    if os.path.exists(save_path):
        # Load the model and tokenizer from local
        model = LlamaForCausalLM.from_pretrained(save_path)
        tokenizer = LlamaTokenizer.from_pretrained(save_path)
    else:
        # Load model from hugging face
        model_id = "meta-llama/Llama-2-7b-chat-hf"
        tokenizer = LlamaTokenizer.from_pretrained(model_id, use_fast=True)
        model = LlamaForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.float16,
            load_in_8bit=True
        )
    os.makedirs(save_path, exist_ok=True)
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
    if tokenizer.pad_token is None:
      tokenizer.pad_token = tokenizer.eos_token
    '''

    # Open a ngrok tunnel to the localhost port 5000
    public_url = ngrok.connect(5000).public_url
    print(f"Public URL: {public_url}")

    # Run the Flask app
    app.run()

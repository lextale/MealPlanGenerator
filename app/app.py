#####################################################################
# @description       : Πτυχιακή Εργασία   
# @author            : Αλεξάνδρα Παραμύθα                      
# @last modified on  : 11-03-2025
# * Modifications Log 
# * Ver   Date         Author                  Modification
# * 3.0   09-06-2025   Αλεξάνδρα Παραμύθα    Final Version
####################################################################

# Εισαγωγή απαραίτητων βιβλιοθηκών
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from transformers import LlamaForCausalLM, LlamaTokenizer, pipeline
from huggingface_hub import login as hf_login
from pyngrok import ngrok
#from datetime import datetime
import os
from Constants import Constants
from Basemodels import MealPlanFormat, MealBreakfast, MealLunch, MealDinner, Meal
import json
#import re
import time
import pyrebase
from werkzeug.utils import secure_filename
#import requests
import traceback
import json
import sys
#from pydantic import BaseModel
from lmformatenforcer import JsonSchemaParser
from lmformatenforcer.integrations.transformers import build_transformers_prefix_allowed_tokens_fn
#from auto_gptq import AutoGPTQForCausalLM

app = Flask(__name__)  # Αρχικοποίηση Flask εφαρμογής για τη διαχείριση HTTP requests  

def argsHandle():
    args = sys.argv[1:]  # Παράλειψε το όνομα του python αρχείου
    args_len = len(args)
    
    argsDict = {
        '--ngroktoken': '',
        '--firebasetoken': '',
        '--firebaseconfig': '',
        '--hftoken': ''
    }
    expectedArgs = list(argsDict.keys())
    expectedArgs.append('--modelpath')

    for i in range(0, args_len-1, 2):
        if args[i].startswith("--"):
            key = args[i]
            value = args[i + 1]
            if key not in expectedArgs:
                raise Exception(f'Unexpected Argument: {key}')
            if ((value == '' or value == None) and key != '--modelpath'):
                raise Exception(f'Argument cannot be empty for {key}')
            argsDict[key] = value
    
    #if argsDict['--modelpath'] == '' or argsDict['--modelpath'] == None:
    #  argsDict['--modelpath'] = '/'
        
    missingArgs = []
    for key, value in argsDict.items():
        if ((value == '' or value == None) and key != '--modelpath'):
            missingArgs.append(key)
    if len(missingArgs) > 0:
        raise Exception(f"Missing arguements: {', '.join(missingArgs)}")
    
    return argsDict

args = argsHandle()

# Στοιχεία αυθεντικοποίησης για το Firebase
app.secret_key = args['--firebasetoken']
file = open(args['--firebaseconfig'], 'r')
firebase_config = json.load(file)
file.close()

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

def init_auth():
    # authtoken ngrok
    ngrok_auth_token = args['--ngroktoken']
    
    # Θέτουμε το authtoken για ngrok
    os.system(f'ngrok authtoken {ngrok_auth_token}')

    # Σύνδεση με HuggingFace
    hf_login(args['--hftoken'])

def storeMealPlanMetrics(generation_start_time, generation_end_time, response, submissionForm):
    UserId = ''
    if 'user' in session:
        userId = session['user']['uid']

    metrics = {
            "generation_start_time": generation_start_time,
            "generation_end_time": generation_end_time,
            "generation_time_ms": generation_end_time - generation_start_time,
            "UserId": UserId, 
            "ingredientsSet": [],
            "excludedFood": [], 
            "excludedFoodInIngredients": [],
            "hasExcludedFoodInIngredients": ''
        }

    for dayMeal, contents in response.items():
        ingredients = list(set(contents['ingredients']))
        metrics['ingredientsSet'].extend(ingredients)
        excludedFood = list(set(submissionForm['food_to_avoid']))
        metrics['excludedFood'].extend(excludedFood)
        metrics['excludedFoodInIngredients'] = [food for food in ingredients if food in excludedFood]
        if len(metrics['excludedFoodInIngredients']) > 0:
            metrics['hasExcludedFoodInIngredients'] = True
        else:
            metrics['hasExcludedFoodInIngredients'] = False

    if metrics['ingredientsSet'] == []:
        metrics['ingredientsSet'] = ''

    if metrics['excludedFood'] == []:
        metrics['excludedFood'] = ''

    if metrics['excludedFoodInIngredients'] == []:
        metrics['excludedFoodInIngredients'] = ''

    if metrics['hasExcludedFoodInIngredients'] == []:
        metrics['hasExcludedFoodInIngredients'] = ''

    db.child("metrics").push(metrics)

def debugLogMetrics(timestamp, error):
    userId = ''
    if 'user' in session:
        userId = session['user']['uid']

    db.child("debugLog").push(
        {
            'timestamp': timestamp,
            'error': {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            },
            'user': userId
        }
    )

# Εκτελείται πριν από κάθε αίτημα για να διασφαλίσει ότι τα templates φορτώνονται ξανά αυτόματα
# σε περίπτωση που θέλουμε να τροποιήσουμε αρχεία όπως html, css κτλ. χωρίς να 
# εκτελέσουμε ξανά την εφαρμογή
@app.before_request
@app.before_request
def before_request():
    app.jinja_env.cache = None # Απενεργοποίηση της cache των templates
    app.jinja_env.auto_reload = True # Ενεργοποίηση αυτόματης ανανέωσης των template
    app.config['TEMPLATES_AUTO_RELOAD'] = True # Επιτρέπει την αυτόματη επαναφόρτωση των templates χωρίς restart

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


# Φόρτωση Αρχικής Σελίδας (index.html)
# Η σελίδα φορτώνεται με τη βοήθεια της βιβλιοθήκης Flask
# Οι σταθερές περνούν δυναμικά στην index.html
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

# Η getSubmitForm() εκτελείται όταν ο χρήστης υποβάλει τη φόρμα
@app.route('/submit', methods=['POST'])
def getSubmitForm():
    try:
        # Λήψη δεδομένων που εισήγαγε ο χρήστης
        gender = request.form.get("gender")
        age = request.form.get("age")
        diet_type = request.form.get("diet_type")
        goals = request.form.getlist("goals")
        allergies = request.form.getlist("allergies")
        intolerances = request.form.getlist("intolerances")
        food_to_avoid = request.form.getlist("food_to_avoid")

        # Εμφάνιση Δεδομένων χρήστη - Επαλήθευση ορθής λήψης δεδομένων
        print('Data retrived from user\n');
        print('Gender: '+gender);
        print('diet_type: '+diet_type);
        print('goals: '+str(goals));
        print('allergies: '+str(allergies));
        print('intolerances: '+str(intolerances));
        print('food_to_avoid: '+str(food_to_avoid));
        

        # Προσχέδιο προτροπής
        mealtype = ""

        prompt = f"""You are a meal planner that provides to users a {mealtype} meal in the form of json.\
            The user\'s gender is {gender} and is {age} years old.\
            The user follows {'a '+diet_type if diet_type else 'any'} diet and has the following goals: {goals if goals else 'None'}.\
            The user is allergic to {allergies if allergies else 'nothing'}.\
            The user is food intolerant to {intolerances if intolerances else 'nothing'}.\
            {"You must not include any of the following ingredients: " + ", ".join(food_to_avoid) + "." if food_to_avoid else ""}\

            The meal names should be realistic and descriptive, ingredients should be commonly available, cookingTime must correspond to the time needed \
            for cooking the meal  and macros should be reasonable. Ensure the JSON output follows the expected structure exactly without extra text \
            and that you provide a mealName like a meal title, the cooking time needed to prepare instructions, the meal calories and macros and \
            all the ingredients mentioned in instructions. Please do not leave any part of the json empty. The output will be \
            directly use to feed a flask json.
            You must put the information in the following json schema: {Meal.schema_json()}\n"""

        # Create a character level parser and build a transformers prefix function from it
        parser = JsonSchemaParser(Meal.schema())
        prefix_function = build_transformers_prefix_allowed_tokens_fn(hf_pipeline.tokenizer, parser)
        
        generation_start_time = int(time.time())
        # Call the pipeline with the prefix function
        count = 0
        while(count<3):
          try:
            breakfast = json.loads(hf_pipeline(prompt, prefix_allowed_tokens_fn=prefix_function)[0]['generated_text'][len(prompt):].replace("\n",""))
            break
          except:
            count += 1

        count = 0
        while(count<3):
          try:
            lunch = json.loads(hf_pipeline(prompt, prefix_allowed_tokens_fn=prefix_function)[0]['generated_text'][len(prompt):].replace("\n",""))
            break
          except:
            count += 1

        count = 0
        while(count<3):
          try:
            dinner = json.loads(hf_pipeline(prompt, prefix_allowed_tokens_fn=prefix_function)[0]['generated_text'][len(prompt):].replace("\n",""))
            break
          except:
            count += 1

        generation_end_time = int(time.time())


        # Extract the results
        print(breakfast)
        print(lunch)
        print(dinner)

        response = {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner
        }



        # Εμφάνιση παραγόμενου αποτελέσματος
        print(response)

        # Δεδομένα φόρμας υποβολής
        submissionForm = {"gender": gender if gender is not None else '',
                        "age": age if age is not None else '',
                        "diet_type": diet_type if diet_type is not None else '',
                        "goals": goals if len(goals) else '',
                        "allergies": allergies if len(allergies) else '',
                        "intolerances": intolerances if len(intolerances) else '',
                        "food_to_avoid": food_to_avoid if len(food_to_avoid) else ''}
        
        print(submissionForm)
        # Αποθήκευση παραγόμενων γευμάτων σε περίπτωση συνδεδεμένου χρήστη
        if 'user' in session:
            mealPlanId, response = storeGeneratedMealPlan(session['user']['uid'], response, submissionForm)
        else:
            mealPlanId, response = storeGeneratedMealPlan('', response, submissionForm)
        
        storeMealPlanMetrics(generation_start_time, generation_end_time, response, submissionForm)


        print(response)

        if 'user' in session:
          return render_template("results.html", results=response, mealPlanId=mealPlanId)
        else:
          return render_template("results.html", results=response) #return render_template("results.html", response=jsonify({"response": response}))

    except Exception as e:
        print(e)
        print(str(response))
        traceback.print_exc()
        debugLogMetrics(time.time(), e)
        return render_template("error.html", error={"error": str(e)})


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
            debugLogMetrics(time.time(), e)
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
            db.child("users").child(uid).set(data, user['idToken'])

            flash("Account created! Check your email to verify.", "success")
            return redirect(url_for('login'))

        except Exception as e:
          if "WEAK_PASSWORD" in str(e):
              flash("Password must be at least 6 characters.", "danger")
              return render_template('signup.html', username=username, email=email)
          else:
              error_msg = str(e)
              debugLogMetrics(time.time(), e)
          print(e)
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
        debugLogMetrics(time.time(), e)
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
          "user": '',
          "timestampCreated": timestamp_created, 
          "timestampLiked": "", 
          "timestampUnliked": "", 
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
          "user": '',
          "mealPlanId": mealPlanId,
          "timestampCreated": timestamp_created, 
          "timestampLiked": "", 
          "timestampUnliked": "", 
          "isLiked": False, 
          "mealType": mealType,
          "mealName": mealInfo['mealName'] if mealInfo['mealName'] is not None else '',
          "dietType": submissionForm["diet_type"],
          "ingredients": mealInfo['ingredients'] if len(mealInfo['ingredients']) else '', 
          "preparation": mealInfo['instructions'] if mealInfo['instructions'] is not None else '', 
          "cookingTime": mealInfo['cookingTime'] if mealInfo['cookingTime'] is not None else '', 
          "calories": mealInfo['calories'] if mealInfo['calories'] is not None else '', 
          "macros": {key: value if value is not None else '' for key, value in mealInfo['macros'].items()}
        }
      )
      mealIds.append(generatedMeal['name'])
      for mealType, mealId in zip(response, mealIds):
        response[mealType]['mealId'] = mealId;

    return mealPlanId, response

def areThereLikedMealsByMealPlanId(userId, mealPlanId):
    meals = db.child("meals").get().val() or {}
    liked_meals = [ mealId for mealId, meal in meals.items() if meal.get("mealPlanId") == mealPlanId and meal.get('isLiked')]

    if len(liked_meals) > 0:
        return True
    else:
        return False

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
        db.child("mealPlans").child(mealPlanId).child("timestampUnliked").set(int(time.time()))
        if not(areThereLikedMealsByMealPlanId(userId, mealPlanId)):
            db.child("mealPlans").child(mealPlanId).child("user").set("")
    else:
        # If not liked, toggle to like
        db.child("mealPlans").child(mealPlanId).child("isLiked").set(True)
        db.child("mealPlans").child(mealPlanId).child("user").set(userId)
        db.child("mealPlans").child(mealPlanId).child("timestampLiked").set(int(time.time()))

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
    mealPlanId = db.child("meals").child(mealId).child("mealPlanId").get().val()

    current_like = db.child("meals").child(mealId).child("isLiked").get().val()

    if current_like:
        # If already liked, toggle to unlike
        db.child("meals").child(mealId).child("isLiked").set(False)
        db.child("meals").child(mealId).child("user").set("")
        db.child("meals").child(mealId).child("timestampUnliked").set(int(time.time()))
        if not(areThereLikedMealsByMealPlanId(userId, mealPlanId)):
            db.child("mealPlans").child(mealPlanId).child("user").set("")
    else:
        # If not liked, toggle to like
        db.child("meals").child(mealId).child("isLiked").set(True)
        db.child("meals").child(mealId).child("user").set(userId)
        db.child("mealPlans").child(mealPlanId).child("user").set(userId)
        db.child("meals").child(mealId).child("timestampLiked").set(int(time.time()))


    flash("Meal saved!", "success")

    current_like = db.child("meals").child(mealId).child("isLiked").get().val()

    return jsonify({"success": True, "isLiked": current_like, "message": "Meal saved!"})

@app.route('/saved', methods=['GET'])
def saved():
    if 'user' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('login'))

    user = session['user']

    # Get all meals for user
    savedMeals = db.child("meals").order_by_child("user").equal_to(user['uid']).get().val() or {}
    likedMeals = {
        meal_id: meal
            for meal_id, meal in sorted(
                savedMeals.items(),
                key=lambda item: item[1].get('timestampCreated', 0),
                reverse=True
            )
            if meal.get('isLiked')
    }

    # Get all meal plans for user
    savedMealPlans = db.child("mealPlans").order_by_child("user").equal_to(user['uid']).get().val() or {}
    likedMealPlans = {
        mp_id: mp
        for mp_id, mp in sorted(
                savedMealPlans.items(),
                key=lambda item: item[1].get('timestampCreated', 0),
                reverse=True
            )
            if mp.get('isLiked')
    }

    # Build dict mapping mealPlanId -> list of meals belonging to it (filtering from savedMeals)
    mealPlanMeals = {}
    for plan_id, plan_data in likedMealPlans.items():
      meal_type_order = {'breakfast': 0, 'lunch': 1, 'dinner': 2}

      filtered_meals = {
          meal_id: meal
          for meal_id, meal in sorted(
              savedMeals.items(),
              key=lambda item: meal_type_order.get(item[1].get('mealType'), 99)
          )
          if meal.get('mealPlanId') == plan_id
      }

      mealPlanMeals[plan_id] = {
            "mealPlan": plan_data,
            "meals": filtered_meals
      }

    # Collect available diet types from meals and meal plans
    availableDietTypes = set('All')

    # Add diet types from all saved meals
    for meal in savedMeals.values():
        dietType = meal.get("dietType")
        if not dietType:
            availableDietTypes.add('Not specified')
        else:
            availableDietTypes.add(dietType)

    # Add diet types from all saved meal plans
    for mealPlan in savedMealPlans.values():
        dietType = mealPlan.get("submissionFormId").get("diet_type")
        if not dietType:
            availableDietTypes.add('Not specified')
        else:
            availableDietTypes.add(dietType)

    # Add diet types from submissionFormId inside liked meal plans (if exists and not None)
    for mealPlan in likedMealPlans.values():
        submissionForm = mealPlan.get('submissionFormId', {})
        diet_type = submissionForm.get('diet_type')
        if diet_type and diet_type != 'None':
            availableDietTypes.add(diet_type)

    # Convert set to list for template use
    availableDietTypes = list(availableDietTypes)

    print(savedMeals)  # Debug print

    return render_template(
        "saved.html",
        user=user,
        savedMeals=likedMeals,
        savedMealPlans=likedMealPlans,
        availableDietTypes=availableDietTypes,
        mealPlanMeals=mealPlanMeals
    )

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
      return render_template('forgot_password.html')
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash("Email is required", "error")
            return render_template('login.html', email=email)

        try:
            # reset_link = auth.generate_password_reset_link(email)
            #print(f"Send this reset link to the user: {reset_link}")
            auth.send_password_reset_email(email)

            flash("Password reset email sent! Check your inbox.", "success")
            return redirect(url_for('forgot_password'))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            debugLogMetrics(time.time(), e)
            return render_template('login.html', email=email)

    # GET request
    return render_template('login.html')

if __name__ == '__main__':
    init_auth() # Αυθεντικοποίηση για την χρήση Ngrok και HuggingFace
    
    isModelPathSet = '--modelpath' in args.keys()
    if isModelPathSet:
      save_path = args['--modelpath']

      # Όταν η διαδρομή είναι κενή επέλεξε την τρέχουσα τοποθεσία
      if save_path == '' or save_path == None:
        save_path = '.'


    load_failed = False

    # Αν έχει καθοριστεί path προσπάθησε να φορτώσεις το μοντέλο από εκεί
    if isModelPathSet:
        if os.path.exists(save_path):   # Αν υπάρχει αυτό το path
            try:
                model = LlamaForCausalLM.from_pretrained(
                    save_path,
                    device_map="auto",
                    torch_dtype="auto"
                )
                tokenizer = LlamaTokenizer.from_pretrained(save_path)
            except OSError as e: # Αν δεν υπάρχει το μοντέλο σε αυτόν τον φάκελο σημείωσε αποτυχία φόρτωσης
                print(e)
                print('Model and tokenizer will be downloaded in /Llama-2-7b-chat-hf')
                load_failed = True
        else: # Αν δεν υπάρχει το path σημείωσε αποτυχία φόρτωσης
          print(f'Path {save_path} does not exist!')
          print('Model and tokenizer will be downloaded in /Llama-2-7b-chat-hf')
          load_failed = True

    if load_failed == True or isModelPathSet==False:   # Αν δεν εχουμε ορίσει path ή η φόρτωση από το path απέτυχε κατέβασε το μοντέλο
        print(f'isModelPathSet: {isModelPathSet}')
        print(f'load_failed: {load_failed}')
        model_id = "meta-llama/Llama-2-7b-chat-hf"
        tokenizer = LlamaTokenizer.from_pretrained(model_id, use_fast=True)
        model = LlamaForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype="auto"
        )
        save_path = '/Llama-2-7b-chat-hf'
        os.makedirs(save_path, exist_ok=True)
        model.save_pretrained(save_path)
        tokenizer.save_pretrained(save_path)

    # Set pad token if not already set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Create the pipeline
    hf_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device_map="auto",
        pad_token_id=tokenizer.pad_token_id  # avoids warning about missing pad_token
    )

    # Συνδέουμε το ngrok στην τοπική θύρα 5000 και παίρνουμε το δημόσιο URL όπου θα είναι προσβάσιμη η εφαρμογή
    public_url = ngrok.connect(5000).public_url
    print(f"Public URL: {public_url}")

    # Εκκίνηση της Flask εφαρμογής
    app.run()

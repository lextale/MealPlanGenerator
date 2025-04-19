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
        
        #time.sleep(30)
        
        return render_template("results.html", results=response) #return render_template("results.html", response=jsonify({"response": response}))

    except Exception as e:
        print(e)
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
                "username": db.child("users").child(user['localId']).child("username").get().val()
            }
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))

        except Exception as e:
            error_msg = str(e).split(']')[-1].strip()
            flash(error_msg, "danger")

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
            flash(str(e), "danger")

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.clear()
    flash("You’ve been logged out", "info")
    return redirect(url_for('login'))

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

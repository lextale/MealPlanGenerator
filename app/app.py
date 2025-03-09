from flask import Flask, request, jsonify, render_template
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


app = Flask(__name__)

def auth():
    # Authorize ngrok
    ngrok_auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    
    # Run the ngrok command to set the authtoken
    os.system(f'ngrok authtoken {ngrok_auth_token}')

    # HuggingFace Authentication
    login('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')


@app.before_request
def before_request():
    app.jinja_env.cache = None
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

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

        # User Input
        print('Data retrived from user\n');
        print('Gender: '+gender);
        print('diet_type: '+diet_type);
        print('goals: '+str(goals));
        print('intolerances: '+str(intolerances));
        print('intolerances: '+str(intolerances));

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
                                         "minLength": 200,
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
                                         "minLength": 200,
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
                                         "minLength": 200,
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

            The meal names should be realistic, ingredients should be commonly available, cookingTime must correspond to the time needed for cooking the meal  and macros should be reasonable. Ensure the JSON output follows the expected structure exactly without extra text."""

        # Print Prompt
        print('Prompt used: '+prompt);

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
        jsonformer = Jsonformer(model, tokenizer, json_schema, prompt, max_string_token_length=3000)
        response = jsonformer()

        # END TEST (to be deleted)
        print(f'Response generation ended at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        print(response)
        
        return render_template("results.html", results=response) #return render_template("results.html", response=jsonify({"response": response}))

    except Exception as e:
        print(e)
        return render_template("error.html", error={"error": str(e)}) #return render_template("results.html", response=jsonify({"response": response}))
        #return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    auth()
    
    save_path = '/content/Saved Models/Llama-2-7b-chat-hf'
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
    

    # Open a ngrok tunnel to the localhost port 5000
    public_url = ngrok.connect(5000).public_url
    print(f"Public URL: {public_url}")

    # Run the Flask app
    app.run()

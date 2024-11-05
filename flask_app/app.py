from flask import Flask, request, jsonify, render_template
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer
from huggingface_hub import login
from pyngrok import ngrok
from datetime import datetime
import os

app = Flask(__name__)

ngrok_auth_token = 'AUTHTOKEN'

# Run the ngrok command to set the authtoken
os.system(f'ngrok authtoken {ngrok_auth_token}')

# HuggingFace Authentication
login(token="HUGGINGFACETOKEN")

# Load the model and tokenizer
model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message') # User's input from post request
        if not user_message:
            return jsonify({"error": "No message provided."}), 400

        # TEST (to be deleted)
        print(f'Response generation starts at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        # Tokenize input and generate response
        inputs = tokenizer(user_message, return_tensors="pt").to("cuda")
        outputs = model.generate(inputs.input_ids, max_length=512, do_sample=True, temperature=0.9)
        bot_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        bot_response = bot_response[len(user_message):]  # Trim the input message from the response

        # TEST (to be deleted)
        print(f'Response generation ended at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        return jsonify({"response": bot_response})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Open a ngrok tunnel to the localhost port 5000
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")

    # Run the Flask app
    app.run()

import os
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure the API key is set
if not openai.api_key:
    raise EnvironmentError("Missing OpenAI API key in environment variables")

app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/troubleshoot', methods=['POST'])
def troubleshoot():
    user_input = request.json.get('issue')
    if not user_input:
        return jsonify({"error": "No issue provided"}), 400
    try:
        # Using gpt-3.5-turbo with the older OpenAI library
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert CUCM troubleshooter."},
                {"role": "user", "content": f"Troubleshoot this CUCM issue: {user_input}"}
            ],
            max_tokens=150
        )
        solution = response['choices'][0]['message']['content'].strip()
        return jsonify({"solution": solution})
    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors gracefully
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

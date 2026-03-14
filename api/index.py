from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

# Groq inicializálás
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": str(e)}), 500

@app.route('/login_api', methods=['POST'])
def login():
    return jsonify({"message": "Login Success"}), 200

@app.route('/register_api', methods=['POST'])
def register():
    return jsonify({"message": "Register Success"}), 200

# Ez a sor KELL a Vercelnek
app = app

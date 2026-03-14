from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

# Groq kliens inicializálása - HIBAVÉDELEMMEL
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception:
    client = None

@app.route('/ask', methods=['POST'])
def ask():
    if not client:
        return jsonify({"answer": "SYSTEM ERROR: API KEY NOT FOUND IN VERCEL SETTINGS"}), 500
    
    try:
        data = request.json
        prompt = data.get('prompt', 'Hello')
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are StudingWell AI, a professional tutor."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": f"AI ERROR: {str(e)}"}), 500

# Ez a sor KELL a Vercel-nek
app = app

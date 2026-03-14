import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Groq kliens inicializálása
# Fontos: A GROQ_API_KEY-t a Vercel Settings-ben add meg!
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are StudingWell AI, a professional math tutor."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": f"System Error: {str(e)}"}), 500

# Vercel-nél ez a sor kötelező a végére, hogy a Flask tudja, mit exportáljon:
# De NE használd az app.run()-t!

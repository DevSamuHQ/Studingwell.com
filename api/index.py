import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# --- BIZTONSÁGI JAVÍTÁS ---
# Megpróbáljuk betölteni a kulcsot, de nem hagyjuk, hogy összeomoljon a szerver
api_key = os.environ.get("GROQ_API_KEY")

try:
    if api_key:
        client = Groq(api_key=api_key)
    else:
        client = None
except Exception:
    client = None

@app.route('/ask', methods=['POST'])
def ask():
    if not client:
        return jsonify({"answer": "HIBA: A GROQ_API_KEY hiányzik vagy érvénytelen a Vercel beállításokban!"}), 500
    
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": f"AI hiba: {str(e)}"}), 500

@app.route('/login_api', methods=['POST'])
def login():
    # Ideiglenes fix belépés a teszteléshez
    return jsonify({"status": "success", "message": "Authorized"}), 200

@app.route('/register_api', methods=['POST'])
def register():
    return jsonify({"status": "success", "message": "Registered"}), 200

# Ez a sor ÉLETVESZÉLYESEN FONTOS a Vercelnek:
app = app

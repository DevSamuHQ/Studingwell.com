import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Groq kliens – ha nincs kulcs, ne omoljon össze
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception:
    client = None

@app.route('/ask', methods=['POST'])
def ask():
    if not client:
        return jsonify({"answer": "Hiba: GROQ_API_KEY hiányzik a Vercel beállításoknál!"}), 500
    try:
        data = request.json
        prompt = data.get('prompt', '')
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": f"AI Error: {str(e)}"}), 500

# Ez az útvonal csak tesztelésre van
@app.route('/test')
def test():
    return "API OK"

app = app

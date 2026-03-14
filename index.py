from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

# Csak akkor indítjuk el a Groq-ot, ha van kulcs, így nem omlik össze az importálásnál
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except:
    client = None

@app.route('/ask', methods=['POST'])
def ask():
    if not client:
        return jsonify({"answer": "API Key missing"}), 500
    try:
        data = request.json
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": data.get('prompt')}]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": str(e)}), 500

# Vercelnek ez kell a végére:
def handler(request):
    return app(request)

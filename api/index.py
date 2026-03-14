import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from groq import Groq

app = Flask(__name__)
CORS(app)

# Vercel-en csak a /tmp mappa írható
DB_PATH = '/tmp/users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)')
    conn.commit()
    conn.close()

init_db()

# Groq AI kliens inicializálása
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

@app.route('/')
def home():
    return "StudingWell API is running!"

@app.route('/ask', methods=['POST'])
def ask():
    if not client:
        return jsonify({"answer": "AI Error: GROQ_API_KEY is missing in Vercel settings."}), 500
    
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are StudingWell AI, a professional math tutor. Use LaTeX for math like $$ x^2 $$."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": f"AI Error: {str(e)}"}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = data.get('username')
    pw = data.get('password')
    if not user or not pw:
        return jsonify({"message": "Username and password required"}), 400
    
    hashed = generate_password_hash(pw)
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, hashed))
        conn.commit()
        conn.close()
        return jsonify({"message": "Success"}), 201
    except:
        return jsonify({"message": "Username taken"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = data.get('username')
    pw = data.get('password')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (user,))
    u = c.fetchone()
    conn.close()
    
    if u and check_password_hash(u[2], pw):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Vercel-hez kell
app = app

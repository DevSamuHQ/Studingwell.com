import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from groq import Groq

app = Flask(__name__)
CORS(app)

# Use /tmp for the database in Vercel environment
DB_PATH = '/tmp/users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)')
    conn.commit()
    conn.close()

init_db()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are StudingWell AI, a professional math tutor. Use LaTeX for equations like $$ x^2 $$."},
                {"role": "user", "content": data.get('prompt')}
            ]
        )
        return jsonify({"answer": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": "AI service error. Check API key."}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user, pw = data.get('username'), data.get('password')
    hashed = generate_password_hash(pw)
    try:
        conn = sqlite3.connect(DB_PATH); c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, hashed))
        conn.commit(); conn.close()
        return jsonify({"message": "Registration successful!"}), 201
    except:
        return jsonify({"message": "Username taken."}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user, pw = data.get('username'), data.get('password')
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (user,))
    u = c.fetchone(); conn.close()
    if u and check_password_hash(u[2], pw):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401
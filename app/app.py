from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import subprocess
subprocess.run(['python3', 'update_db_and_generate_html.py'])


app = Flask(__name__)

DB_FILE = 'questions.db'

# Create DB + table if not exist
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE questions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            question TEXT NOT NULL,
                            answer TEXT,
                            topic TEXT,
                            difficulty TEXT
                        )''')
        conn.commit()
        conn.close()

# Get all questions
@app.route("/questions", methods=["GET"])
def get_questions():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()
    conn.close()
    # Convert to list of dicts
    questions = [{
        "id": r[0], "question": r[1], "answer": r[2], 
        "topic": r[3], "difficulty": r[4]
    } for r in rows]
    return jsonify(questions)

# Serve frontend
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        # Simple hardcoded auth (optional)
        token = request.form.get("token")
        if token != "secret123":
            return "Unauthorized", 403

        q = request.form.get("question")
        a = request.form.get("answer")
        t = request.form.get("topic")
        d = request.form.get("difficulty")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO questions (question, answer, topic, difficulty) VALUES (?, ?, ?, ?)", 
                       (q, a, t, d))
        conn.commit()
        conn.close()
        return "Question added!"
    else:
        return render_template("add-question.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)


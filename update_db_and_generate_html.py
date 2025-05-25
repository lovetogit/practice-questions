import csv
import sqlite3
import os

DB_PATH = 'app/questions.db'
CSV_PATH = 'questions.csv'
HTML_PATH = 'docs/index.html'

def init_db():
    os.makedirs("app", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT,
            topic TEXT,
            difficulty TEXT
        )
    ''')
    conn.commit()
    conn.close()

def import_csv_to_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                c.execute('''
                    INSERT OR IGNORE INTO questions (question, answer, topic, difficulty)
                    VALUES (?, ?, ?, ?)
                ''', (row["question"], row["answer"], row["topic"], row["difficulty"]))
            except Exception as e:
                print(f"⚠️ Skipped row due to error: {e}")

    conn.commit()
    conn.close()

def generate_html():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT question, answer, topic, difficulty FROM questions')
    rows = c.fetchall()
    conn.close()

    html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Practice Questions</title>
  <style>
    body { font-family: sans-serif; max-width: 800px; margin: 2rem auto; }
    details { background: #fff; padding: 1rem; margin: 1rem 0; border-radius: 8px; box-shadow: 0 0 6px #ccc; }
    summary { font-weight: bold; cursor: pointer; }
    p { margin-top: 0.5rem; }
  </style>
</head>
<body>
  <h1>🧠 Practice Questions</h1>
  <p class="sub">Generated from SQLite DB</p>
'''

    for q, a, t, d in rows:
        html += f'''
<details>
  <summary>{q}</summary>
  <p><strong>Answer:</strong> {a}</p>
  <p><em>{t} | {d}</em></p>
</details>
'''

    html += '</body></html>'

    os.makedirs("docs", exist_ok=True)
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Generated {HTML_PATH} with {len(rows)} questions.")

# 🏁 Run the full pipeline
if __name__ == "__main__":
    init_db()
    import_csv_to_db()
    generate_html()


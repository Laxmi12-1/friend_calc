from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect("friendship.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name1 TEXT NOT NULL,
            name2 TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():

    conn = sqlite3.connect("friendship.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM history
        ORDER BY id DESC
        LIMIT 10
    """)

    history = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        history=history
    )


@app.route('/calculate', methods=['POST'])
def calculate():

    name1 = request.form['name1']
    name2 = request.form['name2']

    score = (sum(ord(c) for c in (name1 + name2)) % 41) + 60

    if score >= 90:
        message = "❤️ Best Friends Forever"
    elif score >= 80:
        message = "😊 Great Friends"
    elif score >= 70:
        message = "👍 Good Friends"
    else:
        message = "🤝 Needs More Bonding"

    conn = sqlite3.connect("friendship.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO history(name1,name2,score)
        VALUES(?,?,?)
        """,
        (name1, name2, score)
    )

    conn.commit()

    cursor.execute("""
        SELECT * FROM history
        ORDER BY id DESC
        LIMIT 10
    """)

    history = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        score=score,
        message=message,
        name1=name1,
        name2=name2,
        history=history
    )


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

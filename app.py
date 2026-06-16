from flask import Flask, render_template, request
import sqlite3
import os

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


# Home page (history hidden)
@app.route("/")
def home():
    return render_template("index.html", history=[])


# Calculate friendship
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


    # Save calculation in database
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
    conn.close()


    # Do NOT send old history back
    return render_template(
        "index.html",
        score=score,
        message=message,
        name1=name1,
        name2=name2,
        history=[]
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

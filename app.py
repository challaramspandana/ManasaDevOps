import os
import sqlite3
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "notice-board-demo-key")
DB = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "notices.db"))

def connect():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

def initialize_database():
    db = connect()
    db.execute("""CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL, category TEXT NOT NULL, content TEXT NOT NULL,
        published_by TEXT NOT NULL, posted_on TEXT NOT NULL, expiry_date TEXT
    )""")
    if db.execute("SELECT COUNT(*) FROM notices").fetchone()[0] == 0:
        today = date.today().isoformat()
        db.executemany("""INSERT INTO notices
            (title, category, content, published_by, posted_on, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?)""", [
            ("Hackathon 2026 Registration", "Events", "Registrations are open for the annual college hackathon. Form teams and register before the deadline.", "IT Department", today, None),
            ("Library Timings Update", "General", "The library will remain open until 7:00 PM on working days this week.", "Library", today, None),
            ("Placement Training Session", "Placements", "A placement preparation session on aptitude and technical interviews will be conducted in Seminar Hall 2.", "Training and Placement Cell", today, None)
        ])
    db.commit()
    db.close()

@app.route("/")
def home():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    sql = "SELECT * FROM notices WHERE 1=1"
    params = []
    if search:
        sql += " AND (title LIKE ? OR content LIKE ? OR published_by LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY id DESC"
    db = connect()
    notices = db.execute(sql, params).fetchall()
    db.close()
    return render_template("index.html", notices=notices, search=search, selected_category=category)

@app.route("/add-notice", methods=["POST"])
def add_notice():
    fields = [request.form.get(k, "").strip() for k in
              ("title", "category", "content", "published_by")]
    expiry = request.form.get("expiry_date", "").strip() or None
    if not all(fields):
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("home"))
    db = connect()
    db.execute("""INSERT INTO notices
        (title, category, content, published_by, posted_on, expiry_date)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (*fields, datetime.now().strftime("%Y-%m-%d"), expiry))
    db.commit()
    db.close()
    flash("Notice published successfully.", "success")
    return redirect(url_for("home"))

@app.route("/delete-notice/<int:notice_id>", methods=["POST"])
def delete_notice(notice_id):
    db = connect()
    db.execute("DELETE FROM notices WHERE id = ?", (notice_id,))
    db.commit()
    db.close()
    flash("Notice deleted.", "success")
    return redirect(url_for("home"))

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=False)

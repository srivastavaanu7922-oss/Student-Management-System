from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT,
        course TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        course = request.form["course"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, roll, course) VALUES (?, ?, ?)",
            (name, roll, course)
        )

        conn.commit()
        conn.close()

        return redirect("/view")

    return render_template("add_student.html")

@app.route("/view")
def view_students():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template("view_students.html", students=students)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        course = request.form["course"]

        cursor.execute(
            "UPDATE students SET name=?, roll=?, course=? WHERE id=?",
            (name, roll, course, id)
        )
        conn.commit()
        conn.close()

        return redirect("/view")

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()

    return render_template("edit_student.html", student=student)

@app.route("/delete/<int:id>")
def delete_student(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/view")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
c.execute("DELETE FROM users") 
c.execute("INSERT INTO users (username, password) VALUES ('admin','admin123'), ('guest','guest123')")
conn.commit()


@app.route("/sqli", methods=["GET", "POST"])
def sqli():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("QUERY:", query)

        result = c.execute(query).fetchall()
        if result:
            return render_template("sqli.html", message=f"✅ Welcome {username}!")
        else:
            return render_template("sqli.html", message="❌ Login Failed!")

    return render_template("sqli.html", message="")


comments = []

@app.route("/xss", methods=["GET", "POST"])
def xss():
    if request.method == "POST":
        msg = request.form.get("msg", "")
        if msg:
            comments.append(msg)  

    return render_template("xss.html", comments=comments)

@app.route("/")
def index():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

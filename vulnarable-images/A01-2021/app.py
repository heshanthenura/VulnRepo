import json
from flask import Flask, request, redirect, url_for, render_template, abort, session

app = Flask(__name__)
app.secret_key = "supersecretkey" 

with open("users.json") as f:
    users = json.load(f)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user_id"] = user["id"]
                return redirect(url_for("profile", user_id=user["id"]))

        return render_template("login.html", error="Invalid credentials!")
    return render_template("login.html")

@app.route("/<int:user_id>")
def profile(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    for user in users:
        if user["id"] == user_id:
            return render_template("profile.html", profile=user["profile"])
    
    abort(404)

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

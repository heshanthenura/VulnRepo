from flask import Flask, render_template, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = "supersecretkey"


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    app=app
)


USER = {"username": "admin", "password": "admin123"}


@app.route("/login-nolimit", methods=["GET", "POST"])
def login_no_limit():
    error = None
    status_code = 200
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USER["username"] and password == USER["password"]:
            return render_template("success.html", username=username), 200
        else:
            error = "Invalid credentials"
            status_code = 401
    return render_template("login_nolimit.html", error=error), status_code


@app.route("/login-limit", methods=["GET", "POST"])
@limiter.limit("3 per minute") 
def login_limit():
    error = None
    status_code = 200
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USER["username"] and password == USER["password"]:
            return render_template("success.html", username=username), 200
        else:
            error = "Invalid credentials"
            status_code = 401
    return render_template("login_limit.html", error=error), status_code


@app.errorhandler(429)
def ratelimit_handler(e):
    return "Rate limit exceeded", 404


@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

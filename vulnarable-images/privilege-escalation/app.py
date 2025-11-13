from flask import (
    Flask, request, redirect, url_for, session, flash,
    abort, jsonify, render_template
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order_mgmt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='customer')

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')

REG_ALLOWED = {'username', 'password', 'role'}
ALLOWED_ROLE_VALUES = {'admin', 'customer'} 

def login_user(user):
    session['user_id'] = user.id
    session['username'] = user.username

def logout_user():
    session.clear()

def current_user():
    uid = session.get('user_id')
    if not uid:
        return None
    return User.query.get(uid)

def require_login(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped

def require_admin_db(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        uid = session.get('user_id')
        if not uid:
            return redirect(url_for('login'))
        u = User.query.get(uid)
        if not u or u.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return wrapped

def init_db():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password_hash=generate_password_hash('admin'), role='admin')
        db.session.add(admin)
        db.session.commit()
        app.logger.info("Default admin created: username=admin password=admin")

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json() or {}
            received_keys = set(data.keys())
        else:
            data = request.form
            received_keys = set(request.form.keys())

        unexpected = received_keys - REG_ALLOWED
        if unexpected:
            app.logger.warning("Blocked register with unexpected fields: %s from %s", sorted(unexpected), request.remote_addr)
            return jsonify({
                "error": "unexpected_parameters",
                "unexpected": sorted(list(unexpected)),
                "message": "Malformed request — only 'username' and 'password' (and optional 'role') are allowed."
            }), 400

        if 'role' in received_keys:
            role_value = (data.get('role') or '')
            if role_value not in ALLOWED_ROLE_VALUES:
                app.logger.warning("Blocked register with invalid role value: %s from %s", role_value, request.remote_addr)
                return jsonify({
                    "error": "role_incorrect",
                    "received_role": role_value,
                    "allowed_roles": sorted(list(ALLOWED_ROLE_VALUES)),
                    "message": "Role value is incorrect (case-sensitive)."
                }), 400
            assigned_role = role_value
        else:
            assigned_role = 'customer'

        username = (data.get('username') or '').strip()
        password = (data.get('password') or '').strip()
        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for('register'))

        user = User(username=username, password_hash=generate_password_hash(password), role=assigned_role)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. You can now log in.")
        return redirect(url_for('login'))

    return render_template('register.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json() or {}
            username = data.get('username') or ''
            password = data.get('password') or ''
        else:
            username = request.form.get('username') or ''
            password = request.form.get('password') or ''

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
        return redirect(url_for('login'))

    return render_template('login.html', current_user=current_user)

@app.route('/dashboard')
@require_login
def dashboard():
    u = current_user()
    return render_template('dashboard.html', user=u, current_user=current_user)

@app.route('/admin_panel')
@require_admin_db
def admin_panel():
    orders = Order.query.all()
    rows = []
    for o in orders:
        owner = User.query.get(o.owner_id)
        rows.append({
            'id': o.id,
            'product': o.product,
            'price': o.price,
            'owner': owner.username if owner else 'unknown',
            'status': o.status
        })
    return render_template('admin_panel.html', orders=rows, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))

@app.route('/setup_demo_data')
def setup_demo_data():
    if User.query.filter(User.username != 'admin').count() > 0:
        return "Demo data already present."
    u1 = User(username='alice', password_hash=generate_password_hash('alicepass'), role='customer')
    u2 = User(username='bob', password_hash=generate_password_hash('bobpass'), role='customer')
    db.session.add_all([u1, u2])
    db.session.commit()
    o1 = Order(product='Widget A', price=9.99, owner_id=u1.id)
    o2 = Order(product='Gadget B', price=19.99, owner_id=u2.id)
    db.session.add_all([o1, o2])
    db.session.commit()
    return "Demo users created: alice/bob and two orders."

@app.errorhandler(403)
def forbidden(e):
    return render_template('forbidden.html', current_user=current_user), 403

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

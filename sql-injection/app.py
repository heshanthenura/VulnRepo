import hashlib
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  
    return conn

def hash_password_sha256(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()



@app.route('/')
def home():
    conn = get_db_connection()
    query = "SELECT * FROM products LIMIT 5"
    print(f"Executing query: {query}") 
    products = conn.execute(query).fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Login attempt with Username: {username} and Password: {password}")
        
        hashed_password = hash_password_sha256(password)
        print(f"Hashed Password: {hashed_password}")

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user:
            stored_hash = user['password']
            if stored_hash == hashed_password:
                session['username'] = username
                session['role'] = user['role']

              
                if user['role'] == 'admin':
                    return redirect(url_for('admin'))  
                
                
                elif username == 'user123':
                    return redirect(url_for('user'))  

            
                else:
                    return redirect(url_for('profile'))  

            else:
                error_message = "Invalid Credentials. Please try again."
        else:
            error_message = "Invalid Credentials. Please try again."
    return render_template('login.html', error_message=error_message)

@app.route('/admin')
def admin():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html')  
    else:
        return redirect(url_for('login'))

@app.route('/user')
def user():
    if 'username' in session and session['username'] == 'user123':
        return render_template('user_dashboard.html')  
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html')  # Profile page template
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = ""
    
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
        
        if not error_message:
            conn = get_db_connection()
            existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
            conn.close()
            
            if existing_user:
                error_message = "Username or Email already exists. Please choose a different one."
            else:
                # If no errors, hash the password and insert into the database
                hashed_password = hash_password_sha256(password)
                
                conn = get_db_connection()
                conn.execute('INSERT INTO users (full_name, email, username, password) VALUES (?, ?, ?, ?)', 
                             (full_name, email, username, hashed_password))
                conn.commit()
                conn.close()
                
                return redirect(url_for('login')) 

    return render_template('register.html', error_message=error_message)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    products = []

    if query:
        conn = get_db_connection()
        sql_query = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
        print(f"Executing query: {sql_query}") 
        products = conn.execute(sql_query).fetchall()
        conn.close()

    print(f"Search query: {query}") 
    return render_template('index.html', query=query, products=products)

@app.route('/dashboard')
def dashboard():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin')) 
        elif session['role'] == 'user':
            return redirect(url_for('user'))  
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

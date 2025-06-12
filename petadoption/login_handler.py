# login_handler.py
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secret_key'  # Change this to a secure secret key

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kruthi10",
        database="petadoption"
    )
    cursor = mydb.cursor()
    
    # Check credentials
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    cursor.close()
    mydb.close()
    
    if user:
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('pet_management'))
    else:
        return render_template('login.html', error="Please enter the correct user name and password")

@app.route('/pet_management')
@login_required
def pet_management():
    import main  # Import your existing main.py
    return main.root.mainloop()

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
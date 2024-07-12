import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import ConnectionFailure

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

def check_mongo_connection():
    try:
        mongo.cx.admin.command('ping')
        print("MongoDB connection successful")
    except ConnectionFailure:
        print("MongoDB connection failed")
        return False
    return True

if not check_mongo_connection():
    raise Exception("Failed to connect to MongoDB. Please check your settings.")

@app.route('/')
def welcome():
    if 'email' in session:
        return redirect(url_for('home'))
    return render_template('welcome.html')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('welcome'))

    existing_email = mongo.db.users.find_one({'email': email})
    if existing_email:
        flash('Email already registered!', 'error')
        return redirect(url_for('welcome'))

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': hashed_password,
        'is_admin': False,  # Default is_admin to False      
    })

    flash('User created successfully! Please sign in.', 'success')
    return redirect(url_for('welcome'))

@app.route('/sign_in', methods=['POST'])
def sign_in():
    email = request.form.get('email')
    password = request.form.get('password')

    user = mongo.db.users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        session['email'] = email
        session['is_admin'] = user.get('is_admin', False)
        flash(f'Welcome back, {user["first_name"]}!', 'success')
        return redirect(url_for('home'))

    flash('Invalid email or password!', 'error')
    return redirect(url_for('welcome'))

@app.route('/home')
def home():
    if 'email' in session:
        user = mongo.db.users.find_one({'email': session['email']})
        return render_template('profile.html', user=user)
    return redirect(url_for('welcome'))

@app.route('/sign_out')
def sign_out():
    session.pop('email', None)
    session.pop('is_admin', None)
    flash('Signed out successfully!', 'success')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
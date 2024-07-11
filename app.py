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
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('welcome.html')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    users_name = request.form.get('users_name')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    is_admin = request.form.get('is_admin') == 'on'

    if password != confirm_password:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('welcome'))

    existing_user = mongo.db.users.find_one({'username': username})
    if existing_user:
        flash('Username already exists!', 'error')
        return redirect(url_for('welcome'))

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({
        'username': username,
        'password': hashed_password,
        'is_admin': is_admin
    })
    flash('User created successfully! Please sign in.', 'success')
    return redirect(url_for('welcome'))

@app.route('/sign_in', methods=['POST'])
def sign_in():
    username = request.form.get('username')
    password = request.form.get('password')

    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        session['username'] = username
        session['is_admin'] = user.get('is_admin', False)
        flash(f'Welcome {username}!', 'success')
        return redirect(url_for('home'))

    flash('Invalid username or password!', 'error')
    return redirect(url_for('welcome'))

@app.route('/home')
def home():
    if 'username' in session:
        is_admin = session.get('is_admin', False)
        return render_template('profile.html', username=session['username'], is_admin=is_admin)
    return redirect(url_for('welcome'))

@app.route('/sign_out')
def sign_out():
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('Signed out successfully!', 'success')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
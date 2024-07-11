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
def home():
    return "Hello, Flask with MongoDB!"


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
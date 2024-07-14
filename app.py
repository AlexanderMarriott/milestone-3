import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import ConnectionFailure

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Security enhancements
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True  # Set to True if using HTTPS

mongo = PyMongo(app)


def check_mongo_connection():
    try:
        mongo.cx.admin.command("ping")
        print("MongoDB connection successful")
    except ConnectionFailure:
        print("MongoDB connection failed")
        return False
    return True


if not check_mongo_connection():
    raise Exception("Failed to connect to MongoDB. Please check your settings.")


@app.route("/")
def welcome():
    if "user_id" in session:
        return redirect(url_for("home"))
    return render_template("welcome.html")


@app.route("/sign_up", methods=["POST"])
def sign_up():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Passwords do not match!", "error")
        return redirect(url_for("welcome"))

    existing_email = mongo.db.users.find_one({"email": email})
    if existing_email:
        flash("Email already registered!", "error")
        return redirect(url_for("welcome"))

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one(
        {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password,
            "is_admin": False,  # Default is_admin to False
        }
    )

    flash("User created successfully! Please sign in.", "success")
    return redirect(url_for("welcome"))


@app.route("/sign_in", methods=["POST"])
def sign_in():
    email = request.form.get("email")
    password = request.form.get("password")

    user = mongo.db.users.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        session["user_id"] = str(user["_id"])  # Store ObjectId as a string in session
        session["is_admin"] = user.get("is_admin", False)
        flash(f'Welcome, {user["first_name"]}!', "success")
        return redirect(url_for("home"))

    flash("Invalid email or password!", "error")
    return redirect(url_for("welcome"))


@app.route("/home")
def home():
    if "user_id" in session:
        user_id = session["user_id"]
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        user_profile = mongo.db.profile_info.find_one({"created_by": user_id})
        # Pass both user and profile data to the template
        return render_template("profile.html", user=user, profile=user_profile)
    return redirect(url_for("welcome"))


@app.route("/update_profile", methods=["POST"])
def update_profile_route():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("welcome"))

    profile_data = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        # Add other fields as necessary
        "created_by": user_id,
    }
    existing_profile = mongo.db.profile_info.find_one({"created_by": user_id})
    if existing_profile:
        mongo.db.profile_info.update_one(
            {"created_by": user_id}, {"$set": profile_data}
        )
    else:
        mongo.db.profile_info.insert_one(profile_data)
    flash("Profile updated successfully!", "success")
    return redirect(url_for("home"))


@app.route("/sign_out")
def sign_out():
    session.pop("user_id", None)  # Remove user_id from session
    session.pop("is_admin", None)
    flash("Signed out successfully!", "success")
    return redirect(url_for("welcome"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

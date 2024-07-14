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
        return redirect(url_for("profile", user_id=session["user_id"]))
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
        return redirect(url_for("profile", user_id=session["user_id"]))

    flash("Invalid email or password!", "error")
    return redirect(url_for("welcome"))


@app.route("/profile/<user_id>")
def profile(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        flash("User not found", "error")
        return redirect(url_for("welcome"))

    user_profile = mongo.db.profile_info.find_one({"created_by": user_id}) or {}
    certifications = list(mongo.db.certifications.find({"created_by": user_id}))
    experience = list(mongo.db.experience.find({"created_by": user_id}))
    program_lang = list(mongo.db.program_lang.find({"created_by": user_id}))
    projects = list(mongo.db.projects.find({"created_by": user_id}))
    qualifications = list(mongo.db.qualifications.find({"created_by": user_id}))

    profile_data = {
        "user": user,
        "profile_info": user_profile,
        "certifications": certifications,
        "experience": experience,
        "program_lang": program_lang,
        "projects": projects,
        "qualifications": qualifications,
    }

    return render_template("profile.html", profile_data=profile_data)


@app.route("/update_profile", methods=["POST"])
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("welcome"))

    profile_data = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "profile_image": request.form.get("profile_image"),
        "tagline": request.form.get("tagline"),
        "github_url": request.form.get("github_url"),
        "linkedin_url": request.form.get("linkedin_url"),
        "profile_headline": request.form.get("profile_headline"),
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
    return redirect(url_for("profile", user_id=user_id))


@app.route("/update_experience", methods=["POST"])
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("welcome"))

    experience_data = {
        "company_img": request.form.get("company_img"),
        "company_name": request.form.get("company_name"),
        "position": request.form.get("position"),
        "start_date": request.form.get("start_date"),
        "end_date": request.form.get("end_date"),
        "job_description": request.form.get("linkedin_url"),
        "created_by": user_id,
    }
    existing_profile = mongo.db.experience.find_one({"created_by": user_id})
    if existing_profile:
        mongo.db.profile_info.update_one(
            {"created_by": user_id}, {"$set": experience_data}
        )
    else:
        mongo.db.profile_info.insert_one(experience_data)
    flash("Experience updated successfully!", "success")
    return redirect(url_for("profile", user_id=user_id))


@app.route("/sign_out")
def sign_out():
    session.pop("user_id", None)  # Remove user_id from session
    session.pop("is_admin", None)
    flash("Signed out successfully!", "success")
    return redirect(url_for("welcome"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

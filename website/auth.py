from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        username_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if username_exists:
            flash("Username already registered!", category="error")
        
        elif len(username) < 4: # type: ignore
            flash("Username is too short!", category="error")
        
        elif email_exists:
            flash("Email already registered!", category="error")
        
        elif len(password1) < 8: # type: ignore
            flash("Password is too short!", category="error")
        
        elif password1 != password2:
            flash("Passwords don't match!", category="error")
        
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="scrypt")) # type: ignore
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
    
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password): # type: ignore
                login_user(user, remember=True)
                flash("Logged in successfully!", category="success")
                return redirect(url_for("views.home"))
            
            else:
                flash("Incorrect password.", category="error")
        
        else:
            flash("User does not exist.", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
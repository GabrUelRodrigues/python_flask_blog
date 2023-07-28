from flask import Blueprint

auth = Blueprint("auth", __name__)

@auth.route("/sign-up")
def sign_up():
    return "Sign up"

@auth.route("/login")
def login():
    return "Login"

@auth.route("/logout")
def logout():
    return "Logout"
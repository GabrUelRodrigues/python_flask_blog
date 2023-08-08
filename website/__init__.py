from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "M4yT#3F0r(eB3W!t#Y0u"
	app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
	db.init_app(app)

	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix="/")
	app.register_blueprint(auth, url_prefix="/")

	from .models import User, Post
	
	with app.app_context():
		create_database()

	login_manager = LoginManager()
	login_manager.login_view = "auth.login" # type: ignore
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))
    
	return app

def create_database():
	if not path.exists(f"instance/{DB_NAME}"):
		db.create_all()
		print("Database created!")
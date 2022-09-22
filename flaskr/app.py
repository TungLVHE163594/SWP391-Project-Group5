from flask import Flask, render_template, request
from dotenv import load_dotenv
from models.model import db
from pathlib import Path
import os
from controllers.mail_service import mail
from flask_mail import Mail 
from routers.user import user_router

#load environment variables
env_path = Path('.') / '../.env'
load_dotenv(dotenv_path=env_path)

#start
app = Flask(__name__)

#database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True

# stmp server

app.secret_key = os.getenv('SECRET_KEY')

#start database
db.init_app(app)
db.create_all(app=app)

#start mail service
mail = Mail(app)

#register blueprint
app.register_blueprint(user_router, url_prefix="/user")


@app.route("/")
def index():
    return render_template("home.html", stringName = "You are not logged in",isLogin = False)

app.run("0.0.0.0", port=os.environ["port"], debug=True)
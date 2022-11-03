from flask import Flask

# New imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from os import environ
import mysql.connector

# force loading of environment variables
load_dotenv('.flaskenv')

# Get the environment variables from .flaskenv
IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USER')
PASSWORD = environ.get('MYSQL_PASS')
DB_NAME = environ.get('MYSQL_DB')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc33O'

# Specify the connection parameters/credentials for the database
DB_CONFIG_STR = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)

login = LoginManager(app)

# enables @login_required
login.login_view = 'login'

from app import routes, models
from app.models import Users    

#Create DB Tables


# Create DB schema
db.create_all()


# Create admin and basic user account
admin1 = Users.query.filter_by(is_admin='1').first()
if admin1 is None:
    admin = Users(user_id=1, first_name='admin',last_name='admin',is_admin='1',username='admin',password_hash='password')
    db.session.add(admin)
    db.session.commit()

user1 = Users.query.filter_by(is_admin='0').first()
if user1 is None:
    user = Users(user_id=2, first_name='user',last_name='user',is_admin='0',username='user',password_hash='password')
    db.session.add(user)
    db.session.commit()
"""
Initialize the Flask application, configure database connection,
load environment variables, and enable CORS for frontend-backend communication.
"""


import os 
from dotenv import load_dotenv 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app import routes, models


#read the .env file
load_dotenv()  
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

#allow front
app = Flask(__name__, instance_relative_config=True)
CORS(app)

#db
os.makedirs(app.instance_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'promecloud.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)





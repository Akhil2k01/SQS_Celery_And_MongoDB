"""
docstring
"""
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_login import LoginManager
from flask_mail import Mail
from flask_caching import Cache
from flask_session import Session
from mongoengine import connect
from config import Config

# connect to the database
# connect('close_loop_validation',
#         username=Config.MONGO_USERNAME,
#         password=Config.MONGO_PWD,
#         host=Config.MONGODB_HOST, port=27017)

mongo_db = MongoEngine()
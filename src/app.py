import os
from flask import Flask, jsonify

from flask_cors import CORS
from flask_restful import Api
from datetime import datetime

from src.common import app_logger
from src.database.db import db

from src.config import APP_VERSION
from src.resources.user import UserRegister, User, UserLogin, TokenRefresh
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

logger = app_logger.logging.getLogger('app')

app = Flask(__name__)

load_dotenv(".env")
app.config["SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)

CORS(app)

jwt = JWTManager(app)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # Instead of hard-coding, you should read from a config file or database.
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(User, '/user/<int:user_id>')


@app.route('/ping', methods=['GET'])
def hello():
    return jsonify({
        "message": "Hello world, from src version {}".format(APP_VERSION),
        "local_time": "{}".format(datetime.now())
    }), 200

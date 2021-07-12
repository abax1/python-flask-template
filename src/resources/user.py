from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_claims, \
    jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse, request
from werkzeug.security import safe_str_cmp

from src.models.user import UserModel
from src.schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json())

        if UserModel.find_by_username(user_data['username']):
            return {"message": "A user with that username already exists."}, 400

        user = UserModel(**user_data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        return user.json()

    @classmethod
    @jwt_required
    def delete(cls, user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        user.delete_from_db()
        return {"message": "User deleted."}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type='str',
        required=True,
        help="This field cannot be left blank."
    )
    parser.add_argument(
        'password',
        type='str',
        required=True,
        help="This field cannot be left blank."
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()  # TODO: Add marshmallow and password hashing.

        user = UserModel.find_by_id(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': 'Invalid credentials.'}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

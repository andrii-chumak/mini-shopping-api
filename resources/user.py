from flask import request
from flask_restful import Resource

from models.user import UserModel


class UserRegister(Resource):
    def post(self):
        data = request.get_json()

        if UserModel.find_by_username(data['username']):
            return {'message': 'This username is already in use.'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': "User created."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': "User with id '{}' doesn't exist".format(user_id)}, 404

        return user.to_json()

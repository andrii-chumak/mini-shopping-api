from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username is required field"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password is required field"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'This username is already in use.'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': "User created."}, 201


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': "User with id '{}' doesn't exist".format(user_id)}, 404

        return user.to_json()

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User with id '{}' doesn't exist".format(user_id)}, 404

        user.delete_from_db()
        return {'message': 'User deleted'}, 200

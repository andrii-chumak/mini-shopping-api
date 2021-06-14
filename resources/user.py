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
        """
           Call this query to register new user
           ---
           headers:
             - Content-Type: application/json
           json:
             - name:        str
             - password     str
           responses:
              201:
                id:         int
                username:   str
              400:
                message: 'This username is already in use.'
        """
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'This username is already in use.'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': "User created."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        """
           Call this query to get user by id
           ---
           params:
             - user_id:     int
           responses:
              200:
                id:         int
                username:   str
              404:
                message:  "User with id '<id>' doesn't exist"
        """
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': "User with id '{}' doesn't exist".format(user_id)}, 404

        return user.to_json()

    def delete(self, user_id):
        """
           Call this query to delete user by id
           ---
           params:
             - user_id:     int
           responses:
              200:
                message: 'User deleted'
              404:
                message: "User with id '<id>' doesn't exist"
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User with id '{}' doesn't exist".format(user_id)}, 404

        user.delete_from_db()
        return {'message': 'User deleted'}, 200

from flask import Flask
from flask_restful import Api

from resources.user import User, UserRegister

from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


api = Api(app)
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)

from flask import Flask
from database import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)

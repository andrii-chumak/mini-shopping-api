from database import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db)
    username = db.Column(db.String(80))
    password = db.Column(db.String(40))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

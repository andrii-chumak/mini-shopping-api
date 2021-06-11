from database import db


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, user_id):
        self.user_id = user_id
        self.status = 'Created'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_order_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

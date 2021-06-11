from database import db


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def to_json(self):
        return {
            'name': self.name,
            'price': self.price
        }

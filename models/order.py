from database import db


class OrderProduct(db.Model):
    __tablename__ = 'ordered_products'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, default=1)


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("UserModel", back_populates="orders")

    products = db.relationship('ProductModel', secondary='ordered_products', lazy='dynamic')

    def __init__(self, user_id, products):
        self.user_id = user_id
        self.status = 'Created'
        self.products = products

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def get_quantity_by_product_id(self, product_id):
        order_product = db.session.query(OrderProduct).filter_by(order_id=self.id).filter_by(product_id=product_id).first()
        return order_product.quantity

    def to_json(self):
        products = [product.to_json() for product in self.products.all()]
        for product in products:
            product['quantity'] = self.get_quantity_by_product_id(product['id'])

        return {
            'id': self.id,
            'user_id': self.user_id,
            'products': products
        }

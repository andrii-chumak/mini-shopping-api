from database import db


class OrderStatus:
    created = 1
    payed = 2
    packed = 3
    shipped = 4
    delivered = 5

    status_dict = {
        created: 'Created',
        payed: 'Payed',
        packed: 'Packed',
        shipped: 'Shipped',
        delivered: 'Delivered',
    }

    @classmethod
    def to_text(cls, status):
        return cls.status_dict[status]


class OrderProduct(db.Model):
    __tablename__ = 'ordered_products'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, default=1)
    free_products = db.Column(db.Integer, default=0)


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("UserModel", back_populates="orders")

    products = db.relationship('ProductModel', secondary='ordered_products', lazy='dynamic')
    total = db.Column(db.Float(precision=2))

    def __init__(self, user_id, products, total):
        self.user_id = user_id
        self.total = total
        self.products = products
        self.status = OrderStatus.created

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def get_quantity_by_product_id(self, product_id):
        order_product = db.session.query(OrderProduct).filter_by(order_id=self.id).filter_by(product_id=product_id).first()
        return order_product.quantity

    def set_quantity_by_product_id(self, product_id, value):
        order_product = db.session.query(OrderProduct).filter_by(order_id=self.id).filter_by(product_id=product_id)
        order_product.update({OrderProduct.quantity: value})
        self.save_to_db()

    def get_number_free_products(self, product_id):
        order_product = db.session.query(OrderProduct).filter_by(order_id=self.id).filter_by(product_id=product_id).first()
        return order_product.free_products

    def set_number_free_products(self, product_id, value):
        order_product = db.session.query(OrderProduct).filter_by(order_id=self.id).filter_by(product_id=product_id)
        order_product.update({OrderProduct.free_products: value})
        self.save_to_db()

    def to_json(self):
        products = [product.to_json() for product in self.products.all()]
        for product in products:
            product['quantity'] = self.get_quantity_by_product_id(product['id'])
            product['free'] = self.get_number_free_products(product['id'])

        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.get_status(),
            'products': products,
            'total': self.total
        }

    def set_status(self, status):
        self.status = status
        self.save_to_db()

    def get_status(self):
        return OrderStatus.to_text(self.status)

from database import db


class CartProduct(db.Model):
    __tablename__ = 'picked_products'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, default=1)
    free_products = db.Column(db.Integer, default=0)


class CartModel(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("UserModel", back_populates="cart")

    products = db.relationship('ProductModel', secondary='picked_products', lazy='dynamic')
    discount = db.Column(db.Integer, default=0)

    def __init__(self, user_id):
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, user_id):
        cart = cls.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = CartModel(user_id)
            cart.save_to_db()

        return cart

    def add_product(self, product):
        if product in self.products:
            self.change_quantity_by_product_id(product.id, 1)
        else:
            self.products.append(product)

        self.save_to_db()

    def remove_product(self, product):
        if product in self.products:
            quantity = self.get_quantity_by_product_id(product.id)
            if quantity == 1:
                self.products.remove(product)
            else:
                self.change_quantity_by_product_id(product.id, -1)

        self.save_to_db()

    def get_quantity_by_product_id(self, product_id):
        cart_product = db.session.query(CartProduct).filter_by(cart_id=self.id).filter_by(product_id=product_id).first()
        return cart_product.quantity

    def change_quantity_by_product_id(self, product_id, value):
        cart_product = db.session.query(CartProduct).filter_by(cart_id=self.id).filter_by(product_id=product_id)
        cart_product.update({CartProduct.quantity: CartProduct.quantity + value})
        self.save_to_db()

    def get_number_free_products(self, product_id):
        cart_product = db.session.query(CartProduct).filter_by(cart_id=self.id).filter_by(product_id=product_id).first()
        return cart_product.free_products

    def set_number_free_products(self, product_id, value):
        cart_product = db.session.query(CartProduct).filter_by(cart_id=self.id).filter_by(product_id=product_id)
        cart_product.update({CartProduct.free_products: value})
        self.save_to_db()

    def set_discount(self, discount):
        self.discount = discount
        self.save_to_db()

    def delete_all_from_cart(self):
        self.products = []
        self.save_to_db()

    def to_json(self):
        products = [product.to_json() for product in self.products.all()]
        for product in products:
            product['quantity'] = self.get_quantity_by_product_id(product['id'])

        return {
            'id': self.id,
            'user_id': self.user_id,
            'products': products
        }


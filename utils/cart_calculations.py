def make_discounts(cart):
    def fifth_product_free(cart):
        for product in cart.products:
            offers_number = cart.get_quantity_by_product_id(product.id) // 5
            cart.set_number_free_products(product.id, offers_number)

    def amount_more_20(cart):
        if calculate_subtotal(cart) >= 20:
            cart.set_discount(1)

    discounts = [
        fifth_product_free,
        amount_more_20
    ]

    cart.set_discount(0)
    for discount in discounts:
        discount(cart)


def check_preconditions(cart):
    def max_price(cart):
        message = 'Total amount cannot exceed 100$'
        if calculate_total(cart) > 100:
            return False, message
        return True, 'Ok'

    preconditions = [
        max_price,
    ]

    for precondition in preconditions:
        result, message = precondition(cart)
        if result is False:
            return False, message

    return result, 'Ok'


def calculate_total(cart):
    total = 0
    make_discounts(cart)
    for product in cart.products:
        quantity = cart.get_quantity_by_product_id(product.id)
        quantity_free = cart.get_number_free_products(product.id)
        total += product.price * (quantity - quantity_free)

    return total - cart.discount


def calculate_subtotal(cart):
    subtotal = 0
    for product in cart.products:
        subtotal += product.price * cart.get_quantity_by_product_id(product.id)

    return subtotal

from decimal import Decimal

def calculate_delivery(order_items):
    # If bag/order_items is empty, no delivery charge
    if not order_items:
        return Decimal('0.00'), 'None', Decimal('0.00')

    size_counts = {'small': 0, 'medium': 0, 'large': 0}
    total_price = Decimal('0.00')

    for item in order_items:
        product = item['product']
        qty = item['quantity']
        size = product.get_size_display().lower()

        if size in size_counts:
            size_counts[size] += qty

        total_price += item['line_total']

    # delivery charge logic
    LARGE_DELIVERY_CHARGE = Decimal('5.50')
    SMALL_DELIVERY_CHARGE = Decimal('3.95')

    if (
        size_counts['large'] > 0 or
        size_counts['medium'] > 2 or
        size_counts['small'] > 4
    ):
        delivery_charge = LARGE_DELIVERY_CHARGE
        delivery_type = 'Large'
    else:
        delivery_charge = SMALL_DELIVERY_CHARGE
        delivery_type = 'Small'

    grand_total = total_price + delivery_charge

    return delivery_charge, delivery_type, grand_total
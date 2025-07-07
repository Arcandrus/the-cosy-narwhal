from product.models import Product
from decimal import Decimal

def bag_contents(request):
    bag = request.session.get('bag', {})
    total_items = sum(bag.values())
    
    grand_total = Decimal('0.00')
    for product_code, quantity in bag.items():
        try:
            product = Product.objects.get(code=product_code)
            grand_total += product.price * quantity
        except Product.DoesNotExist:
            continue  # Skip if product is not found
    
    return {
        'bag_items_count': total_items,
        'bag': bag,
        'grand_total': grand_total,
    }
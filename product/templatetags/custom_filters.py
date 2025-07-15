from django import template
from product.models import Product

register = template.Library()

@register.filter
def replace(value, args):
    old, new = args.split(',')
    return value.replace(old, new)


@register.filter
def product_by_code(code):
    try:
        return Product.objects.get(code=code)
    except Product.DoesNotExist:
        return None
    
    from django import template


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
    
@register.filter
def to_list(start, end):
    """Generate a range from start to end inclusive."""
    return range(start, end + 1)